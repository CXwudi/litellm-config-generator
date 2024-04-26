from ..abstract_llm_poper import AbstractLLMPoper
from ...util.common_apis import list_all_model
from ...util.configs import llm_config
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class OpenRouterProvider(AbstractLLMPoper):

  def __init__(self):
    self.config = llm_config()["openrouter"].as_dict()
  
  def pop_text_models(self):
    all_models = list_all_model("https://openrouter.ai/api/v1/models")
    excluded_models = self.config.get("exclude-models", [])
    list = []
    for model in all_models:
      if model["id"] not in excluded_models:
        list.append(self._template(model))
      else:
        log.debug(f"Excluding model {model["id"]} due to exclude-models")
    
    log.info("Found %d models from OpenRouter, they are %s" % (len(list), str([model["model_name"] for model in list])))
    return list

  def _template(self, model: dict) -> dict:
    model_id = f"openrouter/{model["id"]}"
    return {
      "model_name": model_id,
      "litellm_params": {
        "model": model_id,
        "api_key": "os.environ/OPEN_ROUTER_API_KEY",
        # "max_tokens": model["context_length"], 
      },
      "model_info": {
        "id": model_id,
        "description": f"{model["name"]} from OpenRouter. {model["description"]}",
        "max_tokens": model["context_length"]
      }
    }