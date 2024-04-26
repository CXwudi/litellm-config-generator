from ..abstract_llm_poper import AbstractLLMPoper
from ...util.common_apis import list_all_model
from ...util.configs import llm_config
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class OpenAIProvider(AbstractLLMPoper):

  def __init__(self):
    self._models = []
    self.config = llm_config()["openai"].as_dict()

  @property
  def models(self):
    if self._models is None or len(self._models) == 0:
      all_models = list_all_model(
        "https://api.openai.com/v1/models",
        auth_header={"Authorization": f"Bearer {self.config["api-key"]}"})
      excluded_models = self.config.get("exclude-models", [])
      for model in all_models:
        if model["id"] not in excluded_models:
          self._models.append(model)
        else:
          log.debug(f"Excluding model {model["id"]} due to exclude-models")
    return self._models


  def pop_text_models(self):
    return self._pop_models(model_prefix="gpt")

  def pop_embedding_models(self):
    return self._pop_models(model_prefix="text-embedding")

  def pop_image_models(self):
    return self._pop_models(model_prefix="dall")
  
  def _pop_models(self, model_prefix: str):
    models = [
      model for model in self.models if (model["id"].startswith(model_prefix))
    ]
    log.info("Found %d models for %s, they are %s" % (len(models), model_prefix, str([model["id"] for model in models])))
    list = [self._template(model) for model in models]
    return list

  def _template(self, model: dict) -> dict:
    template = {
      "model_name": model["id"],
      "litellm_params": {
        "model": f"{model["id"]}",
        "api_key": "os.environ/OPENAI_API_KEY",
        # "api_base": "https://api.openai.com/v1",
      },
      "model_info": {
        "description": f"{model["id"]} from OpenAI Official",
      }
    }
    return template
