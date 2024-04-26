from ..abstract_llm_poper import AbstractLLMPoper
from ...util.configs import llm_config
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class AnthropicProvider(AbstractLLMPoper):

  def pop_text_models(self):
    model_names = [
      "claude-3-opus-20240229",
      "claude-3-sonnet-20240229",
      "claude-3-haiku-20240307", 
      "claude-2.1",
      # must use claude-2, instead of 2.0, as LiteLLM uses claude-2
      "claude-2",
      "claude-instant-1.2"
    ]
    list = [self._template(model_name) for model_name in model_names]
    log.info("Using predefined %s models, they are %s" %
             (len(list), str([model["model_name"] for model in list])))
    return list

  def _template(self, model_name: str) -> dict:
    return {
      "model_name": model_name,
      "litellm_params": {
        "model": model_name,
        "api_key": "os.environ/ANTHROPIC_API_KEY",
        "max_tokens":
        4096,  # taken from official doc, this one is needed as it by default is 256 too small.
      },
      "model_info": {
        "description": f"{model_name} from Anthropic Official",
        "max_tokens": 4096,
      }
    }
