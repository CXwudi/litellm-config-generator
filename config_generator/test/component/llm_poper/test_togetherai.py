import unittest
from config_generator.src.component.llm_poper.togetherai import TogetherAiProvider
from config_generator.src.util.configs import read_config


class TestTogetherAiProvider(unittest.TestCase):

  def setUp(self) -> None:
    read_config('config.yaml')
    self.provider = TogetherAiProvider()

  def test_text_models(self):
    models = self.provider.pop_text_models()
    print(models)

  def test_get_html(self):
    text_model_table, image_model_table = self.provider.read_from_website()
    print(f"text_model_table: {text_model_table}")
    print(f"image_model_table: {image_model_table}")

if __name__ == '__main__':
  unittest.main()
