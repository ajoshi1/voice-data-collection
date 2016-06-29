from flask import session, render_template, redirect, url_for, request, session, flash
from ivr_phone_tree_python import app
import twilio.twiml
from ivr_phone_tree_python.view_helpers import twiml
import time

prompts =   [('point seven','10 - 7'),
                ('nine ten','9 - 10'),
                ('one three','1 - 3'),
                ('Add In','Add In'),
                ('seven five','7 - 5'),
                ('eight six','8 - 6'),
                ('Add Out','Add Out'),
                ('Deuce','Deuce'),
                ('two four','2 - 4')
                ]

app.secret_key = 'fkP6Jc8zc1gz56PT7lvsc12aaibdBYG5'

@app.route('/')
@app.route('/ivr')
def home():
    return render_template('index.html')

@app.route('/ivr/pinit', methods=['POST'])
def pinit():
    resp = twilio.twiml.Response()
    print 'init prompts'

    initSessionCounter()

    resp.redirect(url_for('pingpong'))
    return str(resp)

@app.route('/ivr/pingpong', methods=['POST'])
def pingpong():
    #resp = None
    try:
        key, val = prompts[session['counter']]
        #resp = _prompt("six nine", "6 - 9")
        print(key)
        resp = _prompt(key, val)
    except:
        resp = twilio.twiml.Response()
        resp.say("Thank you for your time")
        session.clear()
        resp.hangup()
    return str(resp)

@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():
    """Handle the Recoring"""

    recording_url = request.values.get("RecordingUrl", None)
    key, val = prompts[session['counter']]

    app.logger.info("%s,%s,%s" % (key,val,recording_url))

    sumSessionCounter()

    resp = twilio.twiml.Response()
    resp.redirect(url_for('pingpong'))
    return str(resp)

# private methods
def _prompt(key, val):
    resp = twilio.twiml.Response()
    #for key, val in prompts.iteritems():
    resp.say("Please Speak " + key + "after the tone")
    resp.pause(length=1)
    resp.record(maxLength="3", action='/handle-recording')
    return resp

def initSessionCounter():
    session['counter'] = 0

def sumSessionCounter():
  try:
    session['counter'] += 1
  except KeyError:
    session['counter'] = 1
