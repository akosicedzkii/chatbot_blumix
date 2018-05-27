import random
import json
from flask import Flask, request
from pymessenger.bot import Bot
import os
from watson_developer_cloud import DiscoveryV1
import requests
import string


app = Flask(__name__)
port = int(os.getenv('PORT', 8000))
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
         # api-endpoint
        URL = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=the fifth president of the philippines&utf8=&format=json"


        # sending get request and saving the response as response object
        r = requests.get(url = URL)

        # extracting data in json format
        data = r.json()
        response_sent_text = json.dumps(data, indent=2)
        decoded = json.loads(response_sent_text)
        pages = decoded["query"]["search"]
        for page in pages:
            pageid = page["pageid"]
            
            URL = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&pageids=" + str(pageid)


            # sending get request and saving the response as response object
            r = requests.get(url = URL)
                    
            username = "cf386d90-3dce-4db9-9f35-94d51ea3b468"
            password = "FSny6CcM1Wh5"
            environment_id = "c0b065ea-e935-42ae-b062-becf297fff77"
            collection_id = "ff9c8eb9-024a-4e0a-a96c-8fe4284e03e1"
            
            discovery = DiscoveryV1(
                version="2017-11-07",
                username= username,
                password= password,
                url='https://gateway.watsonplatform.net/discovery/api'
            )
            # extracting data in json format
            data = r.json()
            response_sent_text = json.dumps(data, indent=2)
            decoded = json.loads(response_sent_text)
            requestss = decoded["query"]["pages"][str(pageid)]["extract"]
            f = open( 'demo.html','w')
            printable = set(string.printable)
            printable = filter(lambda x: x in printable, requestss)
            message = "<html><head><title>SearchResult<title></head><body><p>"+ printable +"</p></body></html>"

            f.write(message)
            f.close()
            with open(os.path.join(os.getcwd(), '', 'demo.html')) as fileinfo:
                add_doc = discovery.add_document(environment_id, collection_id, file=fileinfo)

        #requestss = decoded["query"]["pages"][str(pageid)]["extract"].split(".")
        query = "who is the fifth president of the philippines"
        my_query = discovery.query(passages_characters=2000,environment_id=environment_id, collection_id=collection_id, natural_language_query=query,deduplicate=False,highlight=True,passages=True,passages_count=1)
        returns =  str(my_query["passages"][0]["passage_text"].replace("SearchResult",""))
        returns = returns.rsplit(".",1)[0]
        return returns
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        return "Message Processed POST"

port = int(os.getenv('PORT', 8000))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)