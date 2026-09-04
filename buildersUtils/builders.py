from buildersUtils.buildDocument import buildDocuments
from buildersUtils.buildHeaders import buildHeaders
from buildersUtils.buildPages import buildPages
from buildersUtils.buildFields import buildFields

def builder(data: list, output: dict) -> dict:
    fields = buildFields(data[2])
    pages = buildPages(data[1])

    output = buildHeaders(data,output)
    output = buildDocuments(data[0], output, fields, pages)

    return output
