#!/usr/bin/env python

import curses
import argparse
from configparser import ConfigParser

### Constants ###
VERSION="0.0"

CFG_DEFAULT = "Defaults"
CFG_PROMPT_FORMATS = "Prompt Formats"

CFG_DEF_QTYTOKES = "qtytokens"
CFG_DEF_LLAMABIN = "llamabin"

### Initial setup ###
config = ConfigParser()
config[CFG_DEFAULT] = {
    CFG_DEF_LLAMABIN: '~/src/llama.cpp/main',
    CFG_DEF_QTYTOKES: 256
}
config[CFG_PROMPT_FORMATS] = {
    'alpaca': '### Instruction:\n{MAINPROMPT}\n\n### Input: {SYSTEMPROMPT}\n\n### Reponse:\n',
    'llama2': '[INST]<<SYS>>{SYSTEMPROMPT}<</SYS>>{MAINPROMPT}[/INST]'
}

### Process cmdline args
parser = argparse.ArgumentParser(description='A simple script for interacting with llama.cpp. Version {}'.format(VERSION))
parser.add_argument("-m", "--model", help="Model name from the model library, or path to model file", required=True)
parser.add_argument("-p", "--prompt", help="The desired starting prompt text or a path to a text file containing your prompt")
parser.add_argument("-s", "--sysprompt", help="The desired system prompt text or path to a text file containing your system prompt.")
parser.add_argument("-n", "--qtytokens", help="The disired quantity of output tokens.", default=config[CFG_DEFAULT][CFG_DEF_QTYTOKES], type=int)
parser.add_argument("-b", "--llamabin", help="The path to the llama.cpp binary", default=config[CFG_DEFAULT][CFG_DEF_LLAMABIN], required=True)
parser.add_argument("--generate-default-config", help="Generate a default configuration file for this script and place it in the path provided", type=argparse.FileType('w'))

args = parser.parse_args()
