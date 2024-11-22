import os

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("AUTH_EXPIRE_MINUTES", 15))

SECRET_JWT_PRIVATE_KEY = os.environ.get("PRIVATE_JWT_KEY", "")

SECRET_JWT_PUBLIC_KEY = os.environ.get("PUBLIC_JWT_KEY", "")

DB_URI = os.environ.get("DB_URI", "")

DB_MIGRATION_URI = os.environ.get("DB_MIGRATION_URI", "")
