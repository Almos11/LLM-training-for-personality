import os
import torch
from pathlib import Path
from safetensors import SafetensorError
from safetensors.torch import load_file as safetensors_load

def convert_safetensors_to_bin(directory, from_safetensors=True):
    if from_safetensors:
        print("Converting .safetensor files to PyTorch binaries (.bin)")
        for safetensor_path in Path(directory).glob("*.safetensors"):
            bin_path = safetensor_path.with_suffix(".bin")
            try:
                result = safetensors_load(safetensor_path)
            except SafetensorError as e:
                raise RuntimeError(f"{safetensor_path} is likely corrupted. Please try to re-download it.") from e
            print(f"{safetensor_path} --> {bin_path}")
            torch.save(result, bin_path)
            os.remove(safetensor_path)
            print(f"Deleted {safetensor_path}")

# Укажите путь к папке с файлами .safetensors
directory_path = "Meta-Llama-3-8B"
convert_safetensors_to_bin(directory_path)

