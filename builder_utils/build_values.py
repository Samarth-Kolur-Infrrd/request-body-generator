from app.mongo_connection import get_sub_extraction_field

def build_generic_table_value(id: str) -> list:
    subfield = get_sub_extraction_field(id)
    return subfield[0].get("values") if subfield else []
