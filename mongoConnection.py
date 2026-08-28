from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["requestBodyGeneration"]

documentCollection = db["document"]
pageCollection = db["page"]
extractionFieldCollection = db["extraction_field"]

def getData(inputId):
    document = list(documentCollection.find({"_id":inputId["documentId"]}))
    page = list(pageCollection.find(inputId))
    field = list(extractionFieldCollection.find(inputId))
    return [ document, page, field ]