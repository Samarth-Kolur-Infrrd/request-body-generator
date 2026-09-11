from builder_utils.build_document import build_documents
from builder_utils.build_headers import build_headers
from builder_utils.build_pages import build_pages
from builder_utils.build_fields import build_fields

def builder(data: list, output: dict) -> dict:
    fields = build_fields(data[2])
    pages = build_pages(data[1])

    output = build_headers(data,output)
    output = build_documents(data[0], output, fields, pages)

    return output
