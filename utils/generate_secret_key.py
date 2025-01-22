import secrets
import base64

# Gera 32 bytes aleatórios e converte para base64
secret_key = base64.b64encode(secrets.token_bytes(32)).decode('utf-8')
print(f"Generated SECRET_KEY: {secret_key}")