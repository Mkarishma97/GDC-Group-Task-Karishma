from src.connections.hotstreak_connection import HotstreakConnection
from src.classes.utils import load_config


def run_extraction():
    config = load_config("config/config.yml")
    output_path = config["output"]["json_path"]

    connection = HotstreakConnection(output_path)
    connection.run()
