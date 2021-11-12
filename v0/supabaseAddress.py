import os
#import asyncio
import supabase_py as sb
#import supabase_client
import datetime

class Address:
  def __init__(self):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    self.supabase = sb.create_client(url, key)
    self.addresses = self.supabase.table('addresses').select(
    'inserted_at, name, uid, addr1, addr2,city, state, zip, country'
    ).execute()

  def nodemasters(self, uid):
    nodemasters = self.supabase.table('nodemasters').select('uid').execute()
    for nuid in range(len(nodemasters['data'])):
      if nodemasters['data'][nuid]['uid'] == uid:
        return True
    return False

  def admins(self, uid):
    admins = self.supabase.table('admin').select('uid').execute()
    for nuid in range(len(admins['data'])):
      if admins['data'][nuid]['uid'] == uid:
        return True
    return False

  def leaders(self, uid):
    leaders = self.supabase.table('leaders').select('uid').execute()
    for nuid in range(len(leaders['data'])):
      if leaders['data'][nuid]['uid'] == uid:
        return True
    return False

  def nodemaster_address(self, uid):
    nodemasters = self.supabase.table('nodemasters').select('name, uid, addr1, addr2, city, state, zip, country').execute()
    for nuid in range(len(nodemasters['data'])):
      if nodemasters['data'][nuid]['uid'] == uid:
        return nodemasters['data'][nuid]
    return

  def address_uid(self, uid="", ts=""):
    epoch = lambda e: datetime.datetime.fromisoformat(e).timestamp() * 1000

    ts_result = ""
    if ts != "":
      orders = self.supabase.table('orders').select('shipto_uid, message_id').execute()
      for record in range(len(orders['data'])):
        if orders['data'][record]['message_id'] == ts:
          ts_result = orders['data'][record]['shipto_uid']
    
    recordList = self.addresses['data']

    returnList = []
    for i in range(len(recordList)):
      if recordList[i]['uid'] == uid:
        returnList.append(recordList[i])
      
    returnListCounter = 0
    for i in range(len(returnList)):
      if returnList[i]['name'] != "":
        break
      else:
        returnListCounter+=1
        if returnListCounter == len(returnList):
          return {"name": "", "uid": uid, "addr1": "", "addr2": "", "city": "", "state": "", "zip": "", "country": ""}

    if len(returnList) == 0:
      return {"name": "", "uid": uid, "addr1": "", "addr2": "", "city": "", "state": "", "zip": "", "country": ""}
      
    largerRecord = None

    for record in range(len(recordList)):
      if ts_result != "":
        uid = ts_result
      if recordList[record]['uid'] == uid:
        returnList.append(recordList[record])
    
      largerRecord = returnList[0]
      for i in range(len(returnList)):
          epoch_return_list = epoch(returnList[i]["inserted_at"][0:19])
          epoch_larger_record = epoch(largerRecord["inserted_at"][0:19])
          if epoch_return_list > epoch_larger_record:
              largerRecord = returnList[i]
          i += 1

      return largerRecord

  def insertAddress(self, name, uid, addr1, addr2, city, state, zip, country):
    data = self.supabase.table("addresses").insert({
        'name': name,
        'uid': uid,
        'addr1': addr1,
        'addr2': addr2,
        'city': city,
        'state': state,
        'zip': zip,
        'country': country
    }).execute()
    assert len(data.get("data", [])) > 0

    return

  def addOrder(self, request, shipto, order, id):
    data = self.supabase.table("orders").insert({
        'request_uid': request,
        'shipto_uid': shipto,
        'order_type': order,
        'message_id': id
    }).execute()
    assert len(data.get("data", [])) > 0

    return

  def addLead(self, uid):
    data = self.supabase.table("leaders").insert({
        'uid': uid
    }).execute()
    assert len(data.get("data", [])) > 0

    return  

  def getOrders(self, uid):
    data = self.supabase.table("orders").select("shipto_uid, message_id").execute()
    
    dataList = []
    for i in range(len(data['data'])):
      if data['data'][i]['shipto_uid'] == uid:
        dataList.append(data['data'][i])
    if len(dataList) > 3:
      dataList = dataList[len(dataList)-3:len(dataList)]
    else:
      dataList = dataList
    return dataList

  def getOrderTo(self, ts):
    data = self.supabase.table("orders").select("shipto_uid, message_id").execute()
    for order in range(len(data['data'])):
      record = data['data'][order]
      if record["message_id"] == ts:
        return record['shipto_uid']
    
    return