import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

MONGODB_URI = os.environ.get("MONGODB_URI")

client = MongoClient(MONGODB_URI)

db = client["requestBodyGeneration"]

documentCollection = db["document"]
pageCollection = db["page"]
extractionFieldCollection = db["extraction_field"]

def getData(inputId):
    try:
        document = list(documentCollection.find({"_id":inputId["documentId"]}))
        page = list(pageCollection.find(inputId))
        field = list(extractionFieldCollection.find(inputId))
        return [ document, page, field ]
    except PyMongoError:
        logger.exception("Mongo query failed for inputId=%s against %s", inputId, MONGODB_URI)
        raise