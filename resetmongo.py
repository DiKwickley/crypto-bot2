import pymongo

mongo_uri = "mongodb+srv://aniket:Aniketsprx077@cluster0.uugt8.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_uri)

db = client["crypto-bot"]
reports = db['reports']

x = reports.delete_many({})
print(x)