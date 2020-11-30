import pymongo

uri = "mongodb+srv://aniket:Aniketsprx077@cluster0.uugt8.mongodb.net/test?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(uri)
mydb = myclient["crypto-bot"]
mycol = mydb["reports"]

data = {
    "pair" : "ETHUSDT",
    "report" : {}
}

x = mycol.insert_one(data)

print(x)
