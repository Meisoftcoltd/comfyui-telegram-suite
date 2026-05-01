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

        if t == "INT":
            script += f"""
class AnyTo{t}(AnyToX):
    RETURN_TYPES = ("{t}",)
    RETURN_NAMES = ("{t}",)

    def convert(self, any):
        # Limpia espacios y comillas (" o ')
        clean_val = str(any).strip(' "\\'')
        # Pasamos por float primero por si el string es "1080.0"
        return (int(float(clean_val)),)
"""
        elif t == "FLOAT":
            script += f"""
class AnyTo{t}(AnyToX):
    RETURN_TYPES = ("{t}",)
    RETURN_NAMES = ("{t}",)

    def convert(self, any):
        clean_val = str(any).strip(' "\\'')
        return (float(clean_val),)
"""
        elif t == "BOOLEAN":
            script += f"""
class AnyTo{t}(AnyToX):
    RETURN_TYPES = ("{t}",)
    RETURN_NAMES = ("{t}",)

    def convert(self, any):
        clean_val = str(any).strip(' "\\'').lower()
        return (clean_val in ['true', '1', 't', 'y', 'yes', 'on'],)
"""
        elif t == "STRING":
            script += f"""
class AnyTo{t}(AnyToX):
    RETURN_TYPES = ("{t}",)
    RETURN_NAMES = ("{t}",)

    def convert(self, any):
        # Si ya es string, le quitamos las comillas residuales de JSON
        if isinstance(any, str):
            return (any.strip(' "\\''),)
        return (str(any),)
"""
        else:
            script += f"""
class AnyTo{t}(AnyToX):
    RETURN_TYPES = ("{t}",)
    RETURN_NAMES = ("{t}",)
"""

        script += f"""
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
    script += """
class InvertBOOLEAN:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BOOLEAN": ("BOOLEAN", {"forceInput": True}),
            },
        }
    FUNCTION = "invert"
    CATEGORY = "Telegram Suite 🔽/converters"

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("BOOLEAN",)

    def invert(self, BOOLEAN):
        return (not BOOLEAN,)
"""

    type_mapping.append("\"InvertBOOLEAN\": InvertBOOLEAN,")
    name_mapping.append("\"InvertBOOLEAN\": \"Invert BOOLEAN\",")

    script += "\ntype_mapping = {\n    " + "\n    ".join([l for l in type_mapping]) + "\n}"
    script += "\nname_mapping = {\n    " + "\n    ".join([l for l in name_mapping]) + "\n}"

    with (Path(__file__).parent.parent / "nodes" / "converters.py").open("w", encoding="utf-8") as f:
        f.write(script)

if __name__ == "__main__":
    main()
