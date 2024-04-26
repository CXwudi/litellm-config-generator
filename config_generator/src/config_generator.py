import yaml
import json
import os
from .component.model_poper import create_model_list
from .util.configs import io_config, read_config
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# def create_litellm_settings():
#   return {
#     "drop_params": True,
#     # "success_callback": ["clickhouse"],
#     # "failure_callback": ["clickhouse"],
#     "success_callback": ["langfuse"],
#     "failure_callback": ["langfuse"],
#     "add_function_to_prompt": True,
#   }

# def create_general_settings():
#   return {
#     "master_key": litellm_config()["master-key"],
#   }

# def create_environment_variables():
#   return {
#     # Add your environment variables here ...
#   }


def fillin_yaml_data(yaml_data: dict):
  new_yaml_data = {
    "model_list": create_model_list(),
  }
  new_yaml_data.update(yaml_data)
  return new_yaml_data


def read_input(current_dir: str):
  log.info("Reading input template ...")
  input_template = io_config()["input-template"]
  with open(current_dir + "/" + input_template, "r") as stream:
    try:
      yaml_data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      log.error(exc)
  return yaml_data


def write_outputs(current_dir, data):
  output_yaml = io_config()["output-file"]
  output_model_list_txt = io_config()["output-model-list-file"]
  output_model_list_json = io_config()["output-model-list-json"]
  log.info(f"(*^▽^*) All done! Writing to {output_yaml} and {output_model_list_txt}")

  with open(current_dir + "/" + output_yaml, "w") as outfile:
    yaml.dump(data, outfile, default_flow_style=False, sort_keys=False)

  model_name_list = [model["model_name"] for model in data["model_list"]]
  with open(current_dir + "/" + output_model_list_txt, "w") as outfile:
    for name in model_name_list:
      outfile.write(name + ",")
  with open(current_dir + "/" + output_model_list_json, "w") as outfile:
    json.dump(model_name_list, outfile, indent=2)



def main():
  current_dir = os.getcwd()

  read_config(current_dir + "/config.yaml")

  yaml_data = read_input(current_dir)

  log.info("Start filling YAML template file ...")
  data = fillin_yaml_data(yaml_data)

  write_outputs(current_dir, data)






if __name__ == "__main__":
  print("Running config-generator from config_generator.py")
  main()
