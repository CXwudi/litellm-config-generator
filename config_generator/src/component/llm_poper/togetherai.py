from ..abstract_llm_poper import AbstractLLMPoper
from ...util.configs import llm_config
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class TogetherAiProvider(AbstractLLMPoper):

  def __init__(self):
    self.config = llm_config()["togetherai"].as_dict()
    self._text_models = None
    self._image_models = None

  @property
  def text_models(self):
    if self._text_models is None:
      self._text_models, self._image_models = self.read_from_website()
    return self._text_models
  
  @property
  def image_models(self):
    if self._image_models is None:
      self._text_models, self._image_models = self.read_from_website()
    return self._image_models

  def read_from_website(self):
    raw_html = requests.get(
      "https://docs.together.ai/docs/inference-models").text

    # save the raw HTML to file for debugging
    # with open("togetherai.html", "w") as file:
    #   file.write(raw_html)
    soup = BeautifulSoup(raw_html, 'html.parser')
    # Find all tables in the HTML
    # 1st is chat model, 2nd is completion model, 3rd is code model, 4th is image model
    raw_tables = soup.find_all('table') 

    # Split the raw tables into two groups
    # as for litellm is currently only used for chatting, so we decide to only use the first table
    raw_text_model_tables = raw_tables[:1] 
    raw_image_model_table = raw_tables[3]

    text_model_table = []
    image_model_table = []

    # Process the first three tables
    for i, raw_table in enumerate(raw_text_model_tables):
      rows = raw_table.find_all('tr')
      for j in range(1, len(rows)):  # Skip the header
        cells = rows[j].find_all(['th', 'td'])
        log.debug(f"cell in table {i} row {j} is {cells}")
        text_model_table.append({
          "organization": cells[0].text,
          "model_name": cells[1].text,
          "model_string_for_api": cells[2].text,
          "context_length": int(cells[3].text),
        })

    # Process the fourth table
    rows = raw_image_model_table.find_all('tr')
    for j in range(1, len(rows)):  # Skip the header
      cells = rows[j].find_all(['th', 'td'])
      log.debug(f"cell in table 4 row {j} is {cells}")
      image_model_table.append({
        "organization": cells[0].text,
        "model_name": cells[1].text,
        "model_string_for_api": cells[2].text,
      })

    return text_model_table, image_model_table

  def pop_text_models(self) -> list:
    models = [self._text_model_template(model) for model in self.text_models]
    log.info(f"Found {len(models)} text models from TogetherAI, they are {[model["model_name"] for model in models]}")
    return models


  def pop_image_models(self) -> list:
    return [] # currently don't think litellm really support image model in stable diffusion

  def _text_model_template(self, model: dict) -> dict:
    api_name = model["model_string_for_api"]
    name = f"together_ai/{api_name}"
    return {
      "model_name": name,
      "litellm_params": {
        "model": name,
        "api_key": "os.environ/TOGETHERAI_API_KEY",
        # "max_tokens": model["context_length"] # be careful, you could get Error code: 403 - {'error': {'message': 'Input validation error: `inputs` tokens + `max_new_tokens` must be <= 4097. Given: 371 `inputs` tokens and 4096 `max_new_tokens`', 'type': 'invalid_request_error', 'param': 'max_tokens', 'code': None}}"
      },
      "model_info": {
        "description": f"{model["model_name"]} from {model["organization"]}, offered by TogetherAI",
        "max_tokens": model["context_length"]
      }
    }