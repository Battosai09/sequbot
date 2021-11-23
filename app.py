import os, json, random
from flask import Flask, jsonify, make_response, request
from http.client import HTTPException
from urllib.error import HTTPError, URLError

app = Flask(__name__)
log = app.logger

@app.route('/')
def hello_world():
    target = os.environ.get('TARGET', 'EPSI Workshop')
    return 'Welcome to {}!\n'.format(target)


@app.route('/webhook', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook

    """
    
    # Get request parameters
    req = request.get_json(force=True)
    output = ""
    print(req)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'
    
    try:
        user_lang = req.get('queryResult').get('languageCode')
    except AttributeError:
        return 'json error'        
    
          
    
    ## Check if the request is for translation of the patient response
    if action == 'encrypt.text':
        query = req['queryResult']['parameters'].get('any')
        text_to_encrypt = req['queryResult']['parameters'].get('phrase_a_chiffrer')
        key_to_encrypt = req['queryResult']['parameters'].get('key')

        
        ## Get a specific translation and get a response
        output = encrypt_text(text, key)
    
        ## Compose the response to Dialogflow
        res = {'fulfillmentText': output,
               'outputContexts': req['queryResult']['outputContexts']}
        
   
    elif action == 'input.unknown' :
        output = "remplire ce que va dire le robot dans ce cas"
            
        ## Compose the response to Dialogflow
        res = {'fulfillmentText': output,
               'outputContexts': req['queryResult']['outputContexts']}
            

    else:
        # If the request is not to the encrypt.text action throw an error
        log.error('Unexpected action requested: %s', json.dumps(req))
        res = {
                'speech': 'error', 'displayText': 'error',
                'action': action, 'user_lang': user_lang,
                'req': str(req), 'output':output,
                'outputContexts': req['queryResult']['outputContexts']
              }


    return make_response(jsonify(res))

def encrypt_text(text, key):
    """returns encrypted text 
ALGO DE CRYPTAGE A DEVELOPPER

    """
    reponse = "REPONSE DU CRYPTAGE"
        
        
    return reponse.replace('&#39;', "'")




if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
