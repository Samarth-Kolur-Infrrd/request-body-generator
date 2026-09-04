from app.mongoConnection import getData
from buildersUtils.builders import builder

def generateRequestBody(inputId: dict) -> dict:
    Collections = getData(inputId)
    output = {}
    output = builder(Collections, output)
    return output