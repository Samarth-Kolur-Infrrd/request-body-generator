def buildHeaders(data: list, output: dict)-> dict:
    headers = output
    headers["requestId"] = data[0][0]["requestId"]
    headers["status"] = data[0][0]["status"]
    return headers

