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

### Paso 1

Instala a través del `ComfyUI Manager` (y salta al [Paso 2](#paso-2)) o ejecuta los siguientes comandos:

>⚠️ Asegúrate de que tu entorno virtual de ComfyUI esté activado y que te encuentres en el directorio `ComfyUI/custom_nodes`.

```sh
git clone https://github.com/SwissCore92/comfyui-telegram-suite.git
cd comfyui-telegram-suite
pip install -r requirements.txt
```

### Paso 2

Reinicia ComfyUI.

### Paso 3

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

### Paso 4

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

## 🔀 Conversores de Tipo Reales

Esta suite incluye Nodos Conversores especializados (por ejemplo, `Any To INT`, `Any To FLOAT`) diseñados para salvar la brecha entre las salidas basadas en texto de Telegram y las estrictas entradas matemáticas de ComfyUI.
A diferencia de los nodos de paso (bypass) básicos, estos conversores realizan **Casteo de Tipo Real en Python**. Eliminan automáticamente comillas residuales de JSON (`"`) o espacios adicionales de tus botones de Telegram (por ejemplo, convirtiendo la cadena `"1080"` en un número entero puro `1080`), asegurando una conexión perfecta con nodos de resolución o parámetros.

---

## 🔄 Compatibilidad Nativa con Bucles (Loop-Aware)

Esta suite está diseñada para ser 100% compatible con **[ComfyUI-Sequential-Batcher](https://github.com/Meisoftcoltd/ComfyUI-Sequential-Batcher)** y otros flujos de trabajo iterativos.

* **Nodos Receptores (`Wait`):** Cuentan con una caché interna inteligente. Durante un bucle (ciclo > 0), no pausarán la ejecución esperando un nuevo mensaje; en su lugar, harán "bypass" y devolverán automáticamente la última imagen o texto recibido. Esto evita que tu proceso se atasque pidiéndote confirmación en cada iteración. (Solo conecta la salida de ciclo actual al pin `current_loop_index`).
* **Nodos Emisores (`Send`):** Incorporan un interruptor de silenciamiento (`active`). Si se conecta al índice del bucle usando un nodo como `CycleMuter`, puedes silenciar los envíos en ciclos secundarios (devolviendo True solo en el ciclo 0). ¡Esto evita hacer spam en tu chat de Telegram mientras se procesa un lote grande de imágenes!

## 🔗 Enrutamiento Avanzado: Uso de la Suite con n8n (Modo Webhook)

Si utilizas el mismo token del Bot de Telegram en **n8n** (o Make/Zapier), Telegram bloqueará el método estándar `getUpdates` (Long Polling). Para resolver esto, nuestros nodos de Recepción (`Wait For...`) incluyen un modo **`n8n_webhook`**.

Este modo convierte tu ComfyUI en un servidor silencioso que espera a que n8n inyecte los datos de Telegram.

### 1. Configuración de ComfyUI

1. Establece el modo de tu nodo `Wait For...` a **`n8n_webhook`**.
2. Conecta la entrada `trigger` a la salida `trigger` del nodo anterior para asegurar que el flujo espere correctamente.

### 2. Configuración de Petición HTTP en n8n (Envío del Payload)

En tu flujo de trabajo de n8n, crea un nodo de **Petición HTTP** (HTTP Request) que se active mediante tu Nodo de Telegram.

* **Método:** `POST`
* **URL:** `http://<IP_DE_TU_COMFYUI>:8188/n8n_telegram_webhook` *(Ajusta el puerto si es necesario)*
* **Body Content Type:** `JSON`
* **Specify Body:** `Using JSON`

#### A. Payload para Clics de Botones (Wait For Callback Query)

Asegúrate de que tu campo JSON esté configurado como **Expression** en n8n y pega:

```javascript
{{
  {
    "button_data": $json.callback_query.data,
    "chat_id": $json.callback_query.message.chat.id
  }
}}
```

#### B. Payload para Texto y Multimedia (Wait For Message)

Asegúrate de que tu campo JSON esté configurado como **Expression** en n8n y pega:

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

*Nota: ComfyUI usará automáticamente estas cadenas `file_id` para descargar los medios en alta resolución directamente de los servidores de Telegram. ¡NO necesitas descargar los archivos dentro de n8n!*

## Por Hacer

* [ ] Mejorar la documentación
* [x] Añadir nodo `Edit Message Video`
* [x] Añadir nodo `Edit Message Audio`
* [x] Añadir soporte para Foros/Temas
* [x] Añadir descripciones y tooltips
* [x] Añadir espera activa (Long Polling) para nodos de recepción interactivos

* [ ] Esperar comentarios para refinar esta lista
