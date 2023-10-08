
from base64 import b64encode

def encode_file_to_base64(filepath):
    """Кодирует файл в Base64."""
    with open(filepath, "rb") as f:
        return b64encode(f.read()).decode('utf-8')