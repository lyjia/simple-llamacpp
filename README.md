# simple-llamacpp

A simple frontend script for chatting with LLM's using llama.cpp

## Requirements

* Python 3.10 or greater
* llama.cpp (https://github.com/ggerganov/llama.cpp), compiled and operational
* At least one LLaMA-derived (or other llama.cpp-compatible) LLM checkpoint

## Installation

**simple-llamacpp** itself has no special dependencies and requires no special installation: simply clone the git repo or download the script and run it with Python.

    git clone https://github.com/lyjia/simple-llamacpp
    cd simple-llamacpp
    chmod +x llamacpp-chat2.py
    ./llamacpp-chat2.py --generate-default-config #generate a default configuration file

However, **simple-llamacpp** does require that you have a binary for llama.cpp and at least one LLaMA-derived LLM model available for it to use, such as LLaMA, LLaMA2, Alcapa, or NousHermes.

To download, install, and/or compile llama.cpp, please visit: https://github.com/ggerganov/llama.cpp. **simple-llamacpp** assumes llama.cpp is compiled to a binary at `~/src/llama.cpp/main`, but this value can be changed in the configuration file or with command-line arguments. 

Depending on the version of llama.cpp you are using, your LLM models need to be converted to GGML or GGUF format. Instructions for doing so can be found in the documentation for llama.cpp.

**simple-llamacpp** does not care what version of llama.cpp you are using, provided the command-line arguments for it are what it expects. This script is written and tested against `master-468ea24`

## Configuration

**simple-llamacpp** expects a configuration INI file, and assumes it resides at `~/.config/simple-llamacpp/config.ini`. An alternate location can be provided via command-line arguments.

## Execution

For all command strings listed here, run this script directly on a command-prompt. For example:

### Accessing Help

    ./llamacpp-chat2.py -h

The above command will output the script's help message. Please refer to it for a listing of how to invoke the script and its options.

### Running with a simple prompt

    ./llamacpp-chat2.py -m nous-13b-q41 -p "Write me a poem about cows"

The above command will run llama.cpp with on the 'nous-13g-q41' model with the prompt, "Write me a poem about cows"

### Running with a simple prompt using a system prompt

    ./llamacpp-chat2.py -m nous-13b-q41 -p "Write me a poem about cows" -s prompts.system/assistant.txt

The above command will run llama.cpp with on the 'nous-13g-q41' model with the prompt, "Write me a poem about cows", and will use the system prompt given in the file `prompts.system/assistant.txt`

### Running with both prompt and system prompts in a text file

     ./llamacpp-chat2.py -m nous-13b-q41 -p ~/my_longer_prompt.txt -s prompts.system/assistant.txt 

The above command will run llama.cpp with on the 'nous-13g-q41' model with the prompt found in a file called `my_longer_prompt.txt` and will use the system prompt given in the file `prompts.system/assistant.txt`