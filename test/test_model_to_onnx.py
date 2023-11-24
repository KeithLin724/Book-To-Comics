# onnx sample
# https://huggingface.co/docs/diffusers/optimization/onnx
from optimum.onnxruntime import ORTStableDiffusionPipeline

model_id = "runwayml/stable-diffusion-v1-5"
pipeline = ORTStableDiffusionPipeline.from_pretrained(model_id, export=True)
prompt = "sailing ship in storm by Leonardo da Vinci"
image = pipeline(prompt).images[0]
pipeline.save_pretrained("./onnx-stable-diffusion-v1-5")
