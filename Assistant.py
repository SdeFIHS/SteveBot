from llama_cpp import Llama 
import argostranslate.package
import argostranslate.translate
import pywhatkit
from datetime import date, datetime
import wikipedia
import subprocess
import speech_recognition as sr
import pyttsx3
import serial

#puerto de la izquierda

port = serial.Serial("COM6", 9600)

engine = pyttsx3.init()

wikipedia.set_lang("es")

es_code = "es"
en_code = "en"

def updateTranslator(from_code, to_code):
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())

updateTranslator(en_code, es_code)
updateTranslator(es_code, en_code)

def Translate(text: str, from_code: str, to_code: str):
    translatedText = argostranslate.translate.translate(text, from_code, to_code)
    return translatedText

"""
llm = Llama(model_path = "D:\\lodeinfo\\llama-2-7b.Q8_0.gguf",
             n_ctx=128, 
             n_batch=32)

def getResponse():
    input_es = input("texto: ")
    input_en = Translate(input_es, es_code, en_code)

    #system_message = "You are a helpful assistant"
    user_message = f"""
    #Q: {input_en}
#A: """
""" quitar esta lineaaa
    prompt = user_message

    output = llm(
    prompt,
     max_tokens=-1,
     stop=["A:"],
     echo=False
    )

    outputText_en = output['choices'][0]['text']
    outputText_es = Translate(outputText_en, en_code, es_code)

    return outputText_es
"""
    
def Say(text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def ReadCommand():
    command = input_text.lower()
    wordlist = input_text.split()
    if command.startswith("busca") and command.endswith("en google"):
        port.write(b'l')
        prompt = ' '.join(wordlist[1:-2])
        Say(f"Buscando \"{prompt}\" en Google")
        pywhatkit.search(prompt)
    elif command.startswith("pon") and command.endswith("en youtube"):
        port.write(b'l')
        prompt = ' '.join(wordlist[1:-2])
        Say(f"Reproduciendo \"{prompt}\" en Youtube")
        pywhatkit.playonyt(prompt)
    elif command.startswith("qué es") or command.startswith("quién es") or command.startswith("quién fue"):
        port.write(b'r')
        prompt = ' '.join(wordlist[2:])
        prompt = prompt[:-1]
        data = wikipedia.summary(prompt, sentences=1)
        Say(data)
    elif command == "qué día es hoy":
        port.write(b'f')
        today = date.today()
        month_en = today.strftime("%B")
        month_es = Translate(month_en, en_code, es_code)
        date_text = today.strftime(f"El día de hoy es %d de {month_es} del %Y")
        Say(date_text)
    elif "hora" in command:
        port.write(b'f')
        now = datetime.now()
        hour_str = now.strftime("%H")
        hour = int(hour_str)
        if (hour > 12):
            hour -= 12
            time_str = now.strftime(f"Actualmente son las {hour}:%M pm")
        else:
            time_str = now.strftime("Actualmente son las %H:%M am")
        Say(time_str)
    elif "calculadora" in command:
        port.write(b'u')
        Say("Abriendo calculadora")
        subprocess.Popen('C:\\Windows\\System32\\calc.exe')
    elif command == "levanta las manos":
        port.write(b'u')
    elif command == "hola steve":
        port.write(b'h')
        Say("Hola")
    elif command == "steve mina":
        port.write(b'U')
    elif command == "steve baila":
        port.write(b'u')
    #else:
        #port.write(b'r')
        #getResponse()



input_text = ""
while True:
    confirmation = input("enter")
    if confirmation == "no":
        exit()

    print("Escuchando...")
    try:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            audio = recognizer.listen(source)

        listenedAudio = recognizer.recognize_google(audio, language = 'ES')

    except:
        Say("No entendí jajajajaja")
        continue

    print(listenedAudio)
    input_text = listenedAudio
    ReadCommand()