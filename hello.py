import random
import json
from flask import Flask, request
from pymessenger.bot import Bot
import os
import requests
from watson_developer_cloud import DiscoveryV1
import re


app = Flask(__name__)
ACCESS_TOKEN = 'EAAJ4pZA9Krr0BAL8ZBLqGHQmHly9Jo819w3y0c5llpLeZCihEKx2PqCg7crsfyInAaa61V74JZAp8XjVWac4ahhnu1CZBTM5oEJZB3lygOAb6r7WMshqGe7zz402DdjrFro820zHzYWmJtnyn3PMTnc91uRx518SUJ1lIfZAXtZALDihvNBDmyON'
VERIFY_TOKEN = 'demos2'
bot = Bot(ACCESS_TOKEN)
port = int(os.getenv('PORT', 8000))
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                                       
                    username = "acf386d90-3dce-4db9-9f35-94d51ea3b468"
                    password = "FSny6CcM1Wh5"
                    environment_id = "c0b065ea-e935-42ae-b062-becf297fff77"
                    collection_id = "174f2206-16f6-4cee-93a4-028adaa0291f"
                    query = message['message']['text']

                 

                  
                    try:
                        discovery = DiscoveryV1(
                            version="2017-11-07",
                            username= username,
                            password= password,
                            url='https://gateway.watsonplatform.net/discovery/api'
                        )
                        my_query = discovery.query(environment_id=environment_id, collection_id=collection_id, query=query,deduplicate=False,highlight=True,passages=True,passages_count=1)
                        #print(json.dumps(my_query, indent=2))
                        response_sent_text = json.dumps(my_query, indent=2)
                        decoded = json.loads(response_sent_text)
                        #print(json.dumps(my_query, indent=2))
                        requestss = decoded["passages"][0]["passage_text"]
                    except:

                         # api-endpoint
                        URL = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch="+ query +"&utf8=&format=json"


                        # sending get request and saving the response as response object
                        r = requests.get(url = URL)

                        # extracting data in json format
                        data = r.json()
                        response_sent_text = json.dumps(data, indent=2)
                        decoded = json.loads(response_sent_text)
                        
                        try:
                            pageid = decoded["query"]["search"][0]["pageid"]
                            
                            URL = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&pageids=" + str(pageid)


                            # sending get request and saving the response as response object
                            r = requests.get(url = URL)

                            # extracting data in json format
                            data = r.json()
                            response_sent_text = json.dumps(data, indent=2)
                            decoded = json.loads(response_sent_text)
                            requestss = decoded["query"]["pages"][str(pageid)]["extract"].split(".")

                            try:
                                 requestss = requestss[0] + "." + requestss[1] + "." + requestss[2] + "."
                            except:
                                try:
                                    requestss = requestss[0] + "." + requestss[1] + "."
                                except:
                                    requestss = requestss[0] + "."
                        except:
                            try:
                                requestss = "Do you mean: " + decoded["query"]["searchinfo"]["suggestion"]
                            except:
                                requestss = "No results found for: " + query
                  
                    send_message(recipient_id, cleanhtml(requestss))

    return "Message Processed"

port = int(os.getenv('PORT', 8000))
def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
  
#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)