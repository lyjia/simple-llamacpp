#!/usr/bin/env python

###############################################################################
# Simple frontend script for interacting with llama.cpp
# Requires python 3.10 or greater, no dependencies
# (C) 2023 Lyjia - September 2023
# https://github.com/lyjia/simple-llamacpp
#
# Please see README.md or the above github link for instructions.
###############################################################################

import curses
from argparse import ArgumentParser, Action
from configparser import ConfigParser
from pathlib import Path
from tempfile import NamedTemporaryFile
from subprocess import run
from sys import argv
import os


def msg(str):
    print(str)


#############
# Constants #
#############
VERSION = "0.2"

CFG_DEFAULT = "DEFAULTS"
CFG_PROMPT_FORMATS = "PROMPT.FORMATS"
CFG_MODELS = "MODELS"

CFG_DEF_QTYTOKES = "qtytokens"
CFG_DEF_LLAMABIN = "llamabin"
CFG_DEF_MODELPATH = "modelpath"

CFG_MOD_PATH = "path"
CFG_MOD_PATH_F16 = "f16"
CFG_MOD_PATH_Q4_0 = "q4_0"
CFG_MOD_PATH_Q4_1 = "q4_1"
CFG_MOD_PATH_Q5_0 = "q5_0"
CFG_MOD_PATH_Q5_1 = "q5_1"
CFG_MOD_PATH_Q8_0 = "q8_0"
CFG_MOD_DEFAULT_Q = "defaultq"
CFG_MOD_CONTEXT_LEN = "context"


CFG_MOD_DESC = "desc"
CFG_MOD_FMT = 'promptformat'
CFG_MOD_GQA = "gqa"

PRMT_FMT_ALPACA = 'alpaca'
PRMT_FMT_LLAMA2 = 'llama2'
PRMT_FMT_CHATML = 'chatml'

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/simple-llamacpp/config.ini")

DEFAULTS = {
    CFG_DEF_LLAMABIN:  '~/src/llama.cpp/main',
    CFG_DEF_QTYTOKES:  256,
    CFG_DEF_MODELPATH: '~/data/ml/LLM'
}

PROMPT_FORMATS = {
    PRMT_FMT_ALPACA: '### Instruction:\n{MAINPROMPT}\n\n### Input: {SYSTEMPROMPT}\n\n### Reponse:\n',
    PRMT_FMT_LLAMA2: '[INST]<<SYS>>{SYSTEMPROMPT}<</SYS>>{MAINPROMPT}[/INST]',
    PRMT_FMT_CHATML: '<|im_start|>system\n{SYSTEMPROMPT}<|im_end|>\n<|im_start|>user\n{MAINPROMPT}<|im_end|>'
}

#################
# Initial setup #
#################
config = ConfigParser()


def load_config(args):
    global config
    config_file = DEFAULT_CONFIG_PATH
    if args.config is None:
        config_file = args.config
    msg("Loading config from {} ...".format(config_file))
    config.read(config_file)


class GenerateDefaultConfigAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        global config
        config[CFG_DEFAULT] = DEFAULTS
        config[CFG_PROMPT_FORMATS] = PROMPT_FORMATS

        # some examples for specifying models
        models = {
            'llama2-13b-chat': {
                CFG_MOD_PATH_Q4_1: 'Llama2/llama-2-13b-chat/llama2-13b-chat-q4_1.gguf',
                CFG_MOD_PATH_Q5_1: 'Llama2/llama-2-13b-chat/llama2-13b-chat-q5_1.gguf',
                CFG_MOD_PATH_Q8_0: 'Llama2/llama-2-13b-chat/llama2-13b-chat-q8_0.gguf',
                CFG_MOD_DESC:      'LlaMA2 13b-chat',
                CFG_MOD_FMT:       'llama2',
                CFG_MOD_DEFAULT_Q: 'q8_0',
                CFG_MOD_CONTEXT_LEN: '1500',

            },
            'llama2-70b-chat': {
                CFG_MOD_PATH_Q4_1: 'Llama2/llama-2-70b-chat/llama2-70b-chat-q4_1.gguf',
                CFG_MOD_PATH_Q5_1: 'Llama2/llama-2-70b-chat/llama2-70b-chat-q5_1.gguf',
                CFG_MOD_PATH_Q8_0: 'Llama2/llama-2-70b-chat/llama2-70b-chat-q8_0.gguf',
                CFG_MOD_DESC:      'LlaMa2 70b-chat',
                CFG_MOD_FMT:       'llama2',
                CFG_MOD_DEFAULT_Q: 'q4_1'
            },
            'nous-13b':        {
                CFG_MOD_PATH_Q4_1: 'Llama2/Nous-Hermes-Llama2-13b/nous-hermes-llama2-13b.q4_1.gguf',
                CFG_MOD_PATH_Q8_0: 'Llama2/Nous-Hermes-Llama2-13b/nous-hermes-llama2-13b.q8_0.gguf',
                CFG_MOD_DESC:      'Nous-Hermes 13b',
                CFG_MOD_FMT:       'alpaca',
                CFG_MOD_DEFAULT_Q: 'q8_0'
            },
            'mistral-7b':      {
                CFG_MOD_PATH_Q4_1: 'Llama2/mistral-7B-v0.1/Llama2\mistral-7B-v0.1-q4_1.gguf',
                CFG_MOD_PATH_Q5_1: 'Llama2/mistral-7B-v0.1/Llama2\mistral-7B-v0.1-q5_1.gguf',
                CFG_MOD_PATH_Q8_0: 'Llama2/mistral-7B-v0.1/Llama2\mistral-7B-v0.1-q8_0.gguf',
                CFG_MOD_DESC:      'Mistral AI 13b',
                CFG_MOD_FMT:       'chatml',
                CFG_MOD_DEFAULT_Q: 'q8_0'
            }
        }

        for m in models:
            toplevel = CFG_MODELS + "." + m
            config[toplevel] = {}
            for n in models[m]:
                config[toplevel][n] = models[m][n]
            pass

        if values is None:
            values = DEFAULT_CONFIG_PATH

        dest = values

        os.makedirs(Path(dest).parent, exist_ok=True)

        with open(dest, 'w') as configfile:
            config.write(configfile)

        msg("Please add your models to the model library in {} by using the provided examples".format(dest))
        exit(0)


# we cant do this as an action
def list_installed_models():
    msg("--- Installed models: ---")
    for key in config:
        tokelen = len(CFG_MODELS) + 1
        if key[0:tokelen] == "{}.".format(CFG_MODELS):
            print("%25s - %60s" % (key[tokelen:], config[key][CFG_MOD_DESC]))
    exit(0)


########################
# Process cmdline args #
########################

# Parameters #

parser = ArgumentParser(description='A simple script for interacting with llama.cpp',
                        epilog="(C) 2023 Lyjia. Version {}. This script is licensed to you under the terms of the "
                               "GPLv3. Updates may be found at: https://github.com/lyjia/simple-llamacpp".format(
                            VERSION))

parser.add_argument("-m", "--model",
                    help="Model name from the model library, or path to model file")
parser.add_argument("-p", "--prompt",
                    help="The desired starting prompt text or a path to a text file containing your prompt")
parser.add_argument("-s", "--sysprompt",
                    help="The desired system prompt text or path to a text file containing your system prompt.")
parser.add_argument("-n", "--qtytokens",
                    help="The desired quantity of output tokens.",
                    default=DEFAULTS[CFG_DEF_QTYTOKES],
                    type=int)
parser.add_argument("-b", "--llamabin",
                    help="The path to the llama.cpp binary",
                    default=DEFAULTS[CFG_DEF_LLAMABIN])
parser.add_argument("-c", "--config",
                    help="Read config INI from specified path",
                    default=DEFAULT_CONFIG_PATH)
parser.add_argument('--gqa',
                    help="Specify value for GQA")
parser.add_argument('--prompt-format',
                    help="Specify prompt format (must refer to one of the formats listed in config.ini)")

# Actions #

parser.add_argument("-l", "--listmodels",
                    help="Print a list of available models, then exit.",
                    default=DEFAULT_CONFIG_PATH,
                    action='store_true')

parser.add_argument("--generate-default-config",
                    help="Generate a default configuration file for this script and write it to the path provided, "
                         "then exit. If no path is given, a new config file will be written to {}".format(
                        DEFAULT_CONFIG_PATH),
                    default=DEFAULT_CONFIG_PATH,
                    action=GenerateDefaultConfigAction,
                    metavar='CONFIG',
                    nargs='?')

args = parser.parse_args()

##############
# Validation #
##############

# config file
load_config(args)

if args.listmodels is True:
    list_installed_models()

# model file
model = args.model
modelhive = "{}.{}".format(CFG_MODELS, model)
if modelhive in config:
    model_hash = config[modelhive]
    model_path = os.path.join(os.path.expanduser(config[CFG_DEFAULT][CFG_DEF_MODELPATH]), model_hash[CFG_MOD_PATH])
    if os.path.exists(model_path):
        msg("Using model at {}".format(model_path))
    else:
        msg("ERROR: Model file at {} does not exist!".format(model_path))
        exit(-2)
else:
    if args.model is None:
        msg("ERROR: You must specify a model to use with -m.".format(model))
    else:
        msg("ERROR: Model {} does not exist in the model library!".format(model))
    exit(-3)

# prompt
if args.prompt:
    if os.path.exists(args.prompt):
        prompt_file = args.prompt
        with open(prompt_file, 'r') as f:
            prompt = f.read()
        msg("Loaded prompt from {}...".format(prompt_file))
    else:
        prompt = args.prompt
    msg("Using prompt of length {}.".format(len(prompt)))
else:
    msg("ERROR: you must specify a prompt or prompt file!")
    exit(-1)

# system prompt
if args.sysprompt:
    if os.path.exists(args.sysprompt):
        sysprompt_file = args.sysprompt
        with open(sysprompt_file, 'r') as f:
            sysprompt = f.read()
        msg("Loaded system prompt from {}...".format(sysprompt_file))
    else:
        sysprompt = args.sysprompt
    msg("Using system prompt of length {}.".format(len(sysprompt)))
else:
    sysprompt = None
    msg("No system prompt specified.")

#######
# Go! #
#######

# save the prompt to a temporary file to avoid issues with the shell misinterpreting special characters in the prompt string
with NamedTemporaryFile("w+b") as f:
    if sysprompt is not None:
        prompt_formatted = PROMPT_FORMATS[model_hash[CFG_MOD_FMT]].format(MAINPROMPT=prompt, SYSTEMPROMPT=sysprompt)
        f.write(str.encode(prompt_formatted))
    else:
        f.write(str.encode(prompt))
    f.flush()

    cmd_line = [os.path.expanduser(config[CFG_DEFAULT][CFG_DEF_LLAMABIN]), '-f', f.name]

    # note that we need to pass command line args and the parameters as separate list entries

    # get model var
    cmd_line.append("-m")
    cmd_line.append(model_path)

    # get GQA var
    gqa = None
    if CFG_MOD_GQA in model_hash:
        gqa = model_hash[CFG_MOD_GQA]
    if args.gqa:
        gqa = args.gqa

    if gqa:
        cmd_line.append("-gqa")
        cmd_line.append(gqa)

    # get qtytokens var
    if args.qtytokens:
        cmd_line.append("-n")
        cmd_line.append(str(args.qtytokens))

    msg(cmd_line)
    msg("========= {} is starting llama.cpp! =========".format(argv[0]))
    run(cmd_line)
    msg("========= {} is cleaning up... =========".format(argv[0]))
