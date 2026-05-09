import io
import os
import mimetypes
import json
import subprocess
from typing import NotRequired, TypedDict, Any
from pathlib import Path

import torchaudio
import numpy as np
from PIL import Image

UINT64_MIN = -9223372036854775808
UINT64_MAX = 9223372036854775807

USER_DIR = Path(os.getcwd()) / "user" / "default"

_CATEGORY = "Telegram Suite 🔽/4. ⚙️ Utils"

class Chat(TypedDict):
    chat_id: int
    topics: NotRequired[dict[str, int]]

class Config(TypedDict):
    bots: dict[str, str]
    chats: dict[str, int | Chat]
    api_url: NotRequired[str]


def load_config() -> Config:
    tg_dir = USER_DIR / "telegram-suite"
    if not tg_dir.exists():
        tg_dir.mkdir(parents=True)
    config_path = tg_dir / "config.json"
    if not config_path.exists():
        cfg = {
            "bots": {
                "<YourBotName>": "<YourToken>"
            },
            "chats": {
                "<YourChatName>": 0
            }
        }
        write_json(config_path, cfg)
        log(f"You need to add a bot to the config file at {config_path}.")
        return cfg # type: ignore

    log("Reading config")
    return read_json(config_path) # type: ignore

def log(message: str) -> None:
    print(f"[Telegram Suite 🔽]: {message}")

def cleanup_params(params: dict[str, Any]) -> dict[str, Any]:
    if params.get("parse_mode") == "None":
        params.pop("parse_mode")

    if params.get("message_thread_id") and params["message_thread_id"] < 0:
        params.pop("message_thread_id")

    return params

def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path: Path, data: dict, *, indent=4) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

def guess_mimetype(file_name: str) -> str:
    return mimetypes.guess_type(file_name)[0] or "application/octet-stream"

def get_temp_path(name: str) -> str:
    """
    Sanitizes a filename and returns a safe path within the 'temp' directory.
    Prevents path traversal by ensuring the result is always inside 'temp'.
    """
    # 1. Basic sanitization of path separators
    clean_name = os.path.basename(name.replace("\\", os.sep))

    # 2. Prevent special names that could still escape or be invalid
    if clean_name in [".", "..", ""]:
        import uuid
        clean_name = f"file_{uuid.uuid4().hex[:8]}"

    # 3. Join with absolute temp directory
    return os.path.join(os.getcwd(), "temp", clean_name)

def images_to_bytes(images, format="PNG") -> list[bytes]:
    bytes_images = []
    for image in images:
        i = 255. * image.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        buf = io.BytesIO()
        img.save(buf, format=format)
        b = buf.getvalue()
        buf.close()
        bytes_images.append(b)

    return bytes_images

def audio_to_wav_bytes(audio, format="WAV") -> bytes:
    waveform = audio['waveform'].squeeze()
    if waveform.ndim == 1:
        waveform = waveform.unsqueeze(0)

    sample_rate = audio.get("sample_rate", 44100)

    buf = io.BytesIO()

    try:
        # En versiones nuevas de torchaudio, torchcodec falla con BytesIO.
        # Forzamos el uso del backend antiguo / soundfile para buffers de memoria.
        import torchaudio
        torchaudio.save(buf, waveform, sample_rate, format="wav", backend="soundfile")
    except Exception as e:
        log(f"⚠️ Aviso: Fallo guardando con soundfile, intentando método fallback. Error: {e}")
        # Método Fallback: Escribir el WAV a mano usando scipy o la librería estándar.
        # ComfyUI suele tener scipy instalado.
        try:
            from scipy.io import wavfile
            wavfile.write(buf, sample_rate, waveform.T.cpu().numpy())
        except ImportError:
            raise RuntimeError("No se pudo convertir el audio. Torchaudio falló y Scipy no está instalado.")

    buf.seek(0)
    b = buf.getvalue()
    buf.close()
    return b

def convert_wav_bytes_ffmpeg(input_bytes: bytes, output_format: str = "mp3") -> bytes:
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "wav",
        "-i", "pipe:0",
    ]

    if output_format == "ogg":
        # Telegram requires Opus in an Ogg container (f=opus).
        # We use libopus explicitly to ensure compatibility.
        cmd += ["-acodec", "libopus", "-f", "opus"]
    else:
        cmd += ["-f", output_format]

    cmd.append("pipe:1")

    result = subprocess.run(
        cmd,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg audio conversion failed: {result.stderr.decode()}")

    return result.stdout

class ParseJSON:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_string": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("DICT",)

    FUNCTION = "parse_json"
    CATEGORY = _CATEGORY

    def parse_json(self, json_string):
        return (json.loads(json_string),)


def bytes_to_image(image_bytes: bytes):
    from PIL import Image, ImageOps
    import numpy as np
    import torch

    img = Image.open(io.BytesIO(image_bytes))
    img = ImageOps.exif_transpose(img)
    image = img.convert("RGB")
    image = np.array(image).astype(np.float32) / 255.0
    image = torch.from_numpy(image)[None,]
    return image
