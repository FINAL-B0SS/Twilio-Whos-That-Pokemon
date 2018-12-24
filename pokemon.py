from twilio.rest import Client
import random
from subprocess import call
import os

# Your Account SID from twilio.com/console
account_sid = os.environ.get('twilio_sid')
# Your Auth Token from twilio.com/console
auth_token  = os.environ.get('twilio_token')

client = Client(account_sid, auth_token)

# q stores the urls to the pokemon silhuettes, a stores the urls to the reveal images
pokemon_q = {
    "chancey":"https://i.imgur.com/pRmtAN4.png",    
    "shelmet":"https://i.imgur.com/zvvT3Vb.png",
    "KlinKlang":"https://i.imgur.com/8YTfb2H.png",
}

pokemon_a = {
    "chancey":"https://i.imgur.com/lcKPGWM.png",
    "shelmet":"https://i.imgur.com/E0qzGAq.png",
    "KlinKlang":"https://i.imgur.com/wsNYVCp.png"
}

# picks a random pokemon and sends an sms requesting the user guess the pokemon
random_pokemon = random.choice(pokemon_q.keys())
url = pokemon_a[random_pokemon]
message = client.messages.create(
    to=os.environ.get('my_phone'),
    from_=os.environ.get('twilio_phone'),
    body="Who's that Pokemon?",
    media_url=pokemon_q[random_pokemon]
    )

print(message.sid)

# calls the python file that handles requests and answers
call(["python", "app.py", random_pokemon, url])