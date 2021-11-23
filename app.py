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
        key_to_encrypt = req['queryResult']['parameters'].get('number-integer')

        
        ## Get a specific translation and get a response
        output = encrypt_text(text_to_encrypt, key_to_encrypt)
    
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

def indice(lettre) :
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    if lettre in alphabet : 
        rang=alphabet.index(lettre)
        return rang
    else :
        return -1

def encrypt_text(text, key):
    key=int(key)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    n=len (alphabet)
    l=len(text)
    phrase2=""
    for i in range(0,l) :
        ind=indice(text[i])
        if ind==-1 :
            phrase2=phrase2+text[i]
        else :
            phrase2=phrase2+alphabet[(ind+key)%n]+' '
    return phrase2
	
"""def indice(lettre) :
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789&é(-è_çà)=~'#{[|\^@]}$*ù!:;,?./%"
    if lettre in alphabet : 
        rang=alphabet.index(lettre)
        return rang
    else :
        return -1

def encrypt_text(text, key):
    key=int(key)
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789&é(-è_çà)=~'#{[|\^@]}$*ù!:;,?./%"
    #text=text.lower()
    n=len (alphabet)
    l=len(text)
    phrase2=""
	phrase_crypt_final=""
    for i in range(0,l) :
        ind=indice(text[i])
        if ind==-1 :
            phrase2=phrase2+text[i]
        else :
            phrase2=phrase2+alphabet[(ind+key)%n]
	for j in range (len(phrase2)) :
		phrase_crypt_final = phrase_crypt_final+phrase2[j]+' '
    return phrase_crypt_final"""


if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
