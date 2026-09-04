from buildersUtils.buildValues import buildValues

def buildFields(fields: list) -> list:
    builtfields = []
    for field in fields:
        if field.get("hidden") == True:
            continue
        structured_field = { 
            "_id": field.get("_id"),
            "name": field.get("fieldName"),
            "type": field.get("fieldType"),
            "dataType": field.get("dataType"),
            "startX": field.get("startX"),
            "startY": field.get("startY"),
            "endX": field.get("endX"),
            "endY": field.get("endY"),
        }
        
        if field.get("fieldType") == "Single Value":
            type_based_fields = {
                "startIndex": field.get("startIndex"),
                "endIndex": field.get("endIndex"),
                "confidence": field.get("confidence"),
                "pageNumber": field.get("pageNumber"),
                "additionalAttributes": field.get("additionalAttributes"),
                "wordCoordinates": field.get("wordCoordinates"),
                "value": field.get("value"),
                "question": field.get("question"),
                "fieldId": field.get("fieldId"),
                "extractedUsing": field.get("extractedUsing"),
                "alternateCandidates":field.get("alternateCandidates")
            }
            structured_field.update(type_based_fields)

        elif field.get("fieldType") == "Generic Table":
            type_based_fields = {
                "startIndex": field.get("startIndex"),
                "endIndex":field.get("endIndex"),
                "confidence":field.get("confidence"),
                "pageNumber":field.get("pageNumber"),
                "additionalAttributes": field.get("additionalAttributes"),
                "wordCoordinates": field.get("wordCoordinates"),
                "headers": field.get("headers"),
                "values": field.get("values"),
                "formattedValues":field.get("formattedValues"),
                "fieldId": field.get("fieldId"),
                "extractedUsing":field.get("extractedUsing"),
                "alternateCandidates": field.get("alternateCandidates"),
                "order":field.get("order"),
                "extractionTableType": field.get("extractionTableType"),
            }
            structured_field.update(type_based_fields)
        
        else:
            values = buildValues(field.get("_id"))
            type_based_fields = {
                "pageNumber" : field.get("pageNumber"),
                "values": values,
                "correctedBy": field.get("correctedBy"),
                "correctedUserName"	: field.get("correctedUserName"),
                "correctedUserEmail"	: field.get("correctedUserEmail"),
                "correctedOn"	: field.get("correctedOn"),
                "extractedConfidence": field.get("extractedConfidence"),
                "fieldId"	: field.get("fieldId"),
                "extractedUsing": field.get("extractedUsing"),
                "alternateCandidates": field.get("alternateCandidates"),
                "order"	: field.get("order")
            }
            structured_field.update(type_based_fields)

        builtfields.append(structured_field)
    return builtfields
