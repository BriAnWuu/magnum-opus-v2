import os

# Install python-dotenv if using default dev server
# from dotenv import load_dotenv
# load_dotenv()


def get_secret(secret_id, backup=None):
    return os.getenv(secret_id, backup)


if get_secret('PIPELINE') == 'production':
    from .production import *
else:
    from .local import *
