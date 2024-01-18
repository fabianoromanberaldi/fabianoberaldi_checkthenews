import json


class Configuration:
    def __init__(self) -> None:
        with open("env.json", "r") as env_file:
            env_data = json.load(env_file)

        self.timezone = env_data['timezone']
        self.search_phrase = env_data['search_phrase']
        self.months = env_data['months']
        self.timeout_in_seconds = env_data['timeout_in_seconds']
        self.browser = env_data['browser']
        self.auto_close = env_data['auto_close']
        self.download_images = env_data['download_images']
        self.attempts = env_data['attempts']
