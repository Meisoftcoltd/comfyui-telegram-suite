# ComfyUI Telegram Suite

![version](https://img.shields.io/badge/version-1.0.4-00aaff?style=for-the-badge)

**Implementa Telegram en tus flujos de trabajo de ComfyUI.**

[Registro de cambios](CHANGELOG.md)

## Nodos

Los nodos principales:
<img src="https://github.com/SwissCore92/comfyui-telegram-suite/blob/master/screenshots/main_nodes.png" alt="screenshots/main_nodes.png">

<details><summary>Telegram Bot
</summary>
Este nodo carga tu bot de Telegram y (opcionalmente) establece un chat por defecto.

Puedes configurarlo a través de: `ComfyUI/user/default/telegram-suite/config.json`
</details>

<details><summary>Send Message (Enviar Mensaje)
</summary>
Este nodo simplemente envía un mensaje de texto.
</details>

<details><summary>Send Image(s) (Enviar Imagen(es))
</summary>
Este nodo envía una o más imágenes (hasta 10).

* Si la entrada `IMAGE` contiene múltiples imágenes y `group` está establecido en `True`, se enviarán como un grupo multimedia.
* Si `group` es False, las imágenes se enviarán individualmente.
* Si `send_as_file` es `True`, las imágenes se enviarán como archivos en lugar de como medios en línea.

> Nota:
> Solo el `message(_id)` de la última imagen enviada se devolverá en la salida.
</details>

<details><summary>Send Video (Enviar Video)
</summary>
Este nodo envía un archivo de video.

* La entrada de video debe ser del tipo `VHS_FILENAMES` (por ejemplo, de la salida `Filenames` del nodo ***Video Combine*** en la suite [Video Helper Suite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)).

El video se puede enviar como un video normal, una animación o un archivo.
</details>

<details><summary>Send Audio (Enviar Audio)
</summary>
Este nodo envía un archivo de audio.

* Se puede enviar como un mensaje de audio, un mensaje de voz o un archivo.
</details>

<details><summary>Send Chat Action (Enviar Acción de Chat)
</summary>
Este nodo envía acciones de chat como “escribiendo...”, “subiendo X...”, o “grabando X...”.
</details>

Nodos adicionales incluyen edición de mensajes, espera activa (Long Polling) para flujos interactivos, características experimentales y varios convertidores de tipos (ver [Triggers](#triggers)).

## Instalación

> **Nota:** ¡Requiere `ffmpeg`!

### Paso 1:

Instala a través del `ComfyUI Manager` (y salta al [Paso 2](#paso-2)) o ejecuta los siguientes comandos:

>⚠️ Asegúrate de que tu entorno virtual de ComfyUI esté activado y que te encuentres en el directorio `ComfyUI/custom_nodes`.

```sh
git clone https://github.com/SwissCore92/comfyui-telegram-suite.git
cd comfyui-telegram-suite
pip install -r requirements.txt
```

### Paso 2:
Reinicia ComfyUI.

### Paso 3:
Añade tu(s) bot(s) y chat(s) al archivo de configuración.

* Abre: `ComfyUI/user/default/telegram-suite/config.json`.
* Añade tu(s) *token(s) del bot* bajo `"bots"`.
* Añade tu(s) *ID(s) de chat* bajo `"chats"`.
* **(Opcional)** Añade la *URL de la API de tu propio bot de telegram* bajo `"api_url"`.

Ejemplo:
```json
{
    "bots": {
        "MiSuperBot": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        "MiOtroSuperBot": "654321:CBA-DEF1234ghIkl-zyx57W2v1u123ew11"
    },
    "chats": {
        "MiChatPrivado": 567891234,
        "MiChatGrupal": -1012345678
    },
    "api_url": "https://localhost:8081"
}
```
> Usa cualquier cadena como clave para `"bots"` y `"chats"` — Me gusta usar el @`usuario` de Telegram para mayor claridad.

### Paso 4:
Reinicia ComfyUI nuevamente — ¡y ya estás listo para empezar!

## Triggers (Disparadores)

Las entradas/salidas opcionales de `trigger` se usan para forzar el orden de ejecución en tu flujo de trabajo.

ComfyUI se ejecuta evaluando los nodos de salida y trabajando hacia atrás para resolver las dependencias. Me gusta pensar que las entradas "tiran" de los valores que necesitan desde las salidas conectadas.

El paso de variables a través de triggers (passthrough) asegura que un nodo se ejecute en un punto específico durante el flujo de trabajo. Aquí hay un ejemplo usando [F5-TTS](https://github.com/niknah/ComfyUI-F5-TTS):

<img src="https://github.com/SwissCore92/comfyui-telegram-suite/blob/master/screenshots/trigger_example_tts.png" alt="screenshots/trigger_example_tts.png">

Este flujo envía la acción de chat `recording_voice` antes de generar el audio con el nodo [F5-TTS](https://github.com/niknah/ComfyUI-F5-TTS). Una vez generado el audio, se envía al chat.

> El seed es requerido por el nodo `F5-TTS Audio`, así que el nodo `Send Chat Action` ***debe*** ejecutarse primero.

Puedes usar casi cualquier tipo como un trigger. Sin embargo, dado que ComfyUI tiene una verificación de tipos estricta, necesitarás:

* ~~Convertir la señal a ANY antes de introducirla en la entrada del trigger.~~
Este paso ya no es necesario. Puedes alimentar la señal del trigger directamente en el nodo ahora.
* Convertirlo de vuelta al tipo original después de la salida del trigger.

*Sí, es un poco tosco — pero es la única manera confiable que he encontrado de controlar el orden de ejecución. Por eso también la categoría `converter` tiene tantos nodos.*

Si tienes ideas de cómo resolver este problema de una manera más elegante, no dudes en abrir un PR.

## 🔗 Advanced Routing: Using the Suite with n8n (Webhook Mode)

If you use the same Telegram Bot token in **n8n** (or Make/Zapier), Telegram will lock the standard `getUpdates` (Long Polling) method. To solve this, our Receive nodes (`Wait For...`) include an **`n8n_webhook`** mode.

This mode turns your ComfyUI into a silent server that waits for n8n to inject the Telegram data.

### How to configure n8n to send Button Clicks (Callback Queries) to ComfyUI:

1. In ComfyUI, set your `Wait For Button Click` node mode to **`n8n_webhook`**.
2. Connect the `trigger` input to the `trigger` output of your `Send Menu` node (so ComfyUI waits until the menu is sent).
3. In your **n8n workflow**, create an **HTTP Request** node triggered by your Telegram Node (listening for Callback Queries).
4. Configure the n8n HTTP Request as follows:
   * **Method:** `POST`
   * **URL:** `http://<YOUR_COMFYUI_IP>:<YOUR_COMFYUI_PORT>/n8n_telegram_webhook`
     *(Example: `http://192.168.1.100:8189/n8n_telegram_webhook`)*
   * **Body Type:** `JSON`
   * **Send Body:** Map the variables from your Telegram trigger exactly like this:
     ```json
     {
       "button_data": "={{ $json.callback_query.data }}",
       "chat_id": "={{ $json.callback_query.message.chat.id }}"
     }
     ```
5. When the user clicks a button, n8n will instantly POST this JSON to ComfyUI, waking up the flow and passing the data to the rest of your nodes!

### Payload for "Wait For Message" (Text, Images, Videos)
If you are using the `Wait For Message` node in `n8n_webhook` mode, set up an HTTP Request in n8n triggered by standard Telegram messages.

Use this JSON mapping in your n8n Send Body to pass the text and media `file_id` seamlessly to ComfyUI:

```json
{
  "text": "={{ $json.message.text || $json.message.caption || '' }}",
  "chat_id": "={{ $json.message.chat.id }}",
  "photo_file_id": "={{ $json.message.photo ? $json.message.photo[$json.message.photo.length - 1].file_id : '' }}",
  "video_file_id": "={{ $json.message.video ? $json.message.video.file_id : '' }}"
}
```
*Note: ComfyUI will automatically use these `file_id` strings to download the high-res media directly from Telegram's servers. You do NOT need to download the files within n8n!*

## Por Hacer
- [ ] Mejorar la documentación
- [x] Añadir nodo `Edit Message Video`
- [x] Añadir nodo `Edit Message Audio`
- [x] Añadir soporte para Foros/Temas
- [x] Añadir descripciones y tooltips
- [x] Añadir espera activa (Long Polling) para nodos de recepción interactivos

- [ ] Esperar comentarios para refinar esta lista