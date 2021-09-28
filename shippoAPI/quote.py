import shippo

"""
In this tutorial we have an order with a sender address,
recipient address and parcel. We will retrieve all avail-
able shipping rates, display them to the user and purchase
a label after the user has selected a rate.
"""

# for demo purposes we set the max. transit time here
MAX_TRANSIT_TIME_DAYS = 10

# replace <API-KEY> with your key
shippo.config.api_key = "APIKEY"

# Example address_from object dict
# The complete refence for the address object is available here: https://goshippo.com/docs/reference#addresses
address_from = {
    "name": "Hugo Hu",
    "street1": "13 Corgi St.",
    "street2": "Suite Welsh",
    "city": "New Corgi",
    "state": "NC",
    "zip": "CORGI",
    "country": "US",
}

# Example address_to object dict
# The complete refence for the address object is available here: https://goshippo.com/docs/reference#addresses

address_to = {
    "name": "Corgi's Friend",
    "street1": "15 Translyvanian St.",
    "city": "Hound",
    "state": "DOG",
    "zip": "PUPPY",
    "country": "US",
}

# parcel object dict
# The complete reference for parcel object is here: https://goshippo.com/docs/reference#parcels
parcel = {
    "length": "6",
    "width": "4",
    "height": "2",
    "distance_unit": "in",
    "weight": "15.9",
    "mass_unit": "oz",
}

# Example shipment object
# For complete reference to the shipment object: https://goshippo.com/docs/reference#shipments
# This object has asynchronous=False, indicating that the function will wait until all rates are generated before it returns.
# By default, Shippo handles responses asynchronously. However this will be depreciated soon. Learn more: https://goshippo.com/docs/async
shipment = shippo.Shipment.create(
    address_from=address_from,
    address_to=address_to,
    parcels=[parcel],
    asynchronous=False
)

# Rates are stored in the `rates` array
# The details on the returned object are here: https://goshippo.com/docs/reference#rates
rates = shipment.rates

# info = "$" + str(rates[5]) + ", Carrier: " + str(rates[9]) + ", Service: " + str(rates[12]) + ", Delivery Time: " + str(rates[13]) + " days, duration terms: " + str(rates[14])

service_list = {}
for shipser in range(len(rates)):
    service = rates[shipser]
    service_list["Delivery Estimate: " + str(service["estimated_days"]) + " days, Carrier: " + service["provider"] + ", Service: " + service["servicelevel"]["name"]] = float(service["amount"])
#print(rates, type(rates))

priceList = sorted(service_list.values())
serviceListRaw = service_list.keys()
for price in priceList:
    for service in serviceListRaw:
        if service_list[service] == price:
            print("$" + str(price) + ", " + service)



