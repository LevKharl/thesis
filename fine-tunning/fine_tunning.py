import torch
from transformers import PreTrainedTokenizerFast
from torch.utils.data import DataLoader
from torch.optim import AdamW
import soundfile as sf
from torch.utils.data import Dataset
import pandas as pd
import os

df = pd.read_csv("data/super_final_dataset.csv")

# Load the tokenizer
tokenizer = PreTrainedTokenizerFast(tokenizer_file="model/tokenizer.json",
                                    special_tokens_map_file="model/special_tokens_map.json",
                                    tokenizer_config_file="model/tokenizer_config.json",
                                    added_tokens_file="model/added_tokens.json")

# Load the STFT and VAE models
stft_model = torch.load("model/stft.pt")
vae_model = torch.load("model/vae.pt")

# Load the music diffusion model
music_diffusion_model = torch.load("model/music_diffusion_model")


class MusicDataset(Dataset):
    def __init__(self, dataframe, tokenizer, audio_dir, sample_rate=16000):
        self.dataframe = dataframe
        self.tokenizer = tokenizer
        self.audio_dir = audio_dir
        self.sample_rate = sample_rate

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        row = self.dataframe.iloc[idx]
        prompt = row['input_text']
        audio_path = f"{self.audio_dir}/{row['PATH']}"
        audio, _ = sf.read(audio_path, samplerate=self.sample_rate)

        # Tokenize the input text
        inputs = self.tokenizer(prompt, return_tensors="pt",
                                padding="max_length", truncation=True, max_length=512)
        return inputs, torch.tensor(audio, dtype=torch.float32)


# Load the dataset
train_dataset = MusicDataset(df, tokenizer, "audio/wav_files")

# Create a DataLoader
train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)

# Define optimizer
optimizer = AdamW(music_diffusion_model.parameters(), lr=5e-5)

# Directory to save checkpoints
checkpoint_dir = "model/checkpoints"
os.makedirs(checkpoint_dir, exist_ok=True)

# Training loop with checkpoint saving
num_epochs = 3
save_every_n_steps = 2000  # Save checkpoint every 2000 steps
global_step = 0

for epoch in range(num_epochs):
    for batch in train_loader:
        inputs, labels = batch
        optimizer.zero_grad()

        # Pass the inputs through the model
        outputs = music_diffusion_model(**inputs)

        # Compute the loss (MSE for audio generation)
        loss = torch.nn.functional.mse_loss(outputs, labels)
        loss.backward()
        optimizer.step()

        global_step += 1
        print(f"Epoch: {epoch}, Step: {global_step}, Loss: {loss.item()}")

        # Save checkpoint
        if global_step % save_every_n_steps == 0:
            checkpoint_path = os.path.join(
                checkpoint_dir, f"checkpoint_step_{global_step}.pt")
            torch.save({
                'epoch': epoch,
                'model_state_dict': music_diffusion_model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': loss.item(),
                'global_step': global_step
            }, checkpoint_path)
            print(
                f"Checkpoint saved at step {global_step} to {checkpoint_path}")

# Save the final model
torch.save(music_diffusion_model, "model/fine-tuned-music-diffusion-model.pt")
tokenizer.save_pretrained("model/fine-tuned-tokenizer")
