from ..abstract_llm_poper import AbstractLLMPoper
import logging
from bs4 import BeautifulSoup
import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class GroqProvider(AbstractLLMPoper):

  def __init__(self):
    self._models = None

  @property
  def models(self):
    if self._models is None:
      self._models = self.read_from_webpage()
    return self._models

  def pop_text_models(self):
    list = [self._template(model) for model in self.models]
    log.info("Found %s models, they are %s" % (len(list), str([model["model_name"] for model in list])))
    return list
  
  def read_from_webpage(self):
    raw_html = requests.get(
      "https://console.groq.com/docs/models").text

    # save the raw HTML to file for debugging
    # with open("togetherai.html", "w") as file:
    #   file.write(raw_html)
    soup = BeautifulSoup(raw_html, 'html.parser')

    model_sections = soup.find_all('h3')
    models_info = []

    for section in model_sections:
        details = {}
        ul = section.find_next('ul')
        for li in ul.find_all('li'):
            key = li.strong.text.strip(':')
            value = li.code.text if li.code else li.text.split(': ')[1]
            details[key] = value
        models_info.append(details)
    
    return models_info

  def _template(self, model: dict) -> dict:
    model_name = model['Model ID']
    model_name_prefixed = f"groq/{model_name}"
    context_window = model['Context Window'].split(' ')[0].replace(',', '')
    return {
      "model_name": model_name_prefixed,
      "litellm_params": {
        "model": model_name_prefixed,
        "api_key": "os.environ/GROQ_API_KEY",
      },
      "model_info": {
        "description": f"{model_name} from Groq, Groq is known for its high performance AI chips, bring up 1000 tokens in seconds",
        "max_tokens": int(context_window),
      }
    }