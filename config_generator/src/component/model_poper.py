from .llm_poper.openai import OpenAIProvider
from .llm_poper.google import GeminiAiProvider
from .llm_poper.mistral import MistralAiProvider
from .llm_poper.openrouter import OpenRouterProvider
from .llm_poper.copilot import GitHubCopilotProvider
from .llm_poper.groq import GroqProvider
from .llm_poper.anthropic import AnthropicProvider
from .llm_poper.togetherai import TogetherAiProvider
from .abstract_llm_poper import AbstractLLMPoper

import asyncio

def create_model_list() -> list:
  return asyncio.run(_create_model_list())
  

async def _create_model_list() -> list:
  """
  Creates a list of models asynchronously for each provider.

  Returns:
    list: A list of models.
  """
  model_list = []

  all_providers = [
    OpenAIProvider(),
    GitHubCopilotProvider(),
    AnthropicProvider(),
    GeminiAiProvider(),
    MistralAiProvider(),
    GroqProvider(),
    TogetherAiProvider(),
    OpenRouterProvider()
  ]

  tasks = [asyncio.create_task(_do_pop(provider)) for provider in all_providers]

  for result in asyncio.as_completed(tasks):
    model_list += await result # This will raise an exception if the task failed

  return model_list

async def _do_pop(provider: AbstractLLMPoper) -> list:
  text_models = provider.pop_text_models()
  embedding_models = provider.pop_embedding_models()
  image_models = provider.pop_image_models()
  return text_models + embedding_models + image_models