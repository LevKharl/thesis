import vertexai
from vertexai.preview.language_models import TextGenerationModel

# Initialize Vertex AI client
vertexai.init(project='prj-mtp-mika-hamalainen', location='us-central1')

# Load the Text Generation Model (Text Bison)
text_model = TextGenerationModel.from_pretrained("text-bison")

# Define dataset and output destination
dataset = ["gs://lev_thesis/input_prompts_only.jsonl"]
destination_uri_prefix = "gs://lev_thesis/results/"

# Define optional model parameters (if any specific settings are needed)
model_parameters = {
    "max_output_tokens": 50,
    "temperature": 0.4,
    "top_k": 40,
    "top_p": 0.9
}

# Create and submit the batch prediction job
batch_prediction_job = text_model.batch_predict(
    dataset=dataset,
    destination_uri_prefix=destination_uri_prefix,
    model_parameters=model_parameters
)

# Print job details
print("Batch Prediction Job Name:", batch_prediction_job.display_name)
print("Batch Prediction Job Resource Name:",
      batch_prediction_job.resource_name)
print("Batch Prediction Job State:", batch_prediction_job.state)
