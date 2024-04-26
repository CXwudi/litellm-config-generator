import unittest
from config_generator.src.component.llm_poper.groq import GroqProvider
from config_generator.src.util.configs import read_config


class TestTogetherAiProvider(unittest.TestCase):

  def setUp(self) -> None:
    read_config('config.yaml')
    self.provider = GroqProvider()

  def test_read_from_webpage(self):
    model_names = self.provider.read_from_webpage()
    print(model_names)