import re
import os
import requests
import threading
import json
import time


def restore():
    os.system("mysql -u root --password="" test < C:\\xampp\\htdocs\\test")


def ng_rok():
    os.system("ngrok http 80")


def xampp():
    os.system("C:\\xampp\\xampp_start.exe")


tXampp = threading.Thread(target=xampp)
tXampp.start()

time.sleep(10)

tNgrok = threading.Thread(target=ng_rok)
tNgrok.start()

time.sleep(10)

os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")

with open('tunnels.json') as data_file:
    datajson = json.load(data_file)

ngrok = datajson['tunnels'][1]['public_url']

headers = {'Content-Type': 'application/json'}
params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}

# Back Up

urlReact = 'http://f145d809.ngrok.io/inf-sec-java-ser/java/check'
dataReactStartup = {"url": "" + ngrok + "/inf-sec-php-ser/servicios-php.php", "config": "startup"}

try:
    responseStartUp = requests.post(urlReact, params=params, data=json.dumps(dataReactStartup), headers=headers)
    urlLastBackUp = responseStartUp.json()['url']
except requests.exceptions.RequestException as e:
    print("React Apagado")

urlLastBackUp = urlLastBackUp.replace('servicios-php.php', 'enviar.php')
dataReactStartup = {"url": "" + ngrok + "/inf-sec-php-ser/recibir.php"}

try:
    responseStartUp = requests.post(urlLastBackUp, params=params, data=json.dumps(dataReactStartup), headers=headers)
except requests.exceptions.RequestException as e:
    print("No Backup")

time.sleep(5)

tRestore = threading.Thread(target=restore)
tRestore.start()

while 1:
    time.sleep(10)
    print("NGROK: " + ngrok + "/inf-sec-php-ser/servicios-php.php")
    dataReact = {"url": "" + ngrok + "/inf-sec-php-ser/servicios-php.php", "config": ""}

    try:
        response = requests.post(urlReact, params=params, data=json.dumps(dataReact), headers=headers)
        urlEspejo = response.json()['url']
        print("ESPEJO: " + urlEspejo)
    except requests.exceptions.RequestException as e:
        print("React Apagado")

    file1 = open('C:\\xampp\\htdocs\\inf-sec-php-ser\\servicios-php.php', 'r')
    data = file1.read()
    file1.close()

    m = re.search('[$]espejo = "(.*?)";', data)

    if m:
        urlPhp = m.group(0)

    if urlEspejo != "http://mirror.ngrok.io/inf-sec-php-ser/servicios-php.php":
        cambio = '$espejo = "' + urlEspejo + '";'
        if urlPhp != cambio:
            data = data.replace(urlPhp, cambio)
            file2 = open('C:\\xampp\\htdocs\\inf-sec-php-ser\\servicios-php.php', "w+")
            file2.write(data)
            file2.close()
    else:
        cambio = '$espejo = "";'
        if urlPhp != cambio:
            data = data.replace(urlPhp, cambio)
            file2 = open('C:\\xampp\\htdocs\\inf-sec-php-ser\\servicios-php.php', "w+")
            file2.write(data)
            file2.close()
