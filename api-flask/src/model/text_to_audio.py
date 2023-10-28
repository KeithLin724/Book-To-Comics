import scipy
import torch
from diffusers import AudioLDM2Pipeline


class TextToAudio:
    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.repo_id = "cvssp/audioldm2"

    def load(self) -> None:
        self.pipe = AudioLDM2Pipeline.from_pretrained(
            self.repo_id, torch_dtype=torch.float16
        )
        self.pipe = self.pipe.to(self.device)
        self.generator = torch.Generator(self.device).manual_seed(0)

    def generate(self, prompt: str, negative_prompt: str):
        # run the generation
        audio = self.pipe(
            prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=200,
            audio_length_in_s=10.0,
            num_waveforms_per_prompt=3,
            generator=self.generator,
        ).audios

        return audio

    @staticmethod
    def save_to_wav(
        data,
        file_name: str,
        rate: int = 16000,
    ):
        # save the best audio sample (index 0) as a .wav file
        scipy.io.wavfile.write(file_name, rate=rate, data=data[0])
        return
