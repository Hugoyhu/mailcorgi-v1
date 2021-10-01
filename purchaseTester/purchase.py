import shippo
import purchaseInfo

# enter your shippo test API
shippo.config.api_key = ""

# import label info from purchaseInfo.py crude but it's easier for dev
address_from = purchaseInfo.senderAddress

address_to = purchaseInfo.recipientAddress

parcel = purchaseInfo.parcelInfo

# create the shipment
shipment = shippo.Shipment.create(
    address_from=address_from,
    address_to=address_to,
    parcels=[parcel],
    asynchronous=False
)

# idfk what's happening here because i'm a bad dev but it sorts our prices and returns a list
rawRates = shipment.rates
sorted_dict = {}
service_list = []
serviceListRaw = []
for shipser in range(len(rawRates)):
    print(shipser)
    service = rawRates[shipser]
    print(service)
    service_list.append(float(rawRates[shipser]["amount"]))
    serviceListRaw.append(service)

returnServices = []
priceList = sorted(service_list)
print(priceList)
for price in priceList:
    price = str(price)
    for service in serviceListRaw:
        if service["amount"] == price:
            print("$" + price + ", " + service["servicelevel"]["name"])
            returnServices.append(service)

# sanity check: are there any shipping services
if len(returnServices) > 0:
    rate = returnServices[0]
    print("Purchasing " + returnServices[0]["servicelevel"]["name"] + " for $" + str(priceList[0]))

else:
    print("no shipping services at this time")

# failed attempt at a price check. didn't work and was inefficient
'''
if shipment.rates[3]["servicelevel"]["token"] == "usps_first":
    rate = shipment.rates[3]
    print("Purchasing USPS FCM Label for " + rate["amount"])
elif shipment.rates[1]["servicelevel"]["token"] == "usps_priority":
    rate = shipment.rates[1]
    print("Purchasing USPS Priority Mail Label for " + rate["amount"])
'''
transaction = shippo.Transaction.create(
    rate=rate.object_id, asynchronous=False)

# print out yer label

if transaction.status == "SUCCESS":
    print("Purchased label with tracking number %s" %
          transaction.tracking_number)
    print("The label can be downloaded at %s" % transaction.label_url)
else:
    print("Failed purchasing the label due to:")
    for message in transaction.messages:
        print("- %s" % message['text'])
