# Болталка с openai
# author: Vladislav Janvarev

import os
import openai

from vacore import VACore

modname = os.path.basename(__file__)[:-3] # calculating modname

# функция на старте
def start(core:VACore):
    manifest = {
        "name": "Болталка с OpenAI",
        "version": "1.0",
        "require_online": True,

        "default_options": {
            "apiKey": "", #
        },

        "commands": {
            "поболтаем|поговорим": run_start,
        }
    }
    return manifest

def start_with_options(core:VACore, manifest:dict):
    pass

def run_start(core:VACore, phrase:str):

    options = core.plugin_options(modname)

    if options["apiKey"] == "":
        core.play_voice_assistant_speech("Нужен ключ апи для доступа к опенаи")
        return

    openai.api_key = options["apiKey"]

    if phrase == "":
        core.play_voice_assistant_speech("Да, давай!")
        core.context_set(boltalka)
    else:
        boltalka(core,phrase)

def generate_response(prompt):
    response= openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    #print(response) # debug
    return response["choices"][0]["text"]

def boltalka(core:VACore, phrase:str):
    if phrase == "отмена" or phrase == "пока":
        core.play_voice_assistant_speech("Пока!")
        return

    try:
        response = generate_response(phrase)
        core.say(response)
        core.context_set(boltalka)

    except:
        import traceback
        traceback.print_exc()
        core.play_voice_assistant_speech("Проблемы с доступом к апи. Посмотрите логи")

        return
