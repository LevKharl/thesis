import argparse
import csv
import hashlib
import os.path
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path

import gdown
import requests
from tqdm import tqdm

base_path = Path(__file__).parent
print(f"Base path: {base_path}")
ID_FILE_PATH = '/scratch/project_2008167/lev_thesis/'

download_from_names = {'gdrive': 'GDrive',
                       'mtg': 'MTG', 'mtg-fast': 'MTG Fast mirror'}

CHUNK_SIZE = 512 * 1024  # 512KB


def compute_sha256(filename):
    with open(filename, 'rb') as f:
        contents = f.read()
        checksum = hashlib.sha256(contents).hexdigest()
        return checksum


def download_from_mtg(url, output):
    output_path = Path(output)
    print(f'Downloading from: {url}')
    print(f'To: {output_path}')

    res = requests.get(url, stream=True)
    try:
        total = res.headers.get('Content-Length')
        if total is not None:
            total = int(total)
        with tempfile.NamedTemporaryFile(
            prefix=output_path.name,
            dir=output_path.parent,
            delete=False,
        ) as tmp_file_d:
            tmp_file = tmp_file_d.name
            with tqdm(total=total, unit='B', unit_scale=True) as progressbar:
                for chunk in res.iter_content(chunk_size=CHUNK_SIZE):
                    tmp_file_d.write(chunk)
                    progressbar.update(len(chunk))
        shutil.move(tmp_file_d.name, output)
    finally:
        try:
            os.remove(tmp_file)
        except OSError:
            pass
    return output


def download(dataset, data_type, download_from, output_dir, unpack_tars, remove_tars, track_ids):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if download_from not in download_from_names:
        print(
            f"Unknown --from argument, choices are {list(download_from_names.keys())}", file=sys.stderr)
        return

    print(f'Downloading {dataset} from {download_from_names[download_from]}')
    file_gids = os.path.join(ID_FILE_PATH, dataset +
                             '_' + data_type + '_gids.txt')
    file_sha256_tars = os.path.join(
        ID_FILE_PATH, dataset + '_' + data_type + '_sha256_tars.txt')
    file_sha256_tracks = os.path.join(
        ID_FILE_PATH, dataset + '_' + data_type + '_sha256_tracks.txt')

    print(f"Reading checksum values for tar files from {file_sha256_tars}")
    with open(file_sha256_tars) as f:
        sha256_tars = dict([(row[1], row[0])
                           for row in csv.reader(f, delimiter=' ')])

    print(f"Reading checksum values for tracks from {file_sha256_tracks}")
    with open(file_sha256_tracks) as f:
        sha256_tracks = dict([(row[1], row[0])
                             for row in csv.reader(f, delimiter=' ')])

    # Filenames to download.
    tar_files_to_download = set()
    track_files_to_download = []

    for track_id in track_ids:
        for file, checksum in sha256_tracks.items():
            if track_id in file:
                track_files_to_download.append(file)
                tar_file = f"raw_30s_audio-{int(file.split('/')[0]):02}.tar"
                tar_files_to_download.add(tar_file)
                break

    print(f"Tar files to download: {tar_files_to_download}")
    print(f"Track files to download: {track_files_to_download}")

    # Google IDs to download.
    if download_from == 'gdrive':
        gids = {}
        with open(file_gids, 'r') as f:
            for line in f:
                id, filename = line.split(('   '))[:2]
                gids[filename] = id

    removed = []
    for tar_file in tar_files_to_download:
        output = os.path.join(output_dir, tar_file)
        if os.path.exists(output):
            print(f'Skipping {output} (file already exists)')
            continue

        if download_from == 'gdrive':
            url = f'https://drive.google.com/uc?id={gids[tar_file]}'
            gdown.download(url, output, quiet=False)
        elif download_from == 'mtg':
            url = f'https://essentia.upf.edu/documentation/datasets/mtg-jamendo/{dataset}/{data_type}/{tar_file}'
            download_from_mtg(url, output)
        elif download_from == 'mtg-fast':
            url = f'https://cdn.freesound.org/mtg-jamendo/{dataset}/{data_type}/{tar_file}'
            download_from_mtg(url, output)

        if compute_sha256(output) != sha256_tars[tar_file]:
            print(
                f'{output} does not match the checksum, removing the file', file=sys.stderr)
            removed.append(tar_file)
            os.remove(output)
        else:
            print(f'{tar_file} checksum OK')

    if removed:
        print(f'Missing files: {" ".join(removed)}')
        print('Re-run the script again')
        return

    print('Download complete')

    if unpack_tars:
        print('Unpacking tar archives')
        for tar_file in tar_files_to_download:
            output = os.path.join(output_dir, tar_file)
            print(f'Unpacking {output}')
            tar = tarfile.open(output)
            tar.extractall(path=output_dir)
            tar.close()

            for track in track_files_to_download:
                trackname = os.path.join(output_dir, track)
                if compute_sha256(trackname) != sha256_tracks[track]:
                    print(f'{trackname} does not match the checksum',
                          file=sys.stderr)
                    raise Exception(
                        f'Corrupt file in the dataset: {trackname}')
            print(f'{output} track checksums OK')

            if remove_tars:
                os.remove(output)

        print('Unpacking complete')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download the MTG-Jamendo dataset',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dataset', default='raw_30s', choices=['raw_30s', 'autotagging_moodtheme'],
                        help='dataset to download')
    parser.add_argument('--type', default='audio', choices=['audio', 'audio-low', 'melspecs', 'acousticbrainz'],
                        help='type of data to download (audio, audio in low quality, mel-spectrograms, AcousticBrainz features)')
    parser.add_argument('--from', default='mtg-fast', choices=['mtg', 'mtg-fast'],
                        dest='download_from',
                        help='download from MTG (server in Spain, slow), '
                             'or fast MTG mirror (Finland)')
    parser.add_argument('--outputdir', help='directory to store the dataset')
    parser.add_argument('--unpack', action='store_true',
                        help='unpack tar archives')
    parser.add_argument('--remove', action='store_true',
                        help='remove tar archives while unpacking one by one (use to save disk space)')

    args = parser.parse_args()

    # Read the track IDs from the file
    track_ids_file = os.path.join(base_path, 'track_ids_to_download.txt')
    with open(track_ids_file, 'r') as f:
        track_ids = [line.strip() for line in f]

    # Print track IDs to confirm reading
    print(f"Track IDs to download: {track_ids}")

    # Set the output directory to /scratch/project_2008167/lev_thesis/audio
    output_dir = '/scratch/project_2008167/lev_thesis/audio'

    download(args.dataset, args.type, args.download_from,
             output_dir, args.unpack, args.remove, track_ids)
