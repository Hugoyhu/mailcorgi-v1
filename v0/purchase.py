import shippo
import supabase_py as sb
import supabaseAddress
import os

class Purchase:
  def __init__(self, nodemaster_uid, r_uid, package_type):
    # create supabase instance w/ env. keys
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    self.supabase = sb.create_client(url, key)

    shippo.config.api_key = os.environ.get("SHIPPO_API_KEY")

    # maximum days in transit
    self.MAX_TRANSIT_TIME_DAYS = 10

    # fetch nodemaster info
    address = self.supabase.table('nodemasters').select('name, uid, addr1, addr2, city, state, zip, country').execute()

    # fetch client info
    sba = supabaseAddress.Address()
    receiver = sba.address_uid(uid=r_uid)

    value = lambda x: receiver[x]
    self.Rname = value("name")
    self.Ruid = value("uid")
    self.Raddr1 = value("addr1")
    self.Raddr2 = value("addr2")
    self.Rcity = value("city")
    self.Rstate = value("state")
    self.Rzip = value("zip")
    self.Rcountry = value("country")

    # fetch package info

    package = self.supabase.table('parcel').select('type, length, width, height, weight, is_envelope').execute()
    
    # switch: determines type of package requested
    # capital P denotes "parcel/package"

    for parcelType in range(len(package['data'])):
      if package['data'][parcelType]['type'] == package_type:
        value = lambda x: package['data'][parcelType][x]
        self.pType = value("type")
        self.pLength = value("length")
        self.pWidth = value("width")
        self.pHeight = value("height")
        self.pWeight = value("weight")
        self.envelope = value("is_envelope")

    # check nodemaster's address in supabase table
    # capital S denotes "sender"
    for key in range(len(address['data'])):
      if address['data'][key]['uid'] == nodemaster_uid:
        value = lambda x: address['data'][key][x]
        self.Sname = value("name")
        self.Suid = value("uid")
        self.Saddr1 = value("addr1")
        self.Saddr2 = value("addr2")
        self.Scity = value("city")
        self.Sstate = value("state")
        self.Szipcode = value("zip")
        self.Scountry = value("country")
    
    # create shippo shipment object
    shippo.api_key = os.environ.get("SHIPPO_API_KEY")

    self.address_from = {
      "name": self.Sname,
      "street1": self.Saddr1,
      "street2": self.Saddr2,
      "city": self.Scity,
      "state": self.Sstate,
      "zip": self.Szipcode,
      "country": self.Scountry
    }


    self.address_to = {
      "name": self.Rname,
      "street1": self.Raddr1,
      "street2": self.Raddr2,
      "city": self.Rcity,
      "state": self.Rstate,
      "zip": self.Rzip,
      "country": self.Rcountry
    }

    parcel = {
      "length": self.pLength,
      "width": self.pWidth,
      "height": self.pHeight,
      "distance_unit": "in",
      "weight": self.pWeight,
      "mass_unit": "oz"
    }


    self.shipment = shippo.Shipment.create(
      address_from = self.address_from,
      address_to = self.address_to,
      parcels = [parcel],
      asynchronous = False
    )

  # quote costs
  
  def quote(self):
    rates = self.shipment.rates

    # return in format of: 
    # [[prices], [services]]

    if self.envelope == True:
      if self.Rcountry != "US":
        return {"2-8 weeks, USPS International Forever Stamp": "1.30"}
      else:
        return {"3-7 days, USPS Domestic Forever Stamp, Untracked": "0.58"}

      if self.Rcountry != "US":
        return {"1-3 weeks, PirateShip Simple Export Rate": "8.49+"}
      rates = self.shipment.rates

      # {'5 days, Service: First-Class Package/Mail Parcel': '4.39', '7 days, Service: Parcel Select': '7.56', '2 days, Service: Priority Mail': '7.59', '2 days, Service: Ground': '7.66', '3 days, Service: 3 Day Select®': '9.1', '2 days, Service: 2nd Day Air®': '9.54', '2 days, Service: 2nd Day Air® A.M.': '10.42', '1 days, Service: Next Day Air Saver®': '20.44', '1 days, Service: Priority Mail Express': '25.45', '1 days, Service: Next Day Air®': '25.72', '1 days, Service: Next Day Air® Early': '55.72'}

      service_list = {}
      for shipser in range(len(rates)):
          service = rates[shipser]
          service_list[str(service["estimated_days"]) + " days, Service: " + service["servicelevel"]["name"]] = float(service["amount"])
      #print(rates, type(rates))
      serviceDict = {}
      priceList = sorted(service_list.values())
      serviceListRaw = service_list.keys()
      for price in priceList:
          for service in serviceListRaw:
              if service_list[service] == price:
                  serviceDict[service] = str(price)

      return serviceDict

  def buy(self):
    rates = self.shipment.rates

# filter rates by max. transit time, then select cheapest
    eligible_rate = (
        rate for rate in rates if rate['estimated_days'] <= 30)
    rate = min(eligible_rate, key=lambda x: float(x['amount']))


    # Purchase the desired rate. asynchronous=False indicates that the function will wait until the
    # carrier returns a shipping label before it returns
    transaction = shippo.Transaction.create(
        rate=rate.object_id, asynchronous=False)

    # print label_url and tracking_number
    if transaction.status == "SUCCESS":
        

        return f"Purchase Label with Tracking Number {transaction.tracking_number} and can be downloaded at {transaction.label_url}"
    else:
        
        return
  
