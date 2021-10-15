# TODO: add /add-leader, and other utility commands

import os, logging, supabaseAddress, re
# Use the package we installed
from slack_bolt import App

logging.basicConfig(level=logging.DEBUG)
# Initializes your app with your bot token and signing secret

app = App(token="",
          signing_secret="")


@app.command("/send-envelope")
def envelope(ack, client, command):
    ack()

    postText = ""
    if command["text"] != "": 
      user = ""
      try:
        user = re.search("<@(U.+?)\|.+>", command["text"].split(" ")[0]).group(1)
        address = supabaseAddress.address_uid(str(user))
        postText = f'''
:rotating_light: MISSION ALERT :rotating_light:
Sticker Envelope for {address['name']} ({command['text'].split(" ")[0]})
Here's what's in a Sticker Envelope:
- 10 Assorted Stickers 
And here's our address data:
```
Name: {address['name']}
Street (First Line): {address['addr1']}
Street (Second Line): {address['addr2']}
City: {address['city']}
State/Province: {address['state']}
Postal Code: {address['zip']} 
Country: {address['country']}```
'''
        results =  app.client.chat_postMessage(channel="C02GDBTKY4E", text=postText)
        supabaseAddress.addOrder(command['user_id'], user, "sticker_envelope", results['ts'])
      except AttributeError:
        postText = "Please retry with a valid user's Slack tag." 
    else:
      postText = "Please retry with a valid user's Slack tag."
    
    print(command)
 
# listen for react

@app.event("reaction_added")
def handle_reaction_added_events(body, logger):
    logger.info(body)

@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    next()


@app.command("/addressupdate")
def handle_command(body, ack, client, logger):
  """ 
  Step 5: 
  Payload is sent to this endpoint, we extract the `trigger_id` and call views.open
  """
  
  ack()
  logger.info(body)

  res = client.views_open(
      trigger_id=body["trigger_id"],
      view={
          "type":
          "modal",
          "callback_id":
          "address-modal",
          "title": {
              "type": "plain_text",
              "text": "My App",
              "emoji": True
          },
          "submit": {
              "type": "plain_text",
              "text": "Submit",
              "emoji": True
          },
          "close": {
              "type": "plain_text",
              "text": "Cancel",
              "emoji": True
          },
          "blocks": [
              {
                  "type": "section",
                  "text": {
                      "type":
                      "mrkdwn",
                      "text":
                      "Hello! PLease use this form to update the Address you have with Hack Club and MailCorgi."
                  }
              },
              {
                  "type": "divider"
              },
              {
                  "type": "input",
                  "block_id": "name",
                  "element": {
                      "type": "plain_text_input",
                      "action_id": "plain_text_input-action"
                  },
                  "label": {
                      "type": "plain_text",
                      "text": "Name",
                      "emoji": True
                  }
              },
              {
                  "type": "input",
                  "block_id": "addr1",
                  "element": {
                      "type": "plain_text_input",
                      "action_id": "plain_text_input-action"
                  },
                  "label": {
                      "type": "plain_text",
                      "text": "Address Line 1",
                      "emoji": True
                  }
              },
              {
                  "type": "input",
                  "block_id": "addr2",
                  "element": {
                      "type": "plain_text_input",
                      "action_id": "plain_text_input-action"
                  },
                  "label": {
                      "type": "plain_text",
                      "text": "Address Line 2",
                      "emoji": True
                  }
              },
              {
                  "type": "input",
                  "block_id": "city",
                  "element": {
                      "type": "plain_text_input",
                      "action_id": "plain_text_input-action"
                  },
                  "label": {
                      "type": "plain_text",
                      "text": "City",
                      "emoji": True
                  }
              },
              {
                  "type": "input",
                  "block_id": "state",
                  "element": {
                      "type": "plain_text_input",
                      "action_id": "plain_text_input-action"
                  },
                  "label": {
                      "type": "plain_text",
                      "text": "State",
                      "emoji": True
                  }
              },
              {
                  "type": "input",
                  "block_id": "zip",
                  "element": {
                      "type": "plain_text_input",
                      "action_id": "plain_text_input-action"
                  },
                  "label": {
                      "type": "plain_text",
                      "text": "Zip Code",
                      "emoji": True
                  }
              },
              {
                  "type": "input",
                  "block_id": "country",
                  "element": {
                      "type": "plain_text_input",
                      "action_id": "plain_text_input-action"
                  },
                  "label": {
                      "type": "plain_text",
                      "text": "Country",
                      "emoji": True
                  }
              },
          ]
      },
  )
  logger.info(res)


@app.view("address-modal")
def handle_view_events(ack, body, logger):
  """
  Step 4: 
  The path that allows for your server to receive information from the modal sent in Slack
  """
  ack()
    # declare the addresses

  value = lambda x: body["view"]["state"]["values"][x]["plain_text_input-action"]["value"]
  name = value("name")    
  uid = body["user"]["id"]    
  addr1 = value("addr1")   
  addr2 = value("addr2")    
  city = value("city")
  state = value("state")
  zipcode = value("zip") 
  country = value("country")

  supabaseAddress.insertAddress(name, uid, addr1, addr2, city, state, zipcode, country)
  logger.info(body["view"]["state"]["values"])


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
