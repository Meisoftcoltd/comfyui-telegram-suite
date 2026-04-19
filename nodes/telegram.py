import json
import logging
import mimetypes
from typing import Any

import time
import os
import torch

from server import PromptServer
from aiohttp import web

import httpx
from colorama import Fore

from . import utils
from . import inputs

# prevent httpx from logging the token
logger = logging.getLogger("httpx").setLevel(logging.CRITICAL)

debug = True

# Buzón global para almacenar las llamadas de n8n
N8N_WEBHOOK_MAILBOX = []

# Endpoint API de ComfyUI. Se adapta automáticamente al puerto del usuario (8188, 8189, etc.)
@PromptServer.instance.routes.post("/n8n_telegram_webhook")
async def n8n_webhook(request):
    try:
        data = await request.json()
        N8N_WEBHOOK_MAILBOX.append(data)
        return web.json_response({"status": "ok", "message": "Payload recibido por ComfyUI"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=400)

_CAT_SEND = "Telegram Suite 🔽/1. 📤 Send"
_CAT_RECEIVE = "Telegram Suite 🔽/2. 📥 Receive"
_CAT_EDIT = "Telegram Suite 🔽/3. ✏️ Edit"
_CAT_UTILS = "Telegram Suite 🔽/4. ⚙️ Utils"
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
    CATEGORY = _CAT_UTILS

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
    CATEGORY = _CAT_UTILS

    def call_api_method(self, bot: TelegramBot, method_name, chat_id=None, params=None):
        params = params if params else {}
        params["chat_id"] = chat_id
        return (bot(method_name, params=params),)


class SendGeneric:
    OUTPUT_NODE = True

    RETURN_TYPES = ("DICT", "INT", "*")
    RETURN_NAMES = ("message", "message_id", "trigger")

    CATEGORY = _CAT_SEND

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
    CATEGORY = _CAT_EDIT
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

    CATEGORY = _CAT_EDIT
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

    CATEGORY = _CAT_EDIT
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

    CATEGORY = _CAT_EDIT
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

    CATEGORY = _CAT_EDIT
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
    CATEGORY = _CAT_SEND

    def send_chat_action(self, bot: TelegramBot, trigger=None, **params):
        result = bot("sendChatAction", params=params)
        return result, trigger

    def get_return_types(self, trigger_type, **kwargs):
        return ("BOOL", trigger_type)


class WaitForMessage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "filter": inputs.update_type,
                "mode": (["long_polling", "n8n_webhook"], {"default": "long_polling", "tooltip": "Use n8n_webhook if sharing the bot token with n8n."}),
                "timeout": ("INT", {"default": 600, "min": 10, "max": 3600, "step": 1, "tooltip": "Max wait time in seconds"}),
            },
            "optional": {
                "trigger": inputs.trigger,
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE", "STRING", "INT", "*")
    RETURN_NAMES = ("text", "image", "video_path", "chat_id", "trigger")
    FUNCTION = "wait_for_msg"
    CATEGORY = _CAT_RECEIVE

    def wait_for_msg(self, bot: TelegramBot, filter, mode, timeout, trigger=None):
        start_time = time.time()

        if mode == "n8n_webhook":
            utils.log(f"⏳ [n8n Mode] Waiting for message via /n8n_telegram_webhook... (Timeout: {timeout}s)")
            N8N_WEBHOOK_MAILBOX.clear()

            while True:
                if len(N8N_WEBHOOK_MAILBOX) > 0:
                    data = N8N_WEBHOOK_MAILBOX.pop(0)

                    text = data.get("text", "")
                    chat_id = data.get("chat_id", 0)
                    photo_file_id = data.get("photo_file_id", "")
                    video_file_id = data.get("video_file_id", "")

                    has_text = bool(text)
                    has_photo = bool(photo_file_id)
                    has_video = bool(video_file_id)

                    if filter == "Text" and not has_text: continue
                    if filter == "Photo" and not has_photo: continue
                    if filter == "Video" and not has_video: continue

                    image = torch.zeros((1, 64, 64, 3))
                    video_path = ""

                    if has_photo and filter in ["All", "Photo"]:
                        b, _ = bot.download_file(photo_file_id)
                        image = utils.bytes_to_image(b)

                    if has_video and filter in ["All", "Video"]:
                        b, name = bot.download_file(video_file_id)
                        temp_path = os.path.join(os.getcwd(), "temp", name)
                        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                        with open(temp_path, "wb") as f:
                            f.write(b)
                        video_path = temp_path

                    utils.log(f"✅ [n8n] Message processed for chat {chat_id}")
                    return (text, image, video_path, chat_id, trigger)

                if time.time() - start_time > timeout:
                    utils.log("❌ Timeout: No message received from n8n.")
                    return ("", torch.zeros((1, 64, 64, 3)), "", 0, trigger)
                time.sleep(1)

        else: # long_polling mode
            utils.log(f"⏳ [Polling Mode] Waiting for direct Telegram message... (Timeout: {timeout}s)")
            latest = bot("getUpdates", params={"limit": 1, "offset": -1})
            next_offset = (latest[0]["update_id"] + 1) if latest else None

            while True:
                params = {"timeout": 30, "allowed_updates": ["message"]}
                if next_offset: params["offset"] = next_offset

                updates = bot("getUpdates", params=params)

                if updates:
                    for update in updates:
                        next_offset = update["update_id"] + 1
                        msg = update.get("message", {})

                        if not msg: continue

                        has_text = "text" in msg or "caption" in msg
                        has_photo = "photo" in msg
                        has_video = "video" in msg

                        if filter == "Text" and not has_text: continue
                        if filter == "Photo" and not has_photo: continue
                        if filter == "Video" and not has_video: continue

                        chat_id = msg.get("chat", {}).get("id", 0)
                        text = msg.get("text", msg.get("caption", ""))
                        image = torch.zeros((1, 64, 64, 3))
                        video_path = ""

                        if has_photo and filter in ["All", "Photo"]:
                            file_id = msg["photo"][-1]["file_id"]
                            b, _ = bot.download_file(file_id)
                            image = utils.bytes_to_image(b)

                        if has_video and filter in ["All", "Video"]:
                            file_id = msg["video"]["file_id"]
                            b, name = bot.download_file(file_id)
                            temp_path = os.path.join(os.getcwd(), "temp", name)
                            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                            with open(temp_path, "wb") as f:
                                f.write(b)
                            video_path = temp_path

                        utils.log(f"✅ [Polling] Message captured from chat {chat_id}")
                        return (text, image, video_path, chat_id, trigger)

                if time.time() - start_time > timeout:
                    utils.log("❌ Timeout: No direct messages in Telegram.")
                    return ("", torch.zeros((1, 64, 64, 3)), "", 0, trigger)
                time.sleep(1)

class SendMessageButtons(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "text": inputs.text,
                "buttons": inputs.buttons,
                "columns": inputs.menu_columns,
            },
            "optional": {
                "trigger": inputs.trigger,
            }
        }

    FUNCTION = "send_menu"

    def send_menu(self, bot: TelegramBot, text, buttons, columns, chat_id, trigger=None, **kwargs):
        # 1. Extraemos todos los botones en una lista plana
        flat_buttons = []
        for btn in buttons.split(","):
            if ":" in btn:
                # Usamos split(":", 1) por si los datos contienen más de dos puntos
                label, data = btn.split(":", 1)
                flat_buttons.append({"text": label.strip(), "callback_data": data.strip()})

        # 2. Agrupamos la lista plana en filas según el número de columnas (Chunking)
        keyboard = [flat_buttons[i:i + columns] for i in range(0, len(flat_buttons), columns)]

        params = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": {"inline_keyboard": keyboard}
        }

        message = bot("sendMessage", params=params)
        return message, message["message_id"], trigger

class WaitForTelegramImage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "chat_id": inputs.chat_id,
                "mode": (["long_polling", "n8n_webhook"], {"default": "long_polling", "tooltip": "Usa long_polling si este bot es exclusivo de ComfyUI. Usa n8n_webhook si compartes el bot."}),
                "timeout": ("INT", {"default": 300, "min": 10, "max": 3600, "step": 1, "tooltip": "Tiempo máximo de espera en segundos"}),
            },
            "optional": {
                "trigger": inputs.trigger,
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "*")
    RETURN_NAMES = ("IMAGE", "MASK", "trigger")
    FUNCTION = "wait_for_image"
    CATEGORY = _CAT_RECEIVE

    def wait_for_image(self, bot: TelegramBot, chat_id, mode, timeout, trigger=None):
        start_time = time.time()

        if mode == "n8n_webhook":
            utils.log(f"⏳ [Modo n8n] Esperando imagen en el endpoint /n8n_telegram_webhook... (Timeout: {timeout}s)")
            N8N_WEBHOOK_MAILBOX.clear()

            while True:
                if len(N8N_WEBHOOK_MAILBOX) > 0:
                    for i, data in enumerate(N8N_WEBHOOK_MAILBOX):
                        photo_file_id = data.get("photo_file_id", "")
                        sender_chat_id = data.get("chat_id", 0)

                        if sender_chat_id == chat_id and photo_file_id:
                            N8N_WEBHOOK_MAILBOX.pop(i)
                            utils.log(f"✅ [n8n] Imagen recibida: {photo_file_id}")
                            b, _ = bot.download_file(photo_file_id)
                            image = utils.bytes_to_image(b)
                            mask = torch.ones((1, image.shape[1], image.shape[2]))
                            return (image, mask, trigger)

                if time.time() - start_time > timeout:
                    utils.log("❌ Timeout: No se recibió ninguna imagen de Telegram.")
                    raise Exception("Timeout: No se recibió ninguna imagen de Telegram")
                time.sleep(1)

        else: # Modo long_polling
            utils.log(f"⏳ [Modo Polling] Esperando imagen directa de Telegram... (Timeout: {timeout}s)")
            latest = bot("getUpdates", params={"limit": 1, "offset": -1})
            next_offset = (latest[0]["update_id"] + 1) if latest else None

            while True:
                params = {"timeout": 30, "allowed_updates": ["message"]}
                if next_offset: params["offset"] = next_offset

                updates = bot("getUpdates", params=params)

                if updates:
                    for update in updates:
                        next_offset = update["update_id"] + 1
                        msg = update.get("message", {})

                        if not msg: continue

                        sender_chat_id = msg.get("chat", {}).get("id", 0)
                        if sender_chat_id == chat_id and "photo" in msg:
                            file_id = msg["photo"][-1]["file_id"]
                            utils.log(f"📸 [Polling] Imagen detectada: {file_id}")
                            b, _ = bot.download_file(file_id)
                            image = utils.bytes_to_image(b)
                            mask = torch.ones((1, image.shape[1], image.shape[2]))
                            return (image, mask, trigger)

                if time.time() - start_time > timeout:
                    utils.log("❌ Timeout: No se recibió ninguna imagen de Telegram.")
                    raise Exception("Timeout: No se recibió ninguna imagen de Telegram")
                time.sleep(1)

class WaitForCallbackQuery:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": inputs.bot,
                "mode": (["long_polling", "n8n_webhook"], {"default": "long_polling", "tooltip": "Usa long_polling si este bot es exclusivo de ComfyUI. Usa n8n_webhook si compartes el bot."}),
                "timeout": ("INT", {"default": 600, "min": 10, "max": 3600, "step": 1, "tooltip": "Tiempo máximo de espera en segundos"}),
            },
            "optional": {
                "trigger": inputs.trigger, # Entrada de activación obligatoria para frenar el flujo
            }
        }

    RETURN_TYPES = ("STRING", "INT", "DICT", "*")
    RETURN_NAMES = ("button_data", "chat_id", "raw_update", "trigger")
    FUNCTION = "wait_for_click"
    CATEGORY = _CAT_RECEIVE

    def wait_for_click(self, bot: TelegramBot, mode, timeout, trigger=None):
        start_time = time.time()

        if mode == "n8n_webhook":
            utils.log(f"⏳ [Modo n8n] Esperando señal en el endpoint /n8n_telegram_webhook... (Timeout: {timeout}s)")
            N8N_WEBHOOK_MAILBOX.clear()

            while True:
                if len(N8N_WEBHOOK_MAILBOX) > 0:
                    data = N8N_WEBHOOK_MAILBOX.pop(0)
                    button_data = data.get("button_data", "")
                    chat_id = data.get("chat_id", 0)
                    utils.log(f"✅ [n8n] Clic recibido: {button_data}")
                    return (button_data, chat_id, data, trigger)

                if time.time() - start_time > timeout:
                    utils.log("❌ Timeout: n8n no respondió.")
                    return ("TIMEOUT", 0, {}, trigger)
                time.sleep(1)

        else: # Modo long_polling original
            utils.log(f"⏳ [Modo Polling] Esperando clic directo de Telegram... (Timeout: {timeout}s)")
            latest = bot("getUpdates", params={"limit": 1, "offset": -1})
            next_offset = (latest[0]["update_id"] + 1) if latest else None

            while True:
                params = {"timeout": 30, "allowed_updates": ["callback_query"]}
                if next_offset: params["offset"] = next_offset

                updates = bot("getUpdates", params=params)

                if updates:
                    for update in updates:
                        next_offset = update["update_id"] + 1
                        if "callback_query" in update:
                            query = update["callback_query"]
                            data = query.get("data", "")
                            chat_id = query.get("message", {}).get("chat", {}).get("id", 0)
                            bot("answerCallbackQuery", params={"callback_query_id": query["id"]})
                            utils.log(f"🔘 [Polling] Clic detectado: {data}")
                            return (data, chat_id, query, trigger)

                if time.time() - start_time > timeout:
                    utils.log("❌ Timeout: No hubo clics en Telegram.")
                    return ("TIMEOUT", 0, {}, trigger)
                time.sleep(1)
