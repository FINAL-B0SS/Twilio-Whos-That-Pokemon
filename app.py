from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from subprocess import call
import sys

pokemon = sys.argv[1]
pokemon_img = sys.argv[2]

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])

def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start a TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body.lower() == pokemon:
        msg = resp.message("Nice Moves!")
        msg.media(pokemon_img)
    # Restarts the game with a new pokemon
    elif body.lower() == "another":
        call(["python", "pokemon.py"])
    else:
        msg = resp.message("It's " + pokemon)
        msg.media(pokemon_img)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)