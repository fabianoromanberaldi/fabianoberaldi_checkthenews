import json


class Configuration:
    def __init__(self) -> None:
        with open("env.json", "r") as env_file:
            env_data = json.load(env_file)

        self.timezone = env_data['timezone']
        self.filter_text = env_data['filter_text']
        self.months = env_data['months']
        self.timeout_in_seconds = env_data['timeout_in_seconds']
        self.browser = env_data['browser']
        self.download_images = env_data['download_images']
