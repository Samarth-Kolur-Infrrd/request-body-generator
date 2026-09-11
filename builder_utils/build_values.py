from app.mongo_connection import get_sub_extraction_field, is_valid_generic_table

def build_values(id: str) -> list:
    subfields = get_sub_extraction_field(id)
    output_values = []
    for subfield in subfields:
        if subfield.get("taggedStatus") in ("TAGGED", "ADD"):
            structured_value = []
            for value in subfield.get("values"):
                if value.get("fieldType") == "Generic Table":
                    # extraction_field_id = value.get("id")
                    # sub_extraction_collateral_parent = subfield.get("_id")
                    # if is_valid_generic_table(extraction_field_id, sub_extraction_collateral_parent):
                    #     structured_value.append(value)
                    structured_value = {}
                else:
                    structured_value = subfield.get("values")        
            output_values.append(structured_value)
    return output_values