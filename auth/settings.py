import os

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("AUTH_EXPIRE_MINUTES", 15))

SECRET_JWT_KEY = os.environ.get(
    "AUTH_JWT_KEY", "118a061374eefc35ba1693bcf9663e091c3051493ff7d6ad0c6fd9c6fdb6a2f2"
)
