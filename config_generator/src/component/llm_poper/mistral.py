from ..abstract_llm_poper import AbstractLLMPoper
from ...util.common_apis import list_all_model
from ...util.configs import llm_config
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class MistralAiProvider(AbstractLLMPoper):

  def __init__(self):
    self._models = []
    self.config = llm_config()["mistral"].as_dict()
  
  @property
  def models(self):
    if self._models is None or len(self._models) == 0:
      self._models = list_all_model(
        "https://api.mistral.ai/v1/models",
        auth_header={"Authorization": f"Bearer {self.config["api-key"]}"})
    return self._models

  def pop_text_models(self):
    return self._get_models(lambda model_id: "embed" not in model_id and "open" not in model_id)

  def pop_embedding_models(self):
    return self._get_models(lambda model_id: "embed" in model_id)
  
  def _get_models(self, filter_func):
    models = [model for model in self.models if filter_func(model["id"])]
    log.info("Found %d models, they are %s" % (len(models), str([model["id"] for model in models])))
    return [self._template(model) for model in models]

  def _template(self, model: dict) -> dict:
    return {
      "model_name": model["id"],
      "litellm_params": {
        "model": f"mistral/{model["id"]}",
        "api_key": "os.environ/MISTRAL_API_KEY",
      },
      "model_info": {
        "description": "%s from Mistral AI" % model["id"],
      }
    }
