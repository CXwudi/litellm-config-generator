from ..abstract_llm_poper import AbstractLLMPoper
from ...util.configs import llm_config
import requests
import logging
import json


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class GeminiAiProvider(AbstractLLMPoper):

  def __init__(self):
    self.config = llm_config()["google"].as_dict()
    self._models = None

  @property
  def models(self):
    if self._models is None:
      url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.config['api-key']}"
      response = requests.get(url)
      if response.status_code == 200:
        self._models = json.loads(response.text)["models"]
      else:
        log.error(f"Failed to fetch models. Status code: {response.status_code}, Response: {response.text}")
    return self._models

  def pop_text_models(self):
    gemini_models = [model for model in self.models if "gemini" in model["name"]]
    list = [self._template(model, ) for model in gemini_models]
    log.info("Found %s gemini models, they are %s" % (len(list), str([model["model_name"] for model in list])))
    return list
  
  def pop_embedding_models(self):
    text_embedding_models = [model for model in self.models if "embedding" in model["name"]]
    list = [self._template(model) for model in text_embedding_models]
    log.info("Found %s google text embedding models, they are %s" % (len(list), str([model["model_name"] for model in list])))
    return list
  
  def _template(self, model: dict) -> dict:
    model_name = model["name"].split("/")[-1]
    return {
      "model_name": model_name,
      "litellm_params": {
        "model": f"gemini/{model_name}",
        "api_key": "os.environ/GEMINI_API_KEY",
      },
      "model_info": {
        "description": f"{model_name} from Google Gemini Official. {model['description']}",
        "max_tokens": model["inputTokenLimit"],
      }
    }
