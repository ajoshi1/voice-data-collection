﻿from flask import render_template, redirect, url_for, request, session, flash
from ivr_phone_tree_python import app
import twilio.twiml
from ivr_phone_tree_python.view_helpers import twiml

prompts = {'six four' : '6 - 4',
           'five - seven' : '5 - 7',
           'threes' : '3 - 3',
           'Deuce' : 'Deuce',
           'Add in' : 'Add in'}

@app.route('/')
@app.route('/ivr')
def home():
    return render_template('index.html')


@app.route('/ivr/welcome', methods=['POST'])
def welcome():
    response = twilio.twiml.Response()
    with response.gather(numDigits=1, action=url_for('menu'), method="POST") as g:
        g.play(url="http://howtodocs.s3.amazonaws.com/et-phone.mp3", loop=3)
    return twiml(response)


@app.route('/ivr/menu', methods=['POST'])
def menu():
    selected_option = request.form['Digits']
    option_actions = {'1': _give_instructions,
                      '2': _list_planets}

    if option_actions.has_key(selected_option):
        response = twilio.twiml.Response()
        option_actions[selected_option](response)
        return twiml(response)

    return _redirect_welcome()


@app.route('/ivr/planets', methods=['POST'])
def planets():
    selected_option = request.form['Digits']
    option_actions = {'2': "+12024173378",
                      '3': "+12027336386",
                      "4": "+12027336637"}

    if option_actions.has_key(selected_option):
        response = twilio.twiml.Response()
        response.dial(option_actions[selected_option])
        return twiml(response)

    return _redirect_welcome()


@app.route('/ivr/pingpong', methods=['POST'])
def pingpong():
    resp = twilio.twiml.Response()
    resp.say("Speak six four")
    resp.record(maxLength="30", action='/handle-recording')
    return str(resp)

@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():
    """Play back the caller's recording."""

    recording_url = request.values.get("RecordingUrl", None)

    resp = twilio.twiml.Response()
    resp.say("Replaying...")
    resp.play(recording_url)
    return str(resp)

# private methods

def _give_instructions(response):
    response.say("To get to your extraction point, get on your bike and go down " +
                 "the street. Then Left down an alley. Avoid the police cars. Turn left " +
                 "into an unfinished housing development. Fly over the roadblock. Go " +
                 "passed the moon. Soon after you will see your mother ship.",
                 voice="alice", language="en-GB")

    response.say("Thank you for calling the ET Phone Home Service - the " +
                 "adventurous alien's first choice in intergalactic travel")

    response.hangup()
    return response


def _list_planets(response):
    with response.gather(numDigits=1, action=url_for('planets'), method="POST") as g:
        g.say("To call the planet Broh doe As O G, press 2. To call the planet " +
              "DuhGo bah, press 3. To call an oober asteroid to your location, press 4. To " +
              "go back to the main menu, press the star key ",
              voice="alice", language="en-GB", loop=3)

    return response


def _redirect_welcome():
    response = twilio.twiml.Response()
    response.say("Returning to the main menu", voice="alice", language="en-GB")
    response.redirect(url_for('welcome'))

    return twiml(response)
