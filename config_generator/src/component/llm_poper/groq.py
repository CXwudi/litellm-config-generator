from ..abstract_llm_poper import AbstractLLMPoper
from ...util.common_apis import list_all_model
from ...util.configs import llm_config
import logging
import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class GroqProvider(AbstractLLMPoper):

  def __init__(self):
    self._models = None
    self.config = llm_config()["groq"].as_dict()

  @property
  def models(self):
    if self._models is None:
      all_models = list_all_model(
        "https://api.groq.com/openai/v1/models",
        auth_header={"Authorization": f"Bearer {self.config["api-key"]}"})
      self._models = all_models
    return self._models

  def pop_text_models(self):
    list = [self._template(model) for model in self.models]
    log.info("Found %s models, they are %s" % (len(list), str([model["model_name"] for model in list])))
    return list
  
  def _template(self, model: dict) -> dict:
    model_name = model['id']
    model_name_prefixed = f"groq/{model_name}"
    context_window = model['context_window']
    return {
      "model_name": model_name_prefixed,
      "litellm_params": {
        "model": model_name_prefixed,
        "api_key": "os.environ/GROQ_API_KEY",
      },
      "model_info": {
        "description": f"{model_name} from {model['owned_by']} hosted by Groq, Groq is known for its high performance AI chips, bring up 1000 tokens in seconds",
        "max_tokens": context_window,
      }
    }