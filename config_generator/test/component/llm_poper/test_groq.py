import unittest
from config_generator.src.component.llm_poper.groq import GroqProvider
from config_generator.src.util.configs import read_config


class TestTogetherAiProvider(unittest.TestCase):

  def setUp(self) -> None:
    read_config('config.yaml')
    self.provider = GroqProvider()
