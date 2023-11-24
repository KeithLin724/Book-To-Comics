from optimum.onnxruntime import ORTStableDiffusionPipeline

model_id = "./onnx-stable-diffusion-v1-5"
pipeline = ORTStableDiffusionPipeline.from_pretrained(model_id)
prompt = "sailing ship in storm by Leonardo da Vinci"
image = pipeline(prompt).images[0]
image.save("sailing ship in storm by Leonardo da Vinci.jpg")
