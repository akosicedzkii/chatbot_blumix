import random
import json
from flask import Flask, request
from pymessenger.bot import Bot
import os
from watson_developer_cloud import DiscoveryV1
import requests

app = Flask(__name__)
port = int(os.getenv('PORT', 8000))
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
         # api-endpoint
        URL = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=who is duterte&utf8=&format=json"


        # sending get request and saving the response as response object
        r = requests.get(url = URL)

        # extracting data in json format
        data = r.json()
        response_sent_text = json.dumps(data, indent=2)
        decoded = json.loads(response_sent_text)
        pageid = decoded["query"]["search"][0]["pageid"]
        
        URL = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&pageids=" + str(pageid)


        # sending get request and saving the response as response object
        r = requests.get(url = URL)

        # extracting data in json format
        data = r.json()
        response_sent_text = json.dumps(data, indent=2)
        decoded = json.loads(response_sent_text)
        requestss = decoded["query"]["pages"][str(pageid)]["extract"].split(".")

        return requestss[0] + "."
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        return "Message Processed POST"

port = int(os.getenv('PORT', 8000))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)