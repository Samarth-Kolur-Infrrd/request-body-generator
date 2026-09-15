from app.mongo_connection import get_collateral_records, get_sub_extraction_parent_table
from builder_utils.build_values import build_generic_table_value

def build_fields(fields: list, type: str, id: str) -> list:
    built_fields = []
    sub_extraction_parent_table = get_sub_extraction_parent_table(id)

    for field in fields:

        if field.get("hidden") == True:
            continue

        if field.get("fieldType") == "Generic Table" and type == "normal":
            field["values"] = build_generic_table_value(field.get("_id"))
        else:
            field["value"] = sub_extraction_parent_table

        if field.get("fieldType") == "Object List":
            field["values"] = build_collateral_value(field.get("_id"))

        built_fields.append( field )

    return built_fields

def build_collateral_value(extraction_field_id: str) -> list:
    values = []
    sub_extraction_records = get_collateral_records(extraction_field_id)
    
    for record in sub_extraction_records:
        sub_value_records = record.get("values")
        values.append(build_fields(sub_value_records,"collateral", extraction_field_id))

    return values
