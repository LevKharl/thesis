import json
import pandas as pd


path = 'data/results-prediction-model-2024-07-30T12-12-55.661248Z-000000000000.jsonl'
file = open(path, 'r')
# {"instance":{"prompt":"Generate a detailed prompt for an AI music (track) generation model based on the following track information:\n- Description: 100% genuine artists. 100% natural sound. OnClassical, an independent label with extraordinary artists focused on solo and chamber music repertoire. A pioneer in the digital music, it has garnered accolades from international music magazines, radios, and audiophiles around the world, for its quality. The best gift Internet has given to audiophiles. —TNT Audio\n\nThe prompt should capture the essence of the track, including the mood, themes, and any distinctive musical elements. The output should be a single sentence that can be used as an input prompt for the AI music generation model. Ensure that the track length and any reference to an album are not mentioned in the output."},"predictions":[{"citationMetadata":{"citations":[]},"content":" Compose a classical music piece with a focus on solo and chamber music repertoire, capturing the essence of natural sound and extraordinary artistry.","safetyAttributes":{"blocked":false,"categories":["Finance","Insult","Profanity","Religion & Belief","Sexual"],"safetyRatings":[{"category":"Dangerous Content","probabilityScore":0.1,"severity":"NEGLIGIBLE","severityScore":0.1},{"category":"Harassment","probabilityScore":0.1,"severity":"NEGLIGIBLE","severityScore":0.1},{"category":"Hate Speech","probabilityScore":0,"severity":"NEGLIGIBLE","severityScore":0},{"category":"Sexually Explicit","probabilityScore":0.1,"severity":"NEGLIGIBLE","severityScore":0.1}],"scores":[0.1,0.1,0.1,0.5,0.1]}}],"status":""}

final_dataset = pd.read_csv('data/rebalanced_dataset.csv')
prompts = []
for line in file:
    data = json.loads(line)
    prediction = data['predictions'][0]['content']
    prompts.append(prediction)

final_dataset['prompt'] = prompts
# remove everything before track name and change  mp3 to wav like 98/25398.mp3 to 25398.wav
final_dataset['PATH'] = final_dataset['PATH'].apply(
    lambda x: x.split('/')[-1].replace('.mp3', '.wav'))
final_dataset.to_csv('data/final_ready_dataset.csv', index=False)
