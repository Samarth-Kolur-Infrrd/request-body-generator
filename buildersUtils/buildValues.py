from mongoConnection import getSubExtractionField

def buildValues(id):
    subfields = getSubExtractionField(id)
    outputValues = []
    for subfield in subfields:
        
        if subfield.get("taggedStatus") in ("TAGGED", "ADD"):
            structured_value = subfield.get("values")
            outputValues.append(structured_value)
    return outputValues