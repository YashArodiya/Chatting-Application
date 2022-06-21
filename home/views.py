from django.shortcuts import render
import mysql.connector as connector
from datetime import datetime

# Create your views here.
global searchText
searchText = 9773509008

def Login(request):
    
    if request.method == "POST":
        global name
        name = request.POST.get('name')
        global phone
        phone = request.POST.get('Phone')
        return render(request,"test.html")
    else:
        return render(request,"test.html")


def chat(request):
    
    template_name="hello.html"
    data = fetch().data()
    cont = fetch().contact()
    Online = fetch().Online_time
    priv = fetch().Private()
    global searchText
    global Reply
    if request.POST.get('searchText'):
        searchText = request.POST.get('searchText')
        if len(searchText) == 8:
            data = fetch().GroupChat()
    if request.POST.get('Reply'):
        Reply = request.POST.get('Reply')
        print(Reply)
        fetch().SaveChat(Reply)
    
    context = {'data': data,'Name':name,'Cont':cont,'Phone':int(phone),'Online':Online,'private':priv}
    return render(request, template_name, context)


class fetch :

    def __init__(self):

        self.con = connector.connect(host ='127.0.0.1',
                                    port = "3306",
                                    user = 'root',
                                    password = 'Arnav@123',
                                    database = 'whatsapp')

    def data(self):

        query = "select chatID,Sender,Date_Time from chat where (Sender = %s AND Reciever = %s) OR (Sender = %s AND Reciever = %s)"
        tup = (phone,searchText,searchText,phone)
        cur = self.con.cursor()
        cur.execute(query,tup)
        x = []
        for i in cur:
            y = {}
            y['chat'] = i[0]
            y['sender'] = i[1]
            y['date']  = i[2]
            x.append(y)
                
        return x

    def contact(self):
        query  = "select Name, Uni_ID from users where Uni_ID in(select Contacts from contact where Users = %s)"
        tup = (phone,)
        cur = self.con.cursor()
        cur.execute(query,tup)
        x = []
        for i in cur:
            y = str(i[0])+'-'+str(i[1])
            x.append(y)
        
        Gquery = "select Name, GroupID from all_groups where GroupID in(select GroupID from participants where Uni_ID = %s)"

        exc = self.con.cursor()
        exc.execute(Gquery,tup)
        for i in exc:
            y = str(i[0])+'-'+str(i[1])
            x.append(y)
        return x

    def SaveChat(self,chat):

        now = datetime.now()
        tup = (102,now,phone,searchText,chat,1)
        query = "INSERT INTO chat VALUES (%s,%s,%s,%s,%s,%s)"
        cur = self.con.cursor()
        cur.execute(query,tup)
        self.con.commit()

    def Online_time(self):
        x = []
        tup = (searchText,)
        q = "select online_status, Last_seen from abc where Uni_ID = %s"
        cur = self.con.cursor()
        cur.execute(q,tup)    
        for i in cur:
            y = {}
            y['online'] = i[0]
            y['LastSeen'] = i[1]
        x.append(y)
        return x 

    def Private(self):

        tup = (searchText,)
        query = "select Privacy from private where Uni_ID = %s"
        cur = self.con.cursor()
        cur.execute(query,tup)
        x = 0
        for i in cur:

            x = i[0]
        return x

    def GroupChat(self):

        query = "select chatID,Sender,Date_Time from groupchat where (Sender = %s AND Reciever = %s) OR (Sender = %s AND Reciever = %s)"
        tup = (phone,searchText,searchText,phone)
        cur = self.con.cursor()
        cur.execute(query,tup)
        x = []
        for i in cur:
            y = {}
            y['chat'] = i[0]
            y['sender'] = i[1]
            y['date']  = i[2]
            x.append(y)
                
        return x