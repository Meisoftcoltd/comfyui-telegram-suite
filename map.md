# Repositorio Code Map

## File: `__init__.py`

```python
from colorama import Fore

from .nodes import telegram
from .nodes import utils
from .nodes import converters

NODE_CLASS_MAPPINGS = {
    f"TelegramSuite_{k}": v for k, v in {
        "TelegramBot": telegram.TelegramBot,
        "APIMethod": telegram.APIMethod,
        "SendMessage": telegram.SendMessage,
        "SendImage": telegram.SendImage,
        "SendVideo": telegram.SendVideo,
        "SendAudio": telegram.SendAudio,
        "SendChatAction": telegram.SendChatAction,

        "EditMessageText": telegram.EditMessageText,
        "EditMessageCaption": telegram.EditMessageCaption,
        "EditMessageImage": telegram.EditMessageImage,
        "EditMessageVideo": telegram.EditMessageVideo,
        "EditMessageAudio": telegram.EditMessageAudio,

        "ParseJSON": utils.ParseJSON,
        "GetMessages": telegram.GetMessages,
        "SendMessageButtons": telegram.SendMessageButtons,
        "GetCallbackQuery": telegram.GetCallbackQuery,

        **converters.type_mapping
    }.items()
}

NODE_DISPLAY_NAME_MAPPINGS = {
    f"TelegramSuite_{k}": f"{v} 🔽" for k, v in {
        "TelegramBot": "Telegram Bot",
        "APIMethod": "API Method",
        "SendMessage": "Send Message",
        "SendImage": "Send Image(s)",
        "SendVideo": "Send Video",
        "SendAudio": "Send Audio",
        "SendChatAction": "Send Chat Action",

        "EditMessageText": "Edit Message Text",
        "EditMessageCaption": "Edit Message Caption",
        "EditMessageImage": "Edit Message Image",
        "EditMessageVideo": "Edit Message Video",
        "EditMessageAudio": "Edit Message Audio",

        "ParseJSON": "Parse JSON",
        "GetMessages": "Telegram Get Messages",
        "SendMessageButtons": "Telegram Send Menu",
        "GetCallbackQuery": "Telegram Get Callback Query",

        **converters.name_mapping
    }.items()
}

CUSTOM_NODE_INPUT_TYPES = {
    "TELEGRAM_BOT": telegram.TelegramBot,
    "MESSAGES": list[dict],
    "MESSAGE_IDS": list[int],
}

__all__ = (
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "CUSTOM_NODE_INPUT_TYPES",
)

print(f"\n{Fore.LIGHTCYAN_EX}[Telegram Suite 🔽] {len(NODE_CLASS_MAPPINGS)} nodes loaded!{Fore.RESET}\n")

```

## File: `nodes/__init__.py`

```python

```

## File: `nodes/converters.py`

```python

class AnyToX:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": ("*",),
            },
        }

    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    def convert(self, any):
        return (any,)

class AnyToINT(AnyToX):
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("INT",)

class INTToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                f"INT": (f"INT", {"forceInput": True}),
            },
        }
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, INT):
        return (INT,)

class AnyToFLOAT(AnyToX):
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("FLOAT",)

class FLOATToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                f"FLOAT": (f"FLOAT", {"forceInput": True}),
            },
        }
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, FLOAT):
        return (FLOAT,)

class AnyToBOOLEAN(AnyToX):
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("BOOLEAN",)

class BOOLEANToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                f"BOOLEAN": (f"BOOLEAN", {"forceInput": True}),
            },
        }
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, BOOLEAN):
        return (BOOLEAN,)

class AnyToSTRING(AnyToX):
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)

class STRINGToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                f"STRING": (f"STRING", {"forceInput": True}),
            },
        }
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, STRING):
        return (STRING,)

class AnyToDICT(AnyToX):
    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("DICT",)

class DICTToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                f"DICT": (f"DICT", {"forceInput": True}),
            },
        }
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, DICT):
        return (DICT,)

class AnyToMODEL(AnyToX):
    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("MODEL",)

class MODELToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                f"MODEL": (f"MODEL", {"forceInput": True}),
            },
        }
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, MODEL):
        return (MODEL,)

class AnyToCLIP(AnyToX):
    RETURN_TYPES = ("CLIP",)
    RETURN_NAMES = ("CLIP",)

class CLIPToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                f"CLIP": (f"CLIP", {"forceInput": True}),
            },
        }
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, CLIP):
        return (CLIP,)

class AnyToVAE(AnyToX):
    RETURN_TYPES = ("VAE",)
    RETURN_NAMES = ("VAE",)

class VAEToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                f"VAE": (f"VAE", {"forceInput": True}),
            },
        }
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, VAE):
        return (VAE,)

class AnyToIMAGE(AnyToX):
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)

class IMAGEToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                f"IMAGE": (f"IMAGE", {"forceInput": True}),
            },
        }
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, IMAGE):
        return (IMAGE,)

class AnyToAUDIO(AnyToX):
    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("AUDIO",)

class AUDIOToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                f"AUDIO": (f"AUDIO", {"forceInput": True}),
            },
        }
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, AUDIO):
        return (AUDIO,)

class AnyToLATENT(AnyToX):
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("LATENT",)

class LATENTToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                f"LATENT": (f"LATENT", {"forceInput": True}),
            },
        }
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, LATENT):
        return (LATENT,)

type_mapping = {
    "AnyToINT": AnyToINT,
    "INTToAny": INTToAny,
    "AnyToFLOAT": AnyToFLOAT,
    "FLOATToAny": FLOATToAny,
    "AnyToBOOLEAN": AnyToBOOLEAN,
    "BOOLEANToAny": BOOLEANToAny,
    "AnyToSTRING": AnyToSTRING,
    "STRINGToAny": STRINGToAny,
    "AnyToDICT": AnyToDICT,
    "DICTToAny": DICTToAny,
    "AnyToMODEL": AnyToMODEL,
    "MODELToAny": MODELToAny,
    "AnyToCLIP": AnyToCLIP,
    "CLIPToAny": CLIPToAny,
    "AnyToVAE": AnyToVAE,
    "VAEToAny": VAEToAny,
    "AnyToIMAGE": AnyToIMAGE,
    "IMAGEToAny": IMAGEToAny,
    "AnyToAUDIO": AnyToAUDIO,
    "AUDIOToAny": AUDIOToAny,
    "AnyToLATENT": AnyToLATENT,
    "LATENTToAny": LATENTToAny,
}
name_mapping = {
    "AnyToINT": "Any To INT",
    "INTToAny": "INT To Any",
    "AnyToFLOAT": "Any To FLOAT",
    "FLOATToAny": "FLOAT To Any",
    "AnyToBOOLEAN": "Any To BOOLEAN",
    "BOOLEANToAny": "BOOLEAN To Any",
    "AnyToSTRING": "Any To STRING",
    "STRINGToAny": "STRING To Any",
    "AnyToDICT": "Any To DICT",
    "DICTToAny": "DICT To Any",
    "AnyToMODEL": "Any To MODEL",
    "MODELToAny": "MODEL To Any",
    "AnyToCLIP": "Any To CLIP",
    "CLIPToAny": "CLIP To Any",
    "AnyToVAE": "Any To VAE",
    "VAEToAny": "VAE To Any",
    "AnyToIMAGE": "Any To IMAGE",
    "IMAGEToAny": "IMAGE To Any",
    "AnyToAUDIO": "Any To AUDIO",
    "AUDIOToAny": "AUDIO To Any",
    "AnyToLATENT": "Any To LATENT",
    "LATENTToAny": "LATENT To Any",
}
```

## File: `nodes/inputs.py`

```python

from .utils import UINT64_MAX


bot = ("TELEGRAM_BOT", {
    "forceInput": True,
    "tooltip": "Telegram bot instance"
})

method_name = ("STRING", {
    "default": "getMe",
    "tooltip": "The telegram bot api message to call. (case insensitive)"
})

params = ("DICT", {
    "default": {},
    "tooltip": "The method parameters."
})

chat_id = ("INT", {
    "forceInput": True,
    "tooltip": "Unique identifier for the target chat"
})

message_id = ("INT", {
    "forceInput": True,
    "tooltip": "Unique Identifier of the message to edit"
})

trigger = ("*", {
    "forceInput": True,
    "tooltip": "Optional trigger to enforce execution order"
})

text = ("STRING", {
    "multiline": True,
    "default": "",
    "tooltip": "Text of the message to be sent, 1-4096 characters after entities parsing"
})

caption = ("STRING", {
    "multiline": True,
    "default": "",
    "tooltip": "Media caption, 0-1024 characters after entities parsing"
})

parse_mode = (["None", "HTML", "Markdown", "MarkdownV2"], {
    "tooltip": "Mode for parsing entities in the photo caption. "
    "See https://core.telegram.org/bots/api#formatting-options for more details."
})

show_caption_above_media = ("BOOLEAN", {
    "default": False,
    "tooltip": "Pass True, if the caption must be shown above the message media"
})

disable_notification = ("BOOLEAN", {
    "default": True,
    "tooltip": "Sends the message silently. Users will receive a notification with no sound."
})

has_spoiler = ("BOOLEAN", {
    "default": False,
    "tooltip": "Pass True if the media needs to be covered with a spoiler animation"
})

protect_content = ("BOOLEAN", {
    "default": False,
    "tooltip": "Protects the contents of the sent message from forwarding and saving"
})

message_thread_id = ("INT", {
    "default": -1,
    "min": -1,
    "max": UINT64_MAX,
    "tooltip": "Unique identifier for the target message thread of the forum topic (-1 = None)"
})

group = ("BOOLEAN", {
    "default": True,
    "tooltip": "Pass True to send multiple media as media group"
})

send_as_file = ("BOOLEAN", {
    "default": False,
    "tooltip": "Pass True to send the media as file without compression"
})

image_formats = (["PNG", "WEBP", "JPG"], {
    "tooltip": "image format"
})

send_video_as = (["Animation", "Video", "File"], {
    "tooltip": "How to send the video"
})

send_audio_as = (["Voice", "Audio", "File"], {
    "tooltip": "How to send the audio"
})


image = ["IMAGE", {
    "forceInput": True,
    "tooltip": "the image(s) to send"
}]

video = ("VHS_FILENAMES", {
    "forceInput": True,
    "tooltip": "the video to send (VHS)"
})

audio = ("AUDIO", {
    "forceInput": True,
    "tooltip": "the audio to send"
})

chat_action = ([
    "typing",
    "upload_photo",
    "record_video",
    "upload_video",
    "record_voice",
    "upload_voice",
    "upload_document",
    "choose_sticker",
    "find_location",
    "record_video_note",
    "upload_video_note",
], {
    "tooltip": "Type of action to broadcast. "
    "Choose one, depending on what the user is about to receive. "
})

def file_name(default: str):
    return ("STRING", {
        "default": default,
        "tooltip": "the file name for this media"
    })
# Para los menús de botones
buttons = ("STRING", {
    "default": "Opción 1, Opción 2, Opción 3",
    "multiline": True,
    "placeholder": "Nombre Botón 1:data1, Nombre Botón 2:data2",
    "tooltip": "Formato: 'Texto:Comando' separados por comas. Ejemplo: 'Generar:gen, Cancelar:stop'"
})

# Para controlar qué buscamos al recibir
update_type = (["All", "Text", "Photo", "Video"], {
    "default": "All",
    "tooltip": "Filtrar el tipo de mensaje que queremos capturar."
})

```

## File: `nodes/telegram.py`

```python
import json
import logging
import mimetypes
from typing import Any

import httpx
from colorama import Fore

from . import utils
from . import inputs

# prevent httpx from logging the token
logger = logging.getLogger("httpx").setLevel(logging.CRITICAL)

debug = True

_CATEGORY = "Telegram Suite 🔽"
DEFAULT_API_URL = "https://api.telegram.org"

config = utils.load_config()

class TelegramException(Exception): ...

class TelegramBot:
    @classmethod
    def INPUT_TYPES(cls):
        api_urls = [DEFAULT_API_URL]

        if url := config.get("api_url"):
            api_urls = [url, *api_urls]

        return {
            "required": {
                "bot": (list(config.get("bots", {}).keys()), {
                    "tooltip": "Select your telegram bot.\n"
                    f"{utils.USER_DIR}/telegram-suite/config.json"
                }),
            },
            "optional": {
                "chat": (list(config.get("chats", {}).keys()), {
                    "tooltip": "Select your telegram chat.\n"
                    f"{utils.USER_DIR}/telegram-suite/config.json"
                }),
                "api_url": (api_urls, {
                    "tooltip": "The api url to use if you are using your own telegram bot api server.\n"
                    f"{utils.USER_DIR}/telegram-suite/config.json\n"
                    "Eg. 'api_url': 'http://localhost:8081'"
                })
            }
        }

    RETURN_TYPES = ("TELEGRAM_BOT", "INT")
    RETURN_NAMES = ("bot", "chat_id")

    FUNCTION = "init_telegram_bot"
    CATEGORY = _CATEGORY

    @classmethod
    def IS_CHANGED(cls, *args, **kwargs):
        return float("nan")

    def init_telegram_bot(self, bot: str, chat=None, api_url="default"):
        token = config["bots"].get(bot)

        if not token:
            raise ValueError(f"Telegram bot token of bot '{bot}' was not found in {utils.USER_DIR}/telegram-suite/config.json")

        self.base_url = f"{api_url}/bot{token}"

        target_chat: int | dict = config["chats"].get(chat, 0) # type: ignore

        # TODO: maybe implement topics in config (needs dynamic changing of the node)
        topics = {}
        if isinstance(target_chat, dict):
            chat_id = target_chat["chat_id"]
            topics = target_chat.get("topics", {})
        else:
            chat_id = target_chat

        return (self, chat_id)

    def __call__(self, method_name: str, params: dict | None = None, files: dict | None = None):
        params = {
            k: json.dumps(v, ensure_ascii=False, separators=(",", ":"))
            if isinstance(v, (dict, list)) else v
            for k, v in params.items()
            if v # is not None
        } if params else None

        result = httpx.post(
            f"{self.base_url}/{method_name}",
            data=params or None,
            files=files or None,
            timeout=None
        ).json()

        if not result["ok"]:
            if debug:
                f = {k: (v[0], "<file_bytes>", v[2]) for k, v in files.items()} if files else None
                utils.log(f"{method_name}({params=}, files={f}) -> {result}")

            raise TelegramException(f"'{method_name}' was unsuccessful: ", result)

        else:
            utils.log(f"{method_name}(...) -> OK")

        return result["result"]

    def download_file(self, file_id: str):
        # 1. Obtener la ruta del archivo
        file_info = self("getFile", params={"file_id": file_id})
        file_path = file_info["file_path"]
        # 2. Descargar el archivo de los servidores de Telegram
        # Reemplazamos /bot por /file/bot en la URL de descarga
        download_url = self.base_url.replace("/bot", "/file/bot")
        resp = httpx.get(f"{download_url}/{file_path}", timeout=None)
        return resp.content, file_path.split("/")[-1]

class APIMethod:
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, *args, **kwargs):
        return float("nan")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "method_name": inputs.method_name,
            },
            "optional": {
                "chat_id": inputs.chat_id,
                "params": inputs.params
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("RESULT *",)

    FUNCTION = "call_api_method"
    CATEGORY = f"{_CATEGORY}/experimental"

    def call_api_method(self, bot: TelegramBot, method_name, chat_id=None, params=None):
        params = params if params else {}
        params["chat_id"] = chat_id
        return (bot(method_name, params=params),)


class SendGeneric:
    OUTPUT_NODE = True

    RETURN_TYPES = ("DICT", "INT", "*")
    RETURN_NAMES = ("message", "message_id", "trigger")

    CATEGORY = _CATEGORY

    @classmethod
    def IS_CHANGED(cls, *args, **kwargs):
        return float("nan")

    @classmethod
    def VALIDATE_INPUTS(cls, input_types):
        return True

class SendMessage(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "text": inputs.text,
                "parse_mode": inputs.parse_mode,
                "disable_notification": inputs.disable_notification,
                "protect_content": inputs.protect_content,
                "message_thread_id": inputs.message_thread_id
            },
            "optional": {
                "trigger": inputs.trigger,
            }
        }

    FUNCTION = "send_message"

    def send_message(self, bot: TelegramBot, trigger=None, **params):
        params = utils.cleanup_params(params)

        message = bot("sendMessage", params=params)

        return message, message["message_id"], trigger

class SendImage(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "IMAGE": inputs.image,
                "caption": inputs.caption,
                "parse_mode": inputs.parse_mode,
                "show_caption_above_media": inputs.show_caption_above_media,
                "has_spoiler": inputs.has_spoiler,
                "disable_notification": inputs.disable_notification,
                "protect_content": inputs.protect_content,
                "group": inputs.group,
                "send_as_file": inputs.send_as_file,
                "file_name": inputs.file_name("image"),
                "format": inputs.image_formats,
                "message_thread_id": inputs.message_thread_id,
            },
            "optional": {
                "trigger": inputs.trigger
            }
        }

    FUNCTION = "send_photo"

    def send_photo(self, bot: TelegramBot, IMAGE, group, send_as_file, file_name, format, trigger=None, **params):
        id = "document" if send_as_file else "photo"

        params = utils.cleanup_params(params)

        images_bytes = utils.images_to_bytes(IMAGE, format)

        if len(images_bytes) == 1:
            # Single Image
            image_bytes = images_bytes[0]
            params[id] = f"attach://{id}"
            file_name = file_name or "image"
            file_name = f"{file_name}.{format.lower()}"
            message = bot(
                "sendDocument" if send_as_file else "sendPhoto",
                params=params,
                files={id: (file_name, image_bytes, utils.guess_mimetype(file_name))}
            )
            return message, message["message_id"], trigger

        else:
            if group:
                # Multiple images - send as media group
                media = []
                files = {}
                file_name = file_name or "image"
                for i, b in enumerate(images_bytes):
                    name = f"{file_name}{i}.{format.lower()}"
                    files[f"{id}{i}"] = (name, b, utils.guess_mimetype(name))

                    m: dict[str, Any] = {
                        "type": "document" if send_as_file else "photo",
                        "media": f"attach://{id}{i}",
                    }
                    if params.get("caption"):
                        m["caption"] = params["caption"]
                    if params.get("parse_mode", "None") != "None":
                        m["parse_mode"] = params["parse_mode"]
                    if id != "document":
                        m["show_caption_above_media"] = (params["show_caption_above_media"] or None)

                    media.append(m)

                messages = bot(
                    "sendMediaGroup",
                    params={
                        "chat_id": params["chat_id"],
                        "media": media,
                        "disable_notification": params["disable_notification"] or None,
                        "protect_content": params["protect_content"] or None,
                    },
                    files=files
                )
                return messages[-1], messages[-1]["message_id"], trigger

            else:
                # Multiple images - send individually
                messages = []
                for index, image_bytes in enumerate(images_bytes):
                    params[id] = f"attach://{id}"
                    name = f"{file_name}_{index}.{format.lower()}"

                    if id == "document":
                        params.pop("show_caption_above_media")

                    messages.append(
                        bot(
                            "sendDocument" if send_as_file else "sendPhoto",
                            params=params,
                            files={id: (name, image_bytes, utils.guess_mimetype(name))}
                        )
                    )
                return messages[-1], messages[-1]["message_id"], trigger

class SendVideo(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "video": inputs.video,
                "caption": inputs.caption,
                "parse_mode": inputs.parse_mode,
                "show_caption_above_media": inputs.show_caption_above_media,
                "has_spoiler": inputs.has_spoiler,
                "disable_notification": inputs.disable_notification,
                "protect_content": inputs.protect_content,
                "send_as": inputs.send_video_as,
                "message_thread_id": inputs.message_thread_id
            },
            "optional": {
                "trigger": inputs.trigger
            }
        }

    FUNCTION = "send_video"

    def send_video(self, bot: TelegramBot, video, send_as, trigger=None, **params):
        params = utils.cleanup_params(params)

        file_path = [v for v in video[1] if not v.endswith(".png")][0]

        file_name = file_path.rsplit("/", 1)[-1]
        mimetype = mimetypes.guess_type(file_name)[0] or "application/octet_stream"

        if send_as == "File":
            send_as = "Document"

        id = send_as.lower()

        params[id] = f"attach://{id}"

        with open(file_path, "rb") as f:
            message = bot(
                f"send{send_as}",
                params=params,
                files={id: (file_name, f.read(), mimetype)}
            )

        return message, message["message_id"], trigger

class SendAudio(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "audio": inputs.audio,
                "caption": inputs.caption,
                "parse_mode": inputs.parse_mode,
                "show_caption_above_media": inputs.show_caption_above_media,
                "disable_notification": inputs.disable_notification,
                "protect_content": inputs.protect_content,
                "send_as": inputs.send_audio_as,
                "file_name": inputs.file_name("audio"),
                "message_thread_id": inputs.message_thread_id
            },
            "optional": {
                "trigger": inputs.trigger
            }
        }

    FUNCTION = "send_audio"

    def send_audio(self, bot: TelegramBot, audio, send_as, file_name, trigger=None, **params):
        params = utils.cleanup_params(params)

        params["caption"] = params["caption"] or None

        format = "ogg" if send_as == "Voice" else "mp3" if send_as == "Audio" else "wav"

        wav_bytes = utils.audio_to_wav_bytes(audio)

        file_name = file_name or "audio"

        name = f"{file_name}.{format}"

        if send_as == "File":
            params["document"] = "attach://document"
            message = bot("sendDocument", params=params, files={"document": (name, wav_bytes, utils.guess_mimetype(name))})
            return message, message["message_id"], trigger

        id = "audio" if send_as == "Audio" else "voice"
        params[id] = f"attach://{id}"

        b = utils.convert_wav_bytes_ffmpeg(wav_bytes, "mp3" if send_as == "Audio" else "ogg")

        message = bot(f"send{id.capitalize()}", params=params, files={id: (name, b, utils.guess_mimetype(name))})

        return message, message["message_id"], trigger


class EditMessageText(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "message_id": inputs.message_id,
                "text": inputs.text,
                "parse_mode": inputs.parse_mode,
            },
            "optional": {
                "trigger": inputs.trigger
            }
        }
    CATEGORY = f"{_CATEGORY}/edit"
    FUNCTION = "edit_message_text"

    def edit_message_text(self, bot: TelegramBot, trigger=None, **params):
        params = utils.cleanup_params(params)

        message = bot("editMessageText", params=params)

        return message, message["message_id"], trigger

class EditMessageCaption(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "message_id": inputs.message_id,
                "caption": inputs.caption,
                "parse_mode": inputs.parse_mode,
                "show_caption_above_media": inputs.show_caption_above_media,
            },
            "optional": {
                "trigger": ("*", {"forceInput": True})
            }
        }

    CATEGORY = f"{_CATEGORY}/edit"
    FUNCTION = "edit_message_caption"

    def edit_message_caption(self, bot: TelegramBot, trigger=None, **params):
        if params["parse_mode"] == "None":
            params.pop("parse_mode")

        message = bot("editMessageCaption", params=params)

        return message, message["message_id"], trigger

class EditMessageImage(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "message_id": inputs.message_id,
                "IMAGE": inputs.image,
                "caption": inputs.caption,
                "parse_mode": inputs.parse_mode,
                "show_caption_above_media": inputs.show_caption_above_media,
                "file_name": inputs.file_name("image"),
                "format": inputs.image_formats,
                "as_file": inputs.send_as_file,
            },
            "optional": {
                "trigger": inputs.trigger
            }
        }

    CATEGORY = f"{_CATEGORY}/edit"
    FUNCTION = "edit_message_image"

    def edit_message_image(self, bot: TelegramBot, IMAGE, file_name, format,  as_file, trigger=None, **params):
        params = utils.cleanup_params(params)

        name = f"{file_name}.{format.lower()}"

        _params = {
            "chat_id": params["chat_id"],
            "message_id": params["message_id"],
            "media": {k: v for k, v in {
                "type": "document" if as_file else "photo",
                "media": "attach://media",
                "caption": params.get("caption"),
                "parse_mode": params.get("parse_mode"),
                "show_caption_above_media": params.get("show_caption_above_media")
            }.items() if v}
        }

        b = utils.images_to_bytes(IMAGE, format)

        files = {"media": (name, b, utils.guess_mimetype(name))}

        message = bot("editMessageMedia", params=_params, files=files)

        return message, message["message_id"], trigger

class EditMessageVideo(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "message_id": inputs.message_id,
                "video": inputs.video,
                "caption": inputs.caption,
                "parse_mode": inputs.parse_mode,
                "show_caption_above_media": inputs.show_caption_above_media,
                "send_as": inputs.send_video_as,
            },
            "optional": {
                "trigger": inputs.trigger
            }
        }

    CATEGORY = f"{_CATEGORY}/edit"
    FUNCTION = "edit_message_video"

    def edit_message_video(self, bot: TelegramBot, video, send_as, trigger=None, **params):
        params = utils.cleanup_params(params)

        file_path = [v for v in video[1] if not v.endswith(".png")][0]
        file_name = file_path.rsplit("/", 1)[-1]

        if send_as == "File":
            send_as = "Document"

        id = send_as.lower()

        _params = {
            "chat_id": params["chat_id"],
            "message_id": params["message_id"],
            "media": {k: v for k, v in {
                "type": id,
                "media": "attach://media",
                "caption": params.get("caption"),
                "parse_mode": params.get("parse_mode"),
                "show_caption_above_media": params.get("show_caption_above_media")
            }.items() if v}
        }

        with open(file_path, "rb") as f:
            files = {"media": (file_name, f.read(), utils.guess_mimetype(file_name))}
            message = bot("editMessageMedia", params=_params, files=files)
            return message, message["message_id"], trigger

class EditMessageAudio(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "message_id": inputs.message_id,
                "audio": inputs.audio,
                "caption": inputs.caption,
                "parse_mode": inputs.parse_mode,
                "show_caption_above_media": inputs.show_caption_above_media,
                "file_name": inputs.file_name("audio"),
                "as_file": inputs.send_as_file,
            },
            "optional": {
                "trigger": inputs.trigger
            }
        }

    CATEGORY = f"{_CATEGORY}/edit"
    FUNCTION = "edit_message_audio"

    def edit_message_audio(self, bot: TelegramBot, audio, file_name, as_file, trigger=None, **params):
        params = utils.cleanup_params(params)

        ext = "wav" if as_file else "mp3"

        name = f"{file_name}.{ext}"

        _params = {
            "chat_id": params["chat_id"],
            "message_id": params["message_id"],
            "media": {k: v for k, v in {
                "type": "document" if as_file else "audio",
                "media": "attach://media",
                "caption": params.get("caption"),
                "parse_mode": params.get("parse_mode"),
                "show_caption_above_media": params.get("show_caption_above_media")
            }.items() if v}
        }

        b = utils.audio_to_wav_bytes(audio)
        if not as_file:
            b = utils.convert_wav_bytes_ffmpeg(b)

        files = {"media": (name, b, utils.guess_mimetype(name))}

        message = bot("editMessageMedia", params=_params, files=files)

        return message, message["message_id"], trigger

class SendChatAction:
    @classmethod
    def IS_CHANGED(cls, *args, **kwargs):
        return float("nan")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "action": inputs.chat_action,
                "message_thread_id": inputs.message_id,
            },
            "optional": {
                "trigger": inputs.trigger
            }
        }

    RETURN_TYPES = ("BOOL", "*")
    RETURN_NAMES = ("True", "trigger")

    FUNCTION = "send_chat_action"
    CATEGORY = _CATEGORY

    def send_chat_action(self, bot: TelegramBot, trigger=None, **params):
        result = bot("sendChatAction", params=params)
        return result, trigger

    def get_return_types(self, trigger_type, **kwargs):
        return ("BOOL", trigger_type)


class GetMessages:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "filter": inputs.update_type,
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE", "STRING", "INT")
    RETURN_NAMES = ("text", "image", "video_path", "chat_id")
    FUNCTION = "fetch"
    CATEGORY = "Telegram Suite 🔽/receive"

    def fetch(self, bot: TelegramBot, filter):
        import torch
        import os
        # offset -1 para leer solo el último mensaje
        updates = bot("getUpdates", params={"limit": 1, "offset": -1})
        if not updates:
            return ("", torch.zeros((1, 64, 64, 3)), "", 0)

        msg = updates[0].get("message", {})
        chat_id = msg.get("chat", {}).get("id", 0)

        text = msg.get("text", "")
        image = torch.zeros((1, 64, 64, 3))
        video_path = ""

        # Lógica de descarga según el contenido
        if "photo" in msg and filter in ["All", "Photo"]:
            file_id = msg["photo"][-1]["file_id"] # La de mayor resolución
            b, _ = bot.download_file(file_id)
            image = utils.bytes_to_image(b)

        if "video" in msg and filter in ["All", "Video"]:
            file_id = msg["video"]["file_id"]
            b, name = bot.download_file(file_id)
            # Guardamos temporalmente para que Comfy lo lea
            temp_path = os.path.join(os.getcwd(), "temp", name)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(b)
            video_path = temp_path

        return (text, image, video_path, chat_id)

class SendMessageButtons(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "text": inputs.text,
                "buttons": inputs.buttons,
            }
        }

    FUNCTION = "send_menu"

    def send_menu(self, bot: TelegramBot, text, buttons, chat_id, **kwargs):
        # Convertimos "Nombre:data" en estructura JSON de botones
        keyboard = []
        for btn in buttons.split(","):
            if ":" in btn:
                label, data = btn.split(":")
                keyboard.append([{"text": label.strip(), "callback_data": data.strip()}])

        params = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": {"inline_keyboard": keyboard}
        }

        message = bot("sendMessage", params=params)
        return message, message["message_id"], None

class GetCallbackQuery:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
            }
        }

    RETURN_TYPES = ("STRING", "INT", "DICT")
    RETURN_NAMES = ("button_data", "chat_id", "raw_update")
    FUNCTION = "get_click"
    CATEGORY = "Telegram Suite 🔽/receive"

    def get_click(self, bot: TelegramBot):
        # Buscamos actualizaciones de tipo 'callback_query'
        updates = bot("getUpdates", params={"limit": 1, "offset": -1, "allowed_updates": ["callback_query"]})

        if updates and "callback_query" in updates[0]:
            query = updates[0]["callback_query"]
            data = query.get("data", "") # El 'comando' que pusimos en el botón
            chat_id = query.get("message", {}).get("chat", {}).get("id", 0)

            # 💡 Opcional: Responder a Telegram que hemos recibido el clic (quita el reloj de carga en el botón)
            bot("answerCallbackQuery", params={"callback_query_id": query["id"]})

            utils.log(f"🔘 Botón pulsado: {data} por {chat_id}")
            return (data, chat_id, query)

        return ("", 0, {})

```

## File: `nodes/utils.py`

```python
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

_CATEGORY = "Telegram Suite 🔽/experimental"

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
    torchaudio.save(buf, waveform, sample_rate, format="wav") # type: ignore
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
        # "-f", output_format,
        "-f", "opus" if output_format == "ogg" else output_format, #TODO: test (using libopus)
        "pipe:1"
    ]

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

```

## File: `scripts/create_converters.py`

```python
from pathlib import Path

# This script is for automatically generate the converters.py file.
# Add more types here if needed.
TYPES = [
    "INT",
    "FLOAT",
    "BOOLEAN",
    "STRING",
    "DICT",
    "MODEL",
    "CLIP",
    "VAE",
    "IMAGE",
    "AUDIO",
    "LATENT",
]

def main():
    script = """
class AnyToX:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": ("*",),
            },
        }

    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    def convert(self, any):
        return (any,)
"""

    type_mapping = []
    name_mapping = []

    for t in TYPES:
        type_mapping.append(f"\"AnyTo{t}\": AnyTo{t},")
        type_mapping.append(f"\"{t}ToAny\": {t}ToAny,")
        name_mapping.append(f"\"AnyTo{t}\": \"Any To {t}\",")
        name_mapping.append(f"\"{t}ToAny\": \"{t} To Any\",")

        script += f"""
class AnyTo{t}(AnyToX):
    RETURN_TYPES = ("{t}",)
    RETURN_NAMES = ("{t}",)

class {t}ToAny:
    @classmethod
    def INPUT_TYPES(cls):
        return {{
            "required": {{
                f"{t}": (f"{t}", {{"forceInput": True}}),
            }},
        }}
    FUNCTION = "convert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("any",)

    def convert(self, {t}):
        return ({t},)
"""
    script += "\ntype_mapping = {\n    " + "\n    ".join([l for l in type_mapping]) + "\n}"
    script += "\nname_mapping = {\n    " + "\n    ".join([l for l in name_mapping]) + "\n}"

    with (Path(__file__).parent.parent / "nodes" / "converters.py").open("w", encoding="utf-8") as f:
        f.write(script)

if __name__ == "__main__":
    main()

```

## Repository Structure Summary

```text
.
├── __init__.py
├── nodes/
│   ├── __init__.py
│   ├── converters.py
│   ├── inputs.py
│   ├── telegram.py
│   └── utils.py
└── scripts/
    └── create_converters.py
```
