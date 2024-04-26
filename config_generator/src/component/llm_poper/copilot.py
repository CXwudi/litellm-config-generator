from ..abstract_llm_poper import AbstractLLMPoper
from ...util.configs import llm_config
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class GitHubCopilotProvider(AbstractLLMPoper):

  def __init__(self):
    self.config = llm_config()["copilot"].as_dict()

  def pop_text_models(self):
    model_names = ["gpt-4", "gpt-3.5-turbo"]
    list = [self._template(model_name) for model_name in model_names]
    log.info("Using predefined %s models, they are %s" % (len(list), str([model["model_name"] for model in list])))
    return list

  def _template(self, model_name: str) -> dict:
    return {
      "model_name": f"github-copilot/{model_name}",
      "litellm_params": {
        "model": f"{model_name}",
        "api_key": "os.environ/COPILOT_GPT4_SERVICE_SUPER_TOKEN",
        "api_base": self.config["api-base"],
        "custom_llm_provider": "openai",
      },
      "model_info": {
        "description": f"{model_name} from GitHub Copilot, service is hosted using https://github.com/aaamoon/copilot-gpt4-service",
        "input_cost_per_token": "0",
        "output_cost_per_token": "0",
      }
    }