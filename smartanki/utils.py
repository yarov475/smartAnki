import os
import requests
from dotenv import load_dotenv
load_dotenv()
hf = os.getenv("HF")

from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="fal-ai",
    api_key=hf,
)

# output is a PIL.Image object
image = client.text_to_image(
    "Astronaut riding a horse",
    model="black-forest-labs/FLUX.1-dev",
)
image.save(fp=2)
