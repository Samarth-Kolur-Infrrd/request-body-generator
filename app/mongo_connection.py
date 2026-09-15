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

document_collection = db["document"]
page_collection = db["page"]
extraction_field_collection = db["extraction_field"]
sub_extraction_field = db["sub_extraction_field"]

def get_data(input_id: dict) -> list:
    try:
        document = list(document_collection.find({"_id":input_id["documentId"]}))
        page = list(page_collection.find(input_id))
        field = list(extraction_field_collection.find(input_id))
        
        return [ document, page, field ]
    except PyMongoError:
        logger.exception("Mongo query failed for input_id=%s against %s", input_id, MONGODB_URI)
        raise

def get_sub_extraction_field(id:str) -> list:
    subfield = list(sub_extraction_field.find({"extractionFieldId": id}))
    return subfield

def get_collateral_records(extraction_field_id):
    return list(sub_extraction_field.find({"extractionFieldId": extraction_field_id}))

def get_sub_extraction_parent_table(parent_id):
    return list(sub_extraction_field.find({"subExtractionCollateralParent": parent_id}))
