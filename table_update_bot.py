import pymongo

connection = pymongo.MongoClient("ds121906.mlab.com", 21906)
db = connection["nana"]
db.authenticate("nana", "nana")
records = db.reserved_table

# user_records = db.reserved_table
# db.reserved_table.insert({"client_id": "000025947", "first_name": "Ode", "book_table": "1:00 PM"})
# records = db.reserved_table.find({})

def insert_Record(chat_id,last_chat_name, text):
    data = records.insert({"client_id":chat_id, "first_name":last_chat_name, "book_table":text})
    return data

def get_Record():
    new_booked_data = ''
    booked_data = db.reserved_table.find()

    for key, record in enumerate(booked_data, 1):
        new_booked_data += str(key) + ". " +record['first_name']+ " - " + record['book_table'] + '\n'

    return new_booked_data

def get_table():
    table_list = ["1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM",]

    return table_list

# datas = get_Record()
# print ("this is datas: ",datas)
