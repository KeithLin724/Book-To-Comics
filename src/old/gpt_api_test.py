import g4f
import json
from pprint import pformat
from g4f.api import run_api

g4f.logging = True  # enable logging
g4f.check_version = False  # Disable automatic version checking
print(g4f.version)  # check version
print(g4f.Provider.Ails.params)  # supported args

# Automatic selection of provider

# streamed completion
# response = g4f.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "user",
#                "content": "Write a short story along with a list of prompts for image generation in a json format like {\"story\":... , \"prompt\": ......}",
#                }],
#     stream=True,
# )

# for message in response:
#     print(message, flush=True, end='')

# normal response
response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    messages=[
        {
            "role": "user",
            "content": 'Write a short story only 150 words along with a list of prompts for image generation in a json format like {"story":... , "prompt": ["...." , "....",...]} , just reply the json only',
        }
    ],
)  # alterative model setting

response = response[response.index("{") : response.index("}") + 1]

response = json.loads(response)

print(pformat(response), type(response))


print(response["prompt"])
