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

**YOU WILL NEED TO MANUALLY SET UP YOUR MODEL LIBRARY.** Use the examples provided in `config.ini` to point it towards your the models you have downloaded and formatted for GGML/GGUF. (See "Generating a default configuration file" to generate an empty config) 

## Command-line arguments
    
    -h, --help            show this help message and exit
    -m MODEL, --model MODEL
                          Model name from the model library, or path to model file
    -p PROMPT, --prompt PROMPT
                          The desired starting prompt text or a path to a text file containing your prompt
    -s SYSPROMPT, --sysprompt SYSPROMPT
                          The desired system prompt text or path to a text file containing your system prompt.
    -n QTYTOKENS, --qtytokens QTYTOKENS
                          The desired quantity of output tokens.
    -b LLAMABIN, --llamabin LLAMABIN
                          The path to the llama.cpp binary
    -c CONFIG, --config CONFIG
                          Read config INI from specified path
    --gqa GQA             Specify value for GQA
    --prompt-format PROMPT_FORMAT
                          Specify prompt format (must refer to one of the formats listed in config.ini)
    -l, --listmodels      Print a list of available models, then exit.
    --generate-default-config [CONFIG]
                          Generate a default configuration file for this script and write it to the path provided, then exit. If no path is given, a
                          new config file will be written to ~/.config/simple-llamacpp/config.ini

## Execution

For all command strings listed here, run this script directly on a command-prompt. For example:

### Accessing Help

    $> ./llamacpp-chat2.py -h

The above command will output the script's help message. Please refer to it for a listing of how to invoke the script and its options.

### Listing all names of models installed in config.ini

    $> ./llamacpp-chat2.py -l

The above command will output a list of all LLM models listed in `config.ini`. You can paste a name shown in the first column into the value for the `--model` argument. 

### Generating a default configuration file

    $> ./llamacpp-chat2.py --generate-default-config

The above command will generate a default config.ini and place it in `~/.config/simple-llamacpp/config.ini`.

### Running with a simple prompt

    $> ./llamacpp-chat2.py -m nous-13b-q41 -p "Write me a poem about cows"

The above command will run llama.cpp with on the 'nous-13g-q41' model with the prompt, "Write me a poem about cows"

### Running with a simple prompt using a system prompt

    $> ./llamacpp-chat2.py -m nous-13b-q41 -p "Write me a poem about cows" -s prompts.system/assistant.txt

The above command will run llama.cpp with on the 'nous-13g-q41' model with the prompt, "Write me a poem about cows", and will use the system prompt given in the file `prompts.system/assistant.txt`

### Running with both prompt and system prompts in a text file

    $> ./llamacpp-chat2.py -m nous-13b-q41 -p ~/my_longer_prompt.txt -s prompts.system/assistant.txt 

The above command will run llama.cpp with on the 'nous-13g-q41' model with the prompt found in a file called `my_longer_prompt.txt` and will use the system prompt given in the file `prompts.system/assistant.txt`

### Screenshot

Here's a picture of **simple-llamacpp2** in action:

![A screenshot showing this code in action](https://github.com/lyjia/simple-llamacpp/blob/master/doc/screenshot.png?raw=true "A screenshot")

### TODOs:

This version of simple-llamacpp is extremely raw and written in a few hours in one day.

* Make it easier to specify running llama.cpp in "interactive" vs. "oneshot" mode. The script has 'chat' in the name but right now it will quit as soon as llama.cpp gives its response. This is a bit more complicated than simply supplying "-i" to llama.cpp

* Hide-by-default all the verbose text that llama.cpp spits out, the output of a one-shot should be nothing more than the actual LLM output

* Interactive curses, webserver, and/or GUI frontend 

* Add a test suite

### Testing:

This script should work on anything that can run python and llama.cpp. I am personally running this on a FreeBSD 13 server, but I don't see any reason for why it wouldn't work on Linux, Mac, or Windows machines.