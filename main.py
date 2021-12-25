from keyboard import write, press_and_release, read_key, wait
from time import sleep
from random import choice
from json import load
from playsound import playsound
from os import listdir


tmp = []
used = []
retry = 0
expression = ""
key = ""


def initialize():
    with open("./config/words.txt", "r") as f:
        w = f.read().split("\n")

    with open("./config/config.json", "r") as f:
        config = load(f)

        class conf:
            e = str(config["escape_key"])
            c = str(config["confirm_key"])
            try:
                sfx = bool(config["sfx"])
            except ValueError:
                sfx = False
                print("SFX value is not set to 'true' or 'false', defaulting to 'false'")

    return w, check_config(conf)


def check_config(config: dict):
    if len(config.e) > 1:
        config.e = config.e[0]
        print(f"Failsafe key is more than one character, only using the first character ({config.e})")
    elif len(config.e) < 1:
        config.e = "-"
        print("Failsafe key isn't set, using '-'")

    if len(config.c) > 1:
        config.c = config.c[0]
        print(f"Confirm key is more than one character, only using the first character ({config.c})")
    elif len(config.c) < 1:
        config.c = "/"
        print("Confirm key isn't set, using '/'")

    return config


words, config = initialize()

print("Initialised...")

while True:
    wait(config.e)
    press_and_release("backspace")
    if config.sfx:
        playsound("./sound/start.mp3", False)
    sleep(0.5)

    while key != config.c:
        key = read_key()
        expression += read_key()
        sleep(0.1)

    for _ in expression:
        press_and_release("backspace")

    expression = expression[:-1]
    key = ""

    if config.sfx:
        playsound("./sound/confirm.mp3", False)

    for word in words:
        if expression in word and word not in used:
            tmp.append(word)

    while key != config.c:
        try:
            rnd = choice(tmp)
            tmp.remove(rnd)
            write(rnd)
            used.append(rnd)
            if config.sfx:
                playsound(f"./sound/send/{choice(listdir(r'./sound/send/'))}", False)
        except IndexError:
            print(f"No more words with the letters '{expression}'")
            break

        press_and_release("enter")
        retry += 1
        sleep(0.5)

        key = read_key()
        press_and_release("backspace")

    retry = 0
    expression = ""
    tmp = []
    key = ""

    if config.sfx:
        playsound("./sound/finish.mp3", False)
