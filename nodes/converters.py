
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

    def convert(self, any):
        if any is None:
            return (0,)
        # Limpia espacios y comillas (" o ')
        clean_val = str(any).strip(' "\'')
        if not clean_val:
            return (0,)
        try:
            # Pasamos por float primero por si el string es "1080.0"
            return (int(float(clean_val)),)
        except ValueError:
            return (0,)

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

    def convert(self, any):
        if any is None:
            return (0.0,)
        clean_val = str(any).strip(' "\'')
        if not clean_val:
            return (0.0,)
        try:
            return (float(clean_val),)
        except ValueError:
            return (0.0,)

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

    def convert(self, any):
        if any is None:
            return (False,)
        clean_val = str(any).strip(' "\'').lower()
        if not clean_val:
            return (False,)
        return (clean_val in ['true', '1', 't', 'y', 'yes', 'on'],)

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

    def convert(self, any):
        # Si ya es string, le quitamos las comillas residuales de JSON
        if isinstance(any, str):
            return (any.strip(' "\''),)
        return (str(any),)

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
    "InvertBOOLEAN": InvertBOOLEAN,
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
    "InvertBOOLEAN": "Invert BOOLEAN",
}