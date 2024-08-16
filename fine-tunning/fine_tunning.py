import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torch.optim import AdamW
import soundfile as sf
import pandas as pd
import os
from transformers import AutoTokenizer, DataCollatorWithPadding, get_linear_schedule_with_warmup, TrainingArguments

# Assuming you've already defined or imported the Mustango model class
from mustango import Mustango

# Load the updated tokenizer with the special tokens
tokenizer = AutoTokenizer.from_pretrained("model/tokenizer")

# Load the dataset
df = pd.read_csv("data/super_final_dataset.csv")


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
        audio_path = os.path.join(self.audio_dir, row['PATH'])
        audio, _ = sf.read(audio_path, samplerate=self.sample_rate)

        # Tokenize the input text using the updated tokenizer
        inputs = self.tokenizer(prompt, return_tensors="pt",
                                padding="max_length", truncation=True, max_length=512)
        return inputs, torch.tensor(audio, dtype=torch.float32)


# Instantiate the Mustango model
model = Mustango("declare-lab/mustango", device="cuda:0")

# Load and prepare the dataset
train_dataset = MusicDataset(df, tokenizer, "audio/wav_files")
data_collator = DataCollatorWithPadding(tokenizer=tokenizer, padding=True)
train_loader = DataLoader(train_dataset, batch_size=4,
                          shuffle=True, collate_fn=data_collator)

# Define optimizer using Transformers' AdamW
optimizer = AdamW(model.model.parameters(), lr=5e-5)

# Define a learning rate scheduler using Transformers' scheduler
num_training_steps = len(train_loader) * 3  # Assuming 3 epochs
scheduler = get_linear_schedule_with_warmup(
    optimizer, num_warmup_steps=0, num_training_steps=num_training_steps
)

# Custom function to resize the embedding layer to accommodate new tokens


def resize_token_embeddings(model, tokenizer):
    old_embeddings = model.model.text_encoder.embeddings
    new_num_tokens = len(tokenizer)

    # Create new embedding layer with resized dimensions
    new_embeddings = nn.Embedding(
        new_num_tokens, old_embeddings.weight.size(1))

    # Copy the existing weights to the new embedding layer
    new_embeddings.weight.data[:old_embeddings.weight.size(
        0)] = old_embeddings.weight.data

    # Replace the model's embedding layer with the new one
    model.model.text_encoder.embeddings = new_embeddings


# Resize the embedding layer to account for the new tokens
resize_token_embeddings(model, tokenizer)

# Training loop with checkpoint saving
training_args = TrainingArguments(
    output_dir="checkpoints",
    logging_dir="logs",
    logging_steps=10,
    save_steps=2000,
    save_total_limit=3,
    load_best_model_at_end=True,
    evaluation_strategy="epoch",  # or "steps" depending on your preference
    num_train_epochs=3,  # Number of epochs
)

global_step = 0
for epoch in range(int(training_args.num_train_epochs)):
    model.model.train()  # Ensure the model is in training mode
    for batch in train_loader:
        inputs, labels = batch

        optimizer.zero_grad()

        # Forward pass through the model
        outputs = model.model.inference(
            inputs["input_ids"].to("cuda:0"),
            steps=100,
            guidance=3,
            samples=1,
            disable_progress=True
        )

        # Calculate loss (MSE loss between generated audio and target audio)
        loss = torch.nn.functional.mse_loss(outputs, labels.to("cuda:0"))
        loss.backward()

        # Update model parameters
        optimizer.step()
        scheduler.step()  # Update the learning rate

        global_step += 1
        print(f"Epoch: {epoch}, Step: {global_step}, Loss: {loss.item()}")

    # Save a checkpoint after each epoch
    checkpoint_path = os.path.join(
        training_args.output_dir, f"checkpoint_epoch_{epoch}.pt")
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'scheduler_state_dict': scheduler.state_dict(),
        'loss': loss.item(),
        'global_step': global_step
    }, checkpoint_path)
    print(f"Checkpoint saved at epoch {epoch} to {checkpoint_path}")

# Save the final model and tokenizer
torch.save(model.model.state_dict(), "model/final_model.pt")
tokenizer.save_pretrained("model/final_tokenizer")
