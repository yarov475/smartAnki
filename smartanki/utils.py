from diffusers import StableDiffusionPipeline
import torch
model_id = "nitrosocke/Arcane-Diffusion"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
prompt = "entropy"
image = pipe(prompt).images[0]
image.save("./ai-antropy.png")