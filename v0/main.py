import os, logging, re, time
# Use the package we installed
from slack_bolt import App

logging.basicConfig(level=logging.DEBUG)

mailChannelID = ""
# Initializes your app with your bot token and signing secret
botToken = os.environ.get("SLACK_BOT_TOKEN")
signingSec = os.environ.get("SLACK_SIGNING_SECRET")
app = App(token=botToken, signing_secret=signingSec)

os.system("pip install supabase_py")
time.sleep(10)
os.system("pip uninstall -y dataclasses")
time.sleep(5)

import supabaseAddress
import label
# create supabaseaddress address instnace
sba = supabaseAddress.Address()

@app.command("/send-envelope")
def envelope(ack, client, command):
    ack()

    postText = ""
    if command["text"][0:3] == "<@U": 
        user = ""
    
        user = re.search("<@(U.+?)\|.+>", command["text"].split(" ")[0]).group(1)
        if sba.leaders(command['user_id']) == False:
          threadText = "well give me a chewtoy an' tell me it's rawhide. you aren't a leader! *angry bjork*"
          app.client.chat_postEphemeral(
            channel=command['channel_id'],
            text=threadText,
            user=command['user_id']
          )
          return

        address = sba.address_uid(uid=str(user))
        
        if len(address) ==0:
          postText = f'''
:rotating_light: MISSION ALERT :rotating_light:
Requested by <@{command['user_id']}>
Sticker Envelope for {command['text'].split(" ")[0]}
Here's what's in a Sticker Envelope:
- 10 Assorted Stickers 
And here's our address data:
```
Name: {command['text'].split(" ")[0]}
Street (First Line): 
Street (Second Line): 
City: 
State/Province:
Postal Code: 
Country:```
React with :thumbsup: to accept, :moneybag: for manual purchase + label, :x: to drop, and :question: to request address.'''
        else:
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
React with :thumbsup: to accept, :moneybag: for manual purchase + label, :x: to drop, and :question: to request address.
'''
        results =  app.client.chat_postMessage(channel=mailChannelID, text=postText)
        sba.addOrder(command['user_id'], user, "sticker_envelope", results['ts'])

    else:
      postText = "Please retry with a valid user's Slack tag."

    if len(address['uid']) == 0:
      sba.insertAddress("", user, "", "", "", "", "", "")

@app.command("/send-box")
def box(ack, client, command):
    ack()

    postText = ""
    if command["text"][0:3] == "<@U": 
        user = ""
    
        user = re.search("<@(U.+?)\|.+>", command["text"].split(" ")[0]).group(1)
        if sba.leaders(command['user_id']) == False:
          threadText = "well give me a chewtoy an' tell me it's rawhide. you aren't a leader! *angry bjork*"
          app.client.chat_postEphemeral(
            channel=command['channel_id'],
            text=threadText,
            user=command['user_id']
          )
          return

        address = sba.address_uid(uid=str(user))
        
        if len(address) ==0:
          postText = f'''
:rotating_light: MISSION ALERT :rotating_light:
Requested by <@{command['user_id']}>
Sticker Box for {command['text'].split(" ")[0]}
Here's what's in a Sticker Box:
- 200 Assorted Stickers, 4 designs(bundles of 50)
And here's our address data:
```
Name: {command['text'].split(" ")[0]}
Street (First Line): 
Street (Second Line): 
City: 
State/Province:
Postal Code: 
Country:```
React with :thumbsup: to accept, :moneybag: for manual purchase + label, :x: to drop, and :question: to request address.'''
        else:
          postText = f'''
:rotating_light: MISSION ALERT :rotating_light:
Sticker Box for {address['name']} ({command['text'].split(" ")[0]})
Here's what's in a Sticker Box:
- 200 Assorted Stickers, 4 designs(bundles of 50)
And here's our address data:
```
Name: {address['name']}
Street (First Line): {address['addr1']}
Street (Second Line): {address['addr2']}
City: {address['city']}
State/Province: {address['state']}
Postal Code: {address['zip']} 
Country: {address['country']}```
React with :thumbsup: to accept, :moneybag: for manual purchase + label, :x: to drop, and :question: to request address.
'''
        results =  app.client.chat_postMessage(channel=mailChannelID, text=postText)
        sba.addOrder(command['user_id'], user, "sticker_box", results['ts'])

    else:
      postText = "Please retry with a valid user's Slack tag."

    if len(address['uid']) == 0:
      sba.insertAddress("", user, "", "", "", "", "", "")

@app.command("/add-leader")
def envelope(ack, client, command):
    ack()


    postText = ""
    if command["text"] != "": 

      user = ""
      if sba.admins(command['user_id']) == False:
        results =  app.client.chat_postEphemeral(
          channel=command['channel_id'], 
          text="You're not an admin! *angry bjork*",
          user=command['user_id']
        )
        return
      
      try:
        user = re.search("<@(U.+?)\|.+>", command["text"].split(" ")[0]).group(1)
        sba.addLead(user)
      
        postText = "Leader added!"
        
        app.client.chat_postEphemeral(
          channel=command['channel_id'], 
          text=postText,
          user=command['user_id']
        )

      except AttributeError:
        postText = "Please retry with a valid user's Slack tag." 
    else:
      postText = "Add"

  
    
  
# listen for react

@app.event("reaction_added")
def handle_reaction_added_events(body, client, logger):
  msg_ts = body['event']['item']['ts']

  threadText = ""

  nodemasterID = body['event']['user']
  if sba.nodemasters(nodemasterID) == False:
    threadText = "well give me a chewtoy an' tell me it's rawhide. you aren't a node master! *angry bjork*"
    app.client.chat_postMessage(
      channel=mailChannelID,
      thread_ts=msg_ts,
      text=threadText,
    )
  address = sba.address_uid(ts=msg_ts)

  rects = body['event']['item']['ts']
  recUID = sba.getOrderTo(rects)
  
  # create Purchase class instance
  # purchase = Purchase{}
  if body['event']['reaction'] == "+1":
    threadText=f"Mission accepted by <@{nodemasterID}>, DM'd to recepient"
    app.client.chat_postMessage(
      channel=recUID,
      text=f"Hi there! <@{nodemasterID}> has accepted your mail order. Please DM them if you have any inquiries."
    )
  elif body['event']['reaction'] == "x":
    threadText="Mission Dropped"
  #elif body['event']['reaction'] == "white_check_mark":
    #app.client.chat_postMessage(
      #channel=mailChannelID,
      #thread_ts=msg_ts,
      #text="Purchase Requested",
    #)
    # purchase cheapest shipping label
    # create Purchase class instance
    #purchaseLabel = purchase.Purchase(nodemasterID, recUID, "sticker_box_200")
    #threadText = purchaseLabel.buy()
    
  elif body['event']['reaction'] == "moneybag":
    # generate pdf
    fileName = label.labelPDF(nodemasterID, recUID, "0")
    try:
      response = app.client.files_upload(
        channels=mailChannelID,
        initial_comment="PDF upload",
        file=f"./{fileName}",
        thread_ts=msg_ts

      )
    except:
      logger.error("Error uploading file")

    os.system("rm *.pdf")

  elif body['event']['reaction'] == "question":
    # send a dm to user asking to run /updateaddress
    
    threadText="Address Requested"

    app.client.chat_postMessage(
      channel=recUID,
      text=f"Hi there! <@{nodemasterID}> needs to send you something in the mail: please use /addressupdate to update your address!"
    )

  app.client.chat_postMessage(
    channel=mailChannelID,
    thread_ts=msg_ts,
    text=threadText,
  )
  logger.info(body)

def shippingModal():
  pass
      
  


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
  print(body)
  address = sba.address_uid(body['user_id'])

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
                      "action_id": "plain_text_input-action",
                      "initial_value": address['name']
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
                      "initial_value": address['addr1'],
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
                  "optional": True,
                  "element": {
                      "type": "plain_text_input",
                      "initial_value": address['addr2'],
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
                      "initial_value": address['city'],
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
                      "initial_value": address['state'],
                      "action_id": "plain_text_input-action"
                  },
                  "label": {
                      "type": "plain_text",
                      "text": "State/Province",
                      "emoji": True
                  }
              },
              {
                  "type": "input",
                  "block_id": "zip",
                  "element": {
                      "type": "plain_text_input",
                      "initial_value": address['zip'],
                      "action_id": "plain_text_input-action"
                  },
                  "label": {
                      "type": "plain_text",
                      "text": "Zip/Pincode",
                      "emoji": True
                  }
              },
              {
                  "type": "input",
                  "block_id": "country",
                  "element": {
                      "type": "plain_text_input",
                      "initial_value": address['country'],
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
def handle_view_events(ack, body):
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

  sba.insertAddress(name, uid, addr1, addr2, city, state, zipcode, country)

  app.client.chat_postMessage(
      channel=uid,
      text=f"Thank you for filling out and updating your address. Your new address should be logged and sent to Mail Team shortly. To verify your address, run /addressupdate again. Your address should be prefilled."
    )
  print(uid)
  orders = sba.getOrders(uid)
  for order in range(len(orders)):
    app.client.chat_postMessage(
      channel=mailChannelID,
      thread_ts=orders[order]['message_id'],
      text=f'''
This address was just updated! Here's what we received:
```
Name: {name}
Street (First Line): {addr1}
Street (Second Line): {addr2}
City: {city}
State/Province: {state}
Postal Code: {zipcode} 
Country: {country}```
      ''',
    )
# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
