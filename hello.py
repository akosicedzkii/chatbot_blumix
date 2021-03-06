import random
import json
from flask import Flask, request
from pymessenger.bot import Bot
import os
import requests
from watson_developer_cloud import DiscoveryV1
import re
import logging
from pprint import pprint
import string

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
            pprint(message)
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                                       
                    try:   
                        username = "cf386d90-3dce-4db9-9f35-94d51ea3b468"
                        password = "FSny6CcM1Wh5"
                        environment_id = "c0b065ea-e935-42ae-b062-becf297fff77"
                        collection_id = "fbd67673-766c-49ac-a210-904876f534be"

                        query = message['message']['text'].lower()
                        original_query = query
                        query = query.replace("who",query)
                        query = query.replace("what",query)
                        query = query.replace("when",query)
                        query = query.replace("how",query)
                        query = query.replace("who",query)

                        URL = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch="+ query +"&utf8=&format=json"


                        # sending get request and saving the response as response object
                        r = requests.get(url = URL)

                        # extracting data in json format
                        data = r.json()
                        response_sent_text = json.dumps(data, indent=2)
                        decoded = json.loads(response_sent_text)
                        pages = decoded["query"]["search"]
                        discovery = DiscoveryV1(
                            version="2017-11-07",
                            username= username,
                            password= password,
                            url='https://gateway.watsonplatform.net/discovery/api'
                        )
                        counter = 0
                        '''for page in pages:
                            pageid = page["pageid"]
                            URL = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&pageids=" + str(pageid)
                            r = requests.get(url = URL)
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
                            if counter == 1:
                                break
                            counter = counter + 1 

                        my_query = discovery.query(passages_characters=2000,environment_id=environment_id, collection_id=collection_id, natural_language_query=original_query,deduplicate=False,highlight=True,passages=True,passages_count=1)
                        returns =  str(my_query["passages"][0]["passage_text"].replace("SearchResult",""))
                        returns = returns.rsplit(".",1)[0]'''
                        returns = original_query
                    except:
                        try:
                            returns = "Do you mean: " + decoded["query"]["searchinfo"]["suggestion"]
                        except:
                            returns = "No results found for: " + query

                    send_message(recipient_id, returns)
                
            if message.get('postback'):
                requestss =  message["postback"]["payload"]
                recipient_id = message['sender']['id']
                send_button(recipient_id)
                #send_message(recipient_id, cleanhtml(requestss))
                
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

def send_button(recipient_id):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, 
        json = {
            "recipient":{
            "id": recipient_id
            },
            "message":{
            "text": "Here are the categories",
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":"Philippines",
                    "payload":"PHPLOAD",
                    "image_url":"http://example.com/img/red.png"
                },
                {
                    "content_type":"text",
                    "title":"Cebu",
                    "payload":"CHPLOAD",
                    "image_url":"http://example.com/img/red.png"
                },
                {
                    "content_type":"text",
                    "title":"Bohol",
                    "payload":"BHPLOAD",
                    "image_url":"http://example.com/img/red.png"
                },
                {
                    "content_type":"location"
                }
            ]
            }
                
            }
        )
    logging.info(r)
    return "hello"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)