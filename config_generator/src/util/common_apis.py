# api_utils.py
import requests

def list_all_model(url: str, auth_header: dict = None) -> list:
  """
  This function retrieves all model IDs from a given URL.

  Parameters:
  url (str): The URL from which to retrieve the model IDs.
  auth_header (dict): The authentication header to be used in the request.

  Returns:
  list: A list of model IDs if the request is successful.

  Raises:
  Exception: If the request is unsuccessful, an exception is raised with the status code.
  """
  response = requests.get(url, headers=auth_header)
  if response.status_code == 200:
    models = response.json()
    return models["data"]
  else:
    raise Exception(f"Failed to get models. Status code: {response.status_code}")