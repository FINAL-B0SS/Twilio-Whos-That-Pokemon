from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
import random

# Your Account SID from twilio.com/console
account_sid = os.environ.get('twilio_sid')
# Your Auth Token from twilio.com/console
auth_token  = os.environ.get('twilio_token')

client = Client(account_sid, auth_token)
app = Flask(__name__)

# q stores the urls to the pokemon silhuettes, a stores the urls to the reveal images
pokemon_q = {
    "chancey":"https://i.imgur.com/pRmtAN4.png",    
    "shelmet":"https://i.imgur.com/zvvT3Vb.png",
    "klinklang":"https://i.imgur.com/8YTfb2H.png",
    "oranguru":"https://i.imgur.com/4f0DvxK.png",
    "croagunk":"https://i.imgur.com/yzOjhI0.png",
    "noivern":"https://i.imgur.com/LPx29ra.png",
    "crabominable":"https://i.imgur.com/LgP2M1Q.png"
}

pokemon_a = {
    "chancey":"https://i.imgur.com/lcKPGWM.png",
    "shelmet":"https://i.imgur.com/E0qzGAq.png",
    "klinklang":"https://i.imgur.com/wsNYVCp.png",
    "oranguru":"https://i.imgur.com/TO5Zpo8.png",
    "croagunk":"https://i.imgur.com/g83t16H.png",
    "noivern":"https://i.imgur.com/8pmCkuj.png",
    "crabominable":"https://i.imgur.com/VMQFPe3.png"
}

# Picks a random pokemon
def new_pokemon():
    global pokemon
    global url
    pokemon = random.choice(pokemon_q.keys())
    url = pokemon_a[pokemon]

# Send the question and image
def send_pokemon():
    global pokemon
    global url
    message = client.messages.create(
        to=os.environ.get('my_phone'),
        from_=os.environ.get('twilio_phone'),
        body="Who's that Pokemon?",
        media_url=pokemon_q[pokemon]
        )
    print(message.sid)

new_pokemon()
send_pokemon()

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    global pokemon
    global url
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    # Start a TwiML response
    resp = MessagingResponse()
    # Determine the right reply for this message
    if body.lower() == pokemon:
        msg = resp.message("Nice Moves!")
        msg.media(url)
    elif body.lower() == "another":
        new_pokemon()
        send_pokemon()
    else:
        msg = resp.message("It's " + pokemon)
        msg.media(url)
    return str(resp)

if __name__ == "__main__":
    app.run(use_reloader=False)