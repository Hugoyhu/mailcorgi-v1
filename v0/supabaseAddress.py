import os
#import asyncio
import supabase_py as sb
#import supabase_client
import datetime

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = sb.create_client(url, key)


def address_uid(uid):
    data = supabase.table('addresses').select(
        'inserted_at, name, uid, addr1, addr2,city, state, zip, country'
    ).execute()
    #error, results = (
    #supabase.table("addresses")
    #.select("name, uid, addr1, addr2, city, state, zip, countr")
    #.query()
    #)
    #print(results)

    # 2021-10-14T15:44:51.684Z
    epoch = lambda e: datetime.datetime.fromisoformat(e).timestamp() * 1000
    if data == None:
        return
    recordList = data['data']
    returnList = []
    largerRecord = None
    print(data)
    for record in range(len(recordList)):
        if recordList[record]['uid'] == uid:
            returnList.append(recordList[record])

    print(returnList)
    largerRecord = returnList[0]
    for i in range(len(returnList)):
        epoch_return_list = epoch(returnList[i]["inserted_at"][0:19])
        epoch_larger_record = epoch(largerRecord["inserted_at"][0:19])
        if epoch_return_list > epoch_larger_record:
            largerRecord = returnList[i]
        i += 1

    return largerRecord


def removeDuplicates(uid):
    record = address_uid(uid)

    #check if record present
    if record == None:
        return

    record["uid"] = None


def insertAddress(name, uid, addr1, addr2, city, state, zip, country):
    data = supabase.table("addresses").insert({
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


def addOrder(request, shipto, order, id):
    data = supabase.table("orders").insert({
        'request_uid': request,
        'shipto_uid': shipto,
        'order_type': order,
        'message_id': id
    }).execute()
    assert len(data.get("data", [])) > 0

    return

