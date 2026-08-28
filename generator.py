from mongoConnection import getData
from builders import buildDocuments, buildHeaders, buildFields, buildPages

def generateRequestBody(inputId):
    Collections = getData(inputId)
    output = {}
    output = buildHeaders(Collections, output)
    output = buildDocuments(Collections, output,
                            buildFields(Collections[2]),
                            buildPages(Collections[1]))
    return output