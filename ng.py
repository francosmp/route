import os
import requests
import threading
import json
import time
import datetime

def ng_rok():
    os.system("sudo /bin/ngrok http 80")

tNgrok = threading.Thread(target=ng_rok)
tNgrok.start()

time.sleep(5)

os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")

with open('tunnels.json') as data_file:
    datajson = json.load(data_file)

ngrok = datajson['tunnels'][1]['public_url']

while 1:
    time.sleep(1)

    status = 0

    urlReact = 'http://434b5214.ngrok.io/inf-sec-java-ser/java/check'

    headers = {'Content-Type': 'application/json'}
    urlEspejo = 'http://espejo.ngrok.io/inf-sec-php-ser/servicios-php.php'
    dataEspejo = {"crud": "read", "index": "1", "codigo": "blanca"}
    params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}

    try:
        response = requests.post(urlEspejo, params=params, data=json.dumps(dataEspejo), headers=headers)
        status = 200
    except requests.exceptions.RequestException as e:
        status = 404

    if status == 200 and response.status_code != 502 and response.status_code != 404:# Enviar post al servidor donde se encuentre el react e indicar el nuevo copia es el otro

        print("Prendido")
        print(datetime.datetime.now())

    if status == 404 or response.status_code == 502 or response.status_code == 404:# Enviar post al servidor donde se encuentre el react e indicar el nuevo root es este

        dataReact = {"url": ngrok + "/inf-sec-php-ser/servicios-php.php"}

        try:
            response = requests.post(urlReact, params=params, data=json.dumps(dataReact), headers=headers)
        except requests.exceptions.RequestException as e:
            print("Ya valió verga")

        print("Apagado")
        print(datetime.datetime.now())
