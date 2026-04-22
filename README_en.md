# ComfyUI Telegram Suite

![version](https://img.shields.io/badge/version-1.0.4-00aaff?style=for-the-badge)

**Implement Telegram in your ComfyUI workflows.**

[Changelog](CHANGELOG.md)

## Nodes

The main nodes:
<img src="https://github.com/SwissCore92/comfyui-telegram-suite/blob/master/screenshots/main_nodes.png" alt="screenshots/main_nodes.png">

<details><summary>Telegram Bot
</summary>
This node loads your Telegram bot and (optionally) sets a default chat.

You can configure it via: `ComfyUI/user/default/telegram-suite/config.json`
</details>

<details><summary>Send Message
</summary>
This node simply sends a text message.
</details>

<details><summary>Send Image(s)
</summary>
This node sends one or more images (up to 10).

* If the `IMAGE` input contains multiple images and `group` is set to `True`, they will be sent as a media group.
* If `group` is False, the images will be sent individually.
* If `send_as_file` is `True`, the images will be sent as files instead of inline media.

> Note:
> Only the `message(_id)` of the last sent image will be returned in the output.
</details>

<details><summary>Send Video
</summary>
This node sends a video file.

* The video input must be of type `VHS_FILENAMES` (for example, from the `Filenames` output of the ***Video Combine*** node in the [Video Helper Suite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)).

The video can be sent as a regular video, an animation, or a file.
</details>

<details><summary>Send Audio
</summary>
This node sends an audio file.

* It can be sent as an audio message, a voice message, or a file.

</details>

<details><summary>Send Chat Action
</summary>
This node sends chat actions like "typing...", "uploading X...", or "recording X...".
</details>

Additional nodes include message editing, active waiting (Long Polling) for interactive flows, experimental features, and various type converters (see [Triggers](#triggers)).

## Installation

> **Note:** Requires `ffmpeg`!

### Step 1

Install via `ComfyUI Manager` (and skip to [Step 2](#step-2)) or run the following commands:

>⚠️ Make sure your ComfyUI virtual environment is activated and you are in the `ComfyUI/custom_nodes` directory.

```sh
git clone https://github.com/SwissCore92/comfyui-telegram-suite.git
cd comfyui-telegram-suite
pip install -r requirements.txt
```

### Step 2

Restart ComfyUI.

### Step 3

Add your bot(s) and chat(s) to the configuration file.

* Open: `ComfyUI/user/default/telegram-suite/config.json`.
* Add your *bot token(s)* under `"bots"`.
* Add your *chat ID(s)* under `"chats"`.
* **(Optional)** Add the *API URL of your own telegram bot* under `"api_url"`.

Example:

```json
{
    "bots": {
        "MySuperBot": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        "MyOtherSuperBot": "654321:CBA-DEF1234ghIkl-zyx57W2v1u123ew11"
    },
    "chats": {
        "MyPrivateChat": 567891234,
        "MyGroupChat": -1012345678
    },
    "api_url": "https://localhost:8081"
}
```

> Use any string as the key for `"bots"` and `"chats"` — I like to use the Telegram @`user` for clarity.

### Step 4

Restart ComfyUI again — and you are ready to go!

## Triggers

The optional `trigger` inputs/outputs are used to force the execution order in your workflow.

ComfyUI runs by evaluating the output nodes and working backwards to resolve dependencies. I like to think that the inputs "pull" the values they need from the connected outputs.

Passing variables through triggers (passthrough) ensures that a node executes at a specific point during the workflow. Here is an example using [F5-TTS](https://github.com/niknah/ComfyUI-F5-TTS):

<img src="https://github.com/SwissCore92/comfyui-telegram-suite/blob/master/screenshots/trigger_example_tts.png" alt="screenshots/trigger_example_tts.png">

This flow sends the `recording_voice` chat action before generating the audio with the [F5-TTS](https://github.com/niknah/ComfyUI-F5-TTS) node. Once the audio is generated, it is sent to the chat.

> The seed is required by the `F5-TTS Audio` node, so the `Send Chat Action` node ***must*** execute first.

You can use almost any type as a trigger. However, since ComfyUI has strict type checking, you will need to:

* ~~Convert the signal to ANY before feeding it into the trigger input.~~
This step is no longer necessary. You can feed the trigger signal directly into the node now.
* Convert it back to the original type after the trigger output.

*Yes, it is a bit clunky — but it is the only reliable way I have found to control the execution order. That is also why the `converter` category has so many nodes.*

If you have ideas on how to solve this problem more elegantly, feel free to open a PR.

## 🔀 Real Type Converters

This suite includes specialized Converter Nodes (e.g., `Any To INT`, `Any To FLOAT`) designed to bridge the gap between Telegram's text-based outputs and ComfyUI's strict mathematical inputs.
Unlike basic bypass nodes, these converters perform **Real Python Type Casting**. They automatically strip residual JSON quotes (`"`) or extra spaces from your Telegram buttons (e.g., converting the string `"1080"` into a pure integer `1080`), ensuring seamless connection to resolution or parameter nodes.

---

## 🔄 Native Loop-Aware Compatibility

This suite is designed to be 100% compatible with **[ComfyUI-Sequential-Batcher](https://github.com/Meisoftcoltd/ComfyUI-Sequential-Batcher)** and other iterative workflows.

* **Receiver Nodes (`Wait`):** They feature a smart internal cache. During a loop (cycle > 0), they will not pause the execution waiting for a new message; instead, they will "bypass" and automatically return the last received image or text. This prevents your process from getting stuck asking for confirmation on every iteration. (Just connect the current cycle output to the `current_loop_index` pin).
* **Sender Nodes (`Send`):** They incorporate a mute switch (`active`). If connected to the loop index using a node like `CycleMuter`, you can silence the sends on secondary cycles (returning True only on cycle 0). This prevents spamming your Telegram chat while processing a large batch of images!

## 🔗 Advanced Routing: Using the Suite with n8n (Webhook Mode)

If you use the same Telegram Bot token in **n8n** (or Make/Zapier), Telegram will lock the standard `getUpdates` (Long Polling) method. To solve this, our Receive nodes (`Wait For...`) include an **`n8n_webhook`** mode.

This mode turns your ComfyUI into a silent server that waits for n8n to inject the Telegram data.

### 1. ComfyUI Setup

1. Set your `Wait For...` node mode to **`n8n_webhook`**.
2. Connect the `trigger` input to the previous node's `trigger` output to ensure the flow waits correctly.

### 2. n8n HTTP Request Setup (Sending the Payload)

In your n8n workflow, create an **HTTP Request** node triggered by your Telegram Node.

* **Method:** `POST`
* **URL:** `http://<YOUR_COMFYUI_IP>:8188/n8n_telegram_webhook` *(Adjust port if necessary)*
* **Body Content Type:** `JSON`
* **Specify Body:** `Using JSON`

#### A. Payload for Button Clicks (Wait For Callback Query)

Ensure your JSON field is set to **Expression** in n8n and paste:

```javascript
{{
  {
    "button_data": $json.callback_query.data,
    "chat_id": $json.callback_query.message.chat.id
  }
}}
```

#### B. Payload for Text & Media (Wait For Message)

Ensure your JSON field is set to **Expression** in n8n and paste:

```javascript
{{
  {
    "text": $json.message.text || $json.message.caption || "",
    "chat_id": $json.message.chat.id,
    "photo_file_id": $json.message.photo ? $json.message.photo.slice(-1)[0].file_id : "",
    "video_file_id": $json.message.video ? $json.message.video.file_id : ""
  }
}}
```

*Note: ComfyUI will automatically use these `file_id` strings to download the high-res media directly from Telegram's servers. You do NOT need to download the files within n8n!*

## To Do

* [ ] Improve documentation
* [x] Add `Edit Message Video` node
* [x] Add `Edit Message Audio` node
* [x] Add support for Forums/Topics
* [x] Add descriptions and tooltips
* [x] Add active waiting (Long Polling) for interactive receiving nodes

* [ ] Await feedback to refine this list
