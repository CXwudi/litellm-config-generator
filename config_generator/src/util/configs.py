from config import config
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

_all_config = None

def io_config():
  return _all_config["io"].as_dict()


def llm_config():
  return _all_config["config"]["llm"]

def read_config(file):
  global _all_config
  log.info("Loading config and input template ...")
  _all_config = config(
    ('env', 'APP'),
    ('yaml', file, True)
  )
