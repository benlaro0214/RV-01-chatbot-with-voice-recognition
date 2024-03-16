import speech_recognition as sr
import pyttsx3
import subprocess
import json

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except Exception as e:
        print(e)
        return None

def execute_command(command):
    try:
        result = subprocess.check_output(command, shell=True)
        return_code = 0
    except subprocess.CalledProcessError as e:
        result = "Error: {}".format(e)
        return_code = e.returncode

    return result.strip().decode(), return_code


def chatbot(text, rules):
    for rule in rules:
        try:
            rule_type = rule["type"]
        except KeyError:
            rule_type = None

        if rule["pattern"] in text.lower():
            if rule_type == "cmd":
                if ":" in rule["response"]:
                    command = rule["response"].split(":")[1].strip()
                    print("Chatbot: Running command '{}'...".format(command))
                    result, return_code = execute_command(command)
                    print("Chatbot: {}".format(result))
                    if return_code == 0:
                        response = result
                    else:
                        response = "Error running command: {}".format(result)
                else:
                    response = rule["response"]
            else:
                response = rule["response"]
            break
    else:
        response = "I'm sorry, I don't understand. Can you please rephrase?"

    return response.strip()  # Ensure response is stripped of leading/trailing whitespace

def main():
    engine = pyttsx3.init()
    with open("rules2a.json") as f:
        rules = json.load(f)

    while True:
        text = recognize_speech()
        if text:
            if text.lower() == "deactivate":
                print("Deactivating program...")
                break
            response = chatbot(text, rules)
            if response:  # Check if response is non-empty before saying
                engine.say(response)
                engine.runAndWait()

    engine.stop()  # Stop the text-to-speech engine after use

if __name__ == "__main__":
    main()

