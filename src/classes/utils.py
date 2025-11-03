import yaml
import logging
from datetime import datetime

def load_config(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def setup_logging(log_file: str, level: str = "INFO"):
    logging.basicConfig(
        filename=log_file,
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def parse_datetime(dt_str: str):
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except Exception:
        return datetime.utcnow()
