from app.mongo_connection import get_data
from builder_utils.builders import builder

def generate_request_body(input_id: dict) -> dict:
    collections = get_data(input_id)
    output = {}
    output = builder(collections, output)
    return output