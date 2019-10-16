import re
import os
import requests
import threading
import json
import time


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

while 1:
    time.sleep(10)
    print("NGROK: " + ngrok + "/inf-sec-php-ser/servicios-php.php")
    urlReact = 'http://f145d809.ngrok.io/inf-sec-java-ser/java/check'
    dataReact = {"url": "" + ngrok + "/inf-sec-php-ser/servicios-php.php"}

    headers = {'Content-Type': 'application/json'}
    params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}

    try:
        response = requests.post(urlReact, params=params, data=json.dumps(dataReact), headers=headers)
        urlEspejo = response.json()['url']
        print("ESPEJO: " + urlEspejo)
    except requests.exceptions.RequestException as e:
        print("React Apagado")

    with open('C:\\xampp\\htdocs\\inf-sec-php-ser\\servicios-php.php', 'r') as file:
        data = file.read()

    m = re.search('[$]espejo = "(.*?)";', data)

    if m:
        urlPhp = m.group(0)

    if urlEspejo != "http://mirror.ngrok.io/inf-sec-php-ser/servicios-php.php":
        data = data.replace(urlPhp, '$espejo = "' + urlEspejo + '";')
    else:
        data = data.replace(urlPhp, '$espejo = "";')

    #f = open("C:\\xampp\\htdocs\\inf-sec-php-ser\\servicios-php.php", "w+")
    #f.write(data)
