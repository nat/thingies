#!/usr/bin/env python3
#
# A script to clean up copy-pastes from slack using GPT-4
#

import pasteboard
import openai
import sys
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
pb = pasteboard.Pasteboard()

import Quartz
from pynput import keyboard

# cmd-shift-p
COMBINATION = {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode.from_char('p')}
current_keys = set()

def on_key_down(key):
    if any([key in COMBINATION, key in current_keys]):
        current_keys.add(key)
        if all(k in current_keys for k in COMBINATION):
            perform_action()

def on_key_up(key):
    if key in current_keys:
        current_keys.remove(key)

def perform_action():
    print("Hotkey pressed!")
    str = pb.get_contents(diff=True)
    prompt = f'Clean up this copy-paste from Slack and make it suitable for pasting into Notion as meeting notes:\n\n {str}\n'

    suggestion = ""
    for chunk in openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stream=True):
        sys.stdout.write(chunk.choices[0].text)
        suggestion += chunk.choices[0].text
        # flush stdout
        sys.stdout.flush()
    sys.stdout.write('\n')

# Using pynput to capture key events
with keyboard.Listener(on_press=on_key_down, on_release=on_key_up) as listener:
    listener.join()
