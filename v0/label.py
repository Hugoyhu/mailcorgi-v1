# generates a 4x6 thermal-ready label w/ address info(for #6.75 envelopes) and a message from hack club

from reportlab.pdfgen.canvas import Canvas
import supabaseAddress

def labelPDF(nUID, rUID, stamp):
  addr = supabaseAddress.Address()
  # get addresses
  nAddr = addr.nodemaster_address(uid=nUID)
  rAddr = addr.address_uid(uid=rUID)

  value = lambda x: nAddr[x]
  Sname = value("name")
  Suid = value("uid")
  Saddr1 = value("addr1")
  Saddr2 = value("addr2")
  Scity = value("city")
  Sstate = value("state")
  Szipcode = value("zip")
  Scountry = value("country")

  value = lambda x: rAddr[x]
  Rname = value("name")
  Ruid = value("uid")
  Raddr1 = value("addr1")
  Raddr2 = value("addr2")
  Rcity = value("city")
  Rstate = value("state")
  Rzipcode = value("zip")
  Rcountry = value("country")
  
  # 4x6 -> x72
  pdfName = Rname + ".pdf"
  canvas = Canvas(Rname + ".pdf", pagesize=(432.0, 288.0))

  
  canvas.setFont("Courier", 11)

  #canvas.rotate(90)
  if Saddr2 is None:
    startX = 14
    startY = 270
    yIncrement = 14
    canvas.drawString(startX, startY, Sname)
    canvas.drawString(startX, startY - yIncrement, Saddr1)
    canvas.drawString(startX, startY - 2 * yIncrement, Scity + ", " + Sstate + ", " + Szipcode)
    canvas.drawString(startX, startY - 3 * yIncrement, Scountry)

  else: 
    startX = 14
    startY = 270
    yIncrement = 14
    canvas.drawString(startX, startY, Sname)
    canvas.drawString(startX, startY - yIncrement, Saddr1)
    canvas.drawString(startX, startY - 2 * yIncrement, Saddr2)
    canvas.drawString(startX, startY - 3 * yIncrement, Scity + ", " + Sstate + ", " + Szipcode)
    canvas.drawString(startX, startY - 4 * yIncrement, Scountry)

  if Raddr2 is None:
    startX = 200
    startY = 180
    yIncrement = 14
    canvas.drawString(startX, startY, Rname)
    canvas.drawString(startX, startY - yIncrement, Raddr1)
    canvas.drawString(startX, startY - 2 * yIncrement, Rcity + ", " + Rstate + ", " + Rzipcode)
    canvas.drawString(startX, startY - 3 * yIncrement, Rcountry)
  else: 
    startX = 200
    startY = 180
    yIncrement = 14
    canvas.drawString(startX, startY, Rname)
    canvas.drawString(startX, startY - yIncrement, Raddr1)
    canvas.drawString(startX, startY - 2 * yIncrement, Raddr2)
    canvas.drawString(startX, startY - 3 * yIncrement, Rcity + ", " + Rstate + ", " + Rzipcode)
    canvas.drawString(startX, startY - 4 * yIncrement, Rcountry)

  canvas.drawString(10, 10, "Hello from Hack Club! By the students, for the students")
  
  #canvas.rotate(90)

  canvas.save()
  return pdfName
