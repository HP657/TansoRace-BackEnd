from dotenv import dotenv_values


def get_env():
    config = dotenv_values(".env")
    return config
