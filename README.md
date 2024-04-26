# [LiteLLM](https://litellm.vercel.app/docs/proxy/quick_start) Config Generator

A helper python program to generate a configuration file for [LiteLLM](https://litellm.vercel.app/docs/proxy/quick_start) proxy.

Just provide a LiteLLM Proxy configuration file in YAML with `model_list` removed, and then run this program with the following instruction, to get the `model_list` filled up with templates.

## Usage

### 1. Environment Setup

Ensure you have a recent Python 3.x installed on your system.

1. First, create a virtual environment:

    ```sh
    python3 -m venv .venv
    ```

2. Activate the virtual environment:

    On Windows:

    ```sh
    .venv\Scripts\activate
    ```

    On Unix or MacOS:

    ```sh
    source .venv/bin/activate
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

### 2. Configuration

copy the `config.example.yaml` file to `config.yaml`, and the `litellm-template.example.yaml` file to `litellm-template.yaml`.

Fill in the `config.yaml` file with your own configuration.

For the `litellm-template.yaml`, this is where you put your LiteLLM configuration file with `model_list` removed.

### 3. Modify the template to suit your needs

This project contains a `.devcontainer` directory which can be used to quickly setup a dev environment with VSCode and Docker, it contains all the necessary Python related plugins to help you modify this project. (It is also the environment I used to develop this project)

The `config_generator/src/component/model_poper.py` file contains the logic to generate the `model_list`. It delegates the generation to different `AbstractLLMPoper` implementation defined in the `config_generator/src/component/llm_poper` directory.

So far we have the following `AbstractLLMPoper` implementations:

| Provider | Implementation | Support Fetching Model List |
| --- | --- | --- |
| OpenAI | `config_generator/src/component/llm_poper/openai.py` | Yes |
| Google | `config_generator/src/component/llm_poper/google.py` | Yes |
| Anthropic | `config_generator/src/component/llm_poper/anthropic.py` | No |
| Mistral | `config_generator/src/component/llm_poper/mistral.py` | Yes |
| Groq | `config_generator/src/component/llm_poper/groq.py` | Yes |
| [GitHub Copilot](https://gitlab.com/aaamoon/copilot-gpt4-service) | `config_generator/src/component/llm_poper/copilot.py` | No |
| TogetherAI | `config_generator/src/component/llm_poper/togetherai.py` | Yes |

You may be interested in modifying the template in each `AbstractLLMPoper` implementation to suit your needs.

### 4. Run the program

```sh
./run.sh
```

The output LiteLLM configuration file will be saved to `io.output-file`.
