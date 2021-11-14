import os
import json
from flask import Flask, request
import requests


app = Flask(__name__)

SERVERLESS_STAGE = os.environ['SERVERLESS_STAGE'];
TEAMS_URL = os.environ['TEAMS_URL'];
APIKEY = os.environ['APIKEY'];


def send_teams_message(title, summary, text):

    ''' Create the mapping to convert to json containing the teams message '''
    tdata = {}
    tdata['@context'] = "http://schema.org/extensions"
    tdata['@type'] = "MessageCard"
    tdata['themeColor'] = "00FF00"
    tdata['title'] = title
    tdata['summary'] = summary
    tdata['text'] = text

    ''' Send a teams formated dict to a teams channel '''
    response = requests.post(
        TEAMS_URL, data=json.dumps(tdata),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to Teams returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )


@app.route("/", methods=["POST"])
def event():

    apikey = request.headers.get('X-API-Key');
    if not apikey == APIKEY:
        resp = app.response_class(
            response=json.dumps("unauthorised"),
            status=403,
            mimetype='application/json'
            )
        return resp
    print(request.json)

    posted = request.json
    data = posted['data']

    if 'user_login' in data:
        send_teams_message('Wordpress User Login', 'Wordpress User Login', 'Login by {} user:{} ID:{}) '.format(data['display_name'], data['user_login'], data['ID']))
    else:
        print("Unhandled Data:\n{}".format(data))

    resp = app.response_class(
        response=json.dumps('{"Result": "got it"}'),
        status=200,
        mimetype='application/json'
    )
    return resp