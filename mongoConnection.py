import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.environ.get("MONGODB_URI")

client = MongoClient(MONGODB_URI)

db = client["requestBodyGeneration"]

documentCollection = db["document"]
pageCollection = db["page"]
extractionFieldCollection = db["extraction_field"]

def getData(inputId):
    document = list(documentCollection.find({"_id":inputId["documentId"]}))
    page = list(pageCollection.find(inputId))
    field = list(extractionFieldCollection.find(inputId))
    return [ document, page, field ]