import json 
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import os
from colr import color
import pyttsx3

ttsengine = pyttsx3.init()
#ttsenginevoices = ttsengine.getProperty('voices') #get voices
ttsengine.setProperty('voice', 'female2') #female voice
#ttsengine.say("I will speak this text")
#ttsengine.runAndWait()


import pyaudio
import speech_recognition as sr

import colorama 
colorama.init()
from colorama import Fore, Style, Back

import random
import pickle
r = sr.Recognizer()
with open("intents.json") as file:
    data = json.load(file)


def chat():
    # load trained model
    model = keras.models.load_model('chat_model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)
    inp = "Hello [this is default input]"
    # parameters
    max_len = 20
    
    while True:
        
        with sr.Microphone() as source:
            przejscie = 0
            inppassword = ""
            while przejscie != 1:
                audio_data = r.record(source, duration=3)
                try:
                    print("Computing pass")
                    inppassword = r.recognize_google(audio_data)
                    
                    if "COMPUTER" in inppassword.upper():
                        przejscie = 1
                        #os.system("espeak -v female2 'Yes?'")
                        ttsengine.say("Yes?")
                        ttsengine.runAndWait()
                except:
                    print("Pass failed, word " +inppassword)
                    

                
            inputslowotekstdwa = str(color("Listening for 5 seconds...", fore=(255, 20, 147)))

            audio_data = r.record(source, duration=5)
            if audio_data:
                print(color("Computing audio recording...", fore=(255, 20, 147)))
                try:
                    inp = r.recognize_google(audio_data)
                except:
                    print(color("ERROR, using last input", fore=(255, 0, 0)))
            print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end=inp+"\n")


        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        for i in data['intents']:
            if i['tag'] == tag:
                odpowiedz = np.random.choice(i['responses'])
                print(Fore.GREEN + "IRIS:" + Style.RESET_ALL , odpowiedz[1:])
                odpowiedz = odpowiedz.replace("'","")
                ttsengine.say(odpowiedz[1:])
                ttsengine.runAndWait()
                #os.system("espeak -v female2 '" + str(odpowiedz[1:])+"'")
                if odpowiedz[0]=="0":
                    try:
                        os.system("google-chrome")
                        os.system("start chrome")
                    except:
                        os.system("start chrome")
                if odpowiedz[0]=="1":
                    try:
                        os.system("google-chrome birdtech.weebly.com")
                        os.system("start chrome birdtech.weebly.com")
                    except:
                        os.system("start chrome birdtech.weebly.com")
                inp = "Hello [this is default input]"
                    
                
                
                

        # print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,random.choice(responses))

print(Fore.YELLOW + "Start messaging with the bot. Say computer to call" + Style.RESET_ALL)
chat()
