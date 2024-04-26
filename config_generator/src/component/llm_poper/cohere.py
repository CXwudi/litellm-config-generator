from ..abstract_llm_poper import AbstractLLMPoper
from ...util.configs import llm_config
import requests
import logging
import json

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class CohereProvider(AbstractLLMPoper):

  def __init__(self) -> None:
    self.config = llm_config()["cohere"].as_dict()
    self._models = None

  @property
  def models(self):
    if self._models is None:
      headers = {'Authorization': 'Bearer ' + self.config['api-key']}
      response = requests.get('https://api.cohere.ai/v1/models', headers=headers)
      if response.status_code == 200:
        self._models = response.json()['models']
      else:
        log.error(f"Failed to fetch models. Status code: {response.status_code}, Response: {response.text}")
    return self._models
  
  def pop_text_models(self) -> list:
    chat_models = [model for model in self.models if "chat" in model['endpoints']]
    # TODO: not completed yet
    return chat_models