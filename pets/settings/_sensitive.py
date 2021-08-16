import os

from django.core.exceptions import ImproperlyConfigured


def manage_sensitive(name, required=True):
    secrets_path = os.getenv('SECRETS_PATH', '/run/secrets')
    secret_file_path = os.path.join(secrets_path, f'{name}')

    if os.path.exists(secret_file_path):
        with open(secret_file_path) as secret_file:
            return secret_file.read().rstrip('\n')

    if required:
        raise ImproperlyConfigured(f'{name} sensitive data was not found')
    return None
