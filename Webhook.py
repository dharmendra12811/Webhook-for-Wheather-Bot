# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:16:25 2019

@author: Dharmendra Singh
"""

import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

#Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)
    print(jso.dumps(req, indent=4))
    
    res = makeResponse(req)
    res = json.dumps(req, indent=4)
    r = make_response(res)
    r.harders['Content-Type']='application/json'
    return r

def makeResponse(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=b6907d289e10d714a6e88b30761fae22')
    json_object = r.json()
    wheather = json_object['list']
    for i in range(0,30):
        if date in wheather[i]['dt_txt']:
            condition = wheather[i]['weather'][0]['description']
            break
    
    speech = "The forcast for "+city+ " for "+date+ " is " + condition
    return {
    "speech": speech,
    "displayText":speech,
    "source": "apiai-wheather-webhook"
            }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
    