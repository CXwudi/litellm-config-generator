from abc import ABC, abstractmethod

class AbstractLLMPoper(ABC):
  """
  Abstract base class for LLMPoper classes.

  This class defines the interface for populating text, embedding, and image models.
  Subclasses implement the selected abstract methods defined in this class.
  """


  def pop_text_models(self) -> list:
    return []


  def pop_embedding_models(self) -> list:
    return []

  def pop_image_models(self) -> list:
    return []
