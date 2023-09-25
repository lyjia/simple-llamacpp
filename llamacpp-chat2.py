#!/usr/bin/env python

import curses
import argparse

### Initial setup

PROMPT_FORMATS = {

        }

### Process cmdline args
parser = argparse.ArgumentParser(description='A simple script for interacting with llama.cpp')
parser.add_argument("-m", "--model", help="Model name from the model library, or path to model file", required=True)
parser.add_argument("-p", "--prompt", help="The desired starting prompt text or a path to a text file containing your prompt")
parser.add_argument("-s", "--sysprompt", help="The desired system prompt text or path to a text file containing your system prompt.")
parser.add_argument("-n", "--numtokens", help="The disired quantity of output tokens.", default=256, type=int)

args = parser.parse_args()
