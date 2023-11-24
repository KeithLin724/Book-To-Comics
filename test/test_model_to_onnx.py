# onnx sample
# https://huggingface.co/docs/diffusers/optimization/onnx
from optimum.onnxruntime import ORTStableDiffusionPipeline
import torch

model_id = "runwayml/stable-diffusion-v1-5"
pipeline = ORTStableDiffusionPipeline.from_pretrained(
    model_id,
    export=True,
    # torch_dtype=torch.float16,
    provider=["CUDAExecutionProvider"],
)

pipeline = pipeline.to("cuda")

prompt = "sailing ship in storm by Leonardo da Vinci"
image = pipeline(prompt).images[0]
image.save("sailing ship in storm by Leonardo da Vinci.png")
pipeline.save_pretrained("./onnx-stable-diffusion-v1-5")
