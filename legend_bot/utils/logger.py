import os
import logging
from datetime import datetime

# Garante que a pasta 'logs' existe
LOG_DIR = "legend_bot/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Nome do arquivo com data
log_file = os.path.join(LOG_DIR, "bot.log")

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def info(msg):
    logging.info(msg)

def warn(msg):
    logging.warning(msg)

def error(msg):
    logging.error(msg)

def debug(msg):
    logging.debug(msg)
