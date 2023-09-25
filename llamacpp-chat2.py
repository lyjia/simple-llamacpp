#!/usr/bin/env python

###############################################################################
# Simple script for interactins with llama.cpp
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
import os

#############
# Constants #
#############
VERSION = "0.0"

CFG_DEFAULT = "defaults"
CFG_PROMPT_FORMATS = "prompt.formats"
CFG_MODELS = "models"

CFG_DEF_QTYTOKES = "qtytokens"
CFG_DEF_LLAMABIN = "llamabin"

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/simple-llamacpp/config.ini")

DEFAULTS = {
    CFG_DEF_LLAMABIN: '~/src/llama.cpp/main',
    CFG_DEF_QTYTOKES: 256
}

PROMPT_FORMATS = {
    'alpaca': '### Instruction:\n{MAINPROMPT}\n\n### Input: {SYSTEMPROMPT}\n\n### Reponse:\n',
    'llama2': '[INST]<<SYS>>{SYSTEMPROMPT}<</SYS>>{MAINPROMPT}[/INST]'
}

#################
# Initial setup #
#################
config = ConfigParser()

class GenerateDefaultConfigAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        global config
        config[CFG_DEFAULT] = DEFAULTS
        config[CFG_PROMPT_FORMATS] = PROMPT_FORMATS

        # some examples for specifying models
        models = {
            'llama2-13b-chat-q8':  {
                'path':         'llama-2-13b-chat/llama-2-13b-chat.ggmlv3.q8_0.bin',
                'desc':         'LlaMA2 13b-chat, q8_0',
                'promptformat': 'llama2'
            },
            'llama2-70b-chat-q41': {
                'path':         'llama-2-70b-chat/llama-2-70b-chat.ggmlv3.q4_1.bin',
                'desc':         'LlaMa2 70b-chat, q4_1 (gqa=8)',
                'promptformat': 'llama2',
                'gqa':          '8'
            },
            'nous-13b-q41':        {
                'path':         'Nous-Hermes-Llama2-13b/nous-hermes-llama2-13b.ggmlv3.q4_1.bin',
                'desc':         'Nous-Hermes 13b q4_1',
                'promptformat': 'alpaca'
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
        print("Generating default config and saving it to: {}".format(dest))

        os.makedirs(Path(dest).parent, exist_ok=True)

        with open(dest, 'w') as configfile:
            config.write(configfile)

        print("All done!")
        print("Please go to {} and add your models to the model library using the provided examples")
        exit(0)


class PrintListOfModelsAction(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        print("Hello!")
        exit(0)


########################
# Process cmdline args #
########################

# Parameters #

parser = ArgumentParser(description='A simple script for interacting with llama.cpp',
                        epilog="(C) 2023 Lyjia. Version {}. This script is licensed to you under the terms of the GPLv3. Updates may be found at: https://github.com/lyjia/simple-llamacpp".format(
                            VERSION))

parser.add_argument("-m", "--model",
                    help="Model name from the model library, or path to model file")
parser.add_argument("-p", "--prompt",
                    help="The desired starting prompt text or a path to a text file containing your prompt")
parser.add_argument("-s", "--sysprompt",
                    help="The desired system prompt text or path to a text file containing your system prompt.")
parser.add_argument("-n", "--qtytokens",
                    help="The disired quantity of output tokens.",
                    default=DEFAULTS[CFG_DEF_QTYTOKES],
                    type=int)
parser.add_argument("-b", "--llamabin",
                    help="The path to the llama.cpp binary",
                    default=DEFAULTS[CFG_DEF_LLAMABIN])
parser.add_argument("-c", "--config",
                    help="Read config INI from specified path",
                    default=DEFAULT_CONFIG_PATH)

# Actions #

parser.add_argument("-l", "--listmodels",
                    help="Print a list of available models, then exit.",
                    default=DEFAULT_CONFIG_PATH,
                    action=PrintListOfModelsAction,
                    nargs=0)

parser.add_argument("--generate-default-config",
                    help="Generate a default configuration file for this script and write it to the path provided, "
                         "then exit. If no path is given, a new config file will be written to {}".format(DEFAULT_CONFIG_PATH),
                    default=DEFAULT_CONFIG_PATH,
                    action=GenerateDefaultConfigAction,
                    metavar='CONFIG',
                    nargs='?')

args = parser.parse_args()

#######
# Go! #
#######

config_file = DEFAULT_CONFIG_PATH
if args.config is None:
    config_file = args.config

model = args.model

if os.exists(args.prompt):
