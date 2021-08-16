import os


def manage_sensitive(name):
    secrets_path = os.getenv('SECRETS_PATH', '/run/secrets')
    secret_file_path = os.path.join(secrets_path, name)

    if os.path.exists(secret_file_path):
        with open(secret_file_path) as secret_file:
            return secret_file.read().rstrip('\n')

    return None
