import os

dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, "system_prompt.txt")) as f:
    SYSTEM_PROMPT = f.read()