import secrets

# Générer une clé secrète aléatoire de 32 caractères
secret_key = secrets.token_urlsafe(32)
print(secret_key)