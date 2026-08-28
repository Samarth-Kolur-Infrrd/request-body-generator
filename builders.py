def buildHeaders(data, output):
    headers = output
    headers["requestId"] = data[0][0]["requestId"]
    headers["status"] = data[0][0]["status"]
    return headers

def buildPages(pages):
    builtpages = []
    for page in pages:
        structured_page = {
            "id": page.get("_id"),
            "pageNumber": page.get("pageNumber"),
            "status": page.get("status"),
            "dpiRes": page.get("dpiRes"),
            "rotation": page.get("rotation")
        }
        builtpages.append(structured_page)
    return builtpages

def buildFields(fields):
    builtfields = []
    for field in fields:
        structured_field = { 
            "name": field.get("fieldName"),
            "type": field.get("fieldType"),
            "dataType": field.get("dataType"),
            "confidence": field.get("confidence"),
            "value": field.get("value"),
            "isCorrected":field.get("isCorrected")
        }
        builtfields.append(structured_field)
    return builtfields

def buildDocuments(data, output, fields, pages):
    documents = data[0]
    builtdocumentList = []
    
    for document in documents:
        documentData = {
            "id": document.get("_id"),
            "name": document.get("fileName"),
            "fileType": document.get("fileType"),
            "status": document.get("status"),
            "subStatus": document.get("subStatus"),
            "docType": document.get("docType"),
            "splitDocumentUrl": document.get("splitDocumentUrl"),
            "splitLevel": document.get("splitLevel"),
            "alphaId": document.get("sourceDocumentId"),
            "fields": fields,
            "pages" : pages,
                        }
        
        if document.get("isCorrected"):
            correctedDetails = {
                "splitDocumentPath": document.get("splitDocumentPath"),
                "splitCorrectionStartTime":document.get("splitCorrectionStartTime"),
                "splitCorrectionEndTime": document.get("splitCorrectionEndTime"),
                "splitCorrectionTime":document.get("splitCorrectionTime"),
                "splitCorrectionUser": document.get("splitCorrectionUser"),
                "splitCorrectedBy":document.get("splitCorrectedBy"),
                "cropQueueAddTime": document.get("cropQueueAddTime"),
                "cropCorrectionStartTime": document.get("cropCorrectionStartTime"),
                "cropCorrectionEndTime": document.get("cropCorrectionEndTime"),
                "cropCorrectionTime": document.get("cropCorrectionTime"),
                "cropCorrectionUser": document.get("cropCorrectionUser"),
                "cropCorrectedBy": document.get("cropCorrectedBy"),
                "sourceDocumentUrl": document.get("sourceDocumentUrl"),
                "correctedByUserInfo": {
                    "SPLIT_CORRECTION": {
                        "queueAddTime": document.get("splitQueueAddTime"),
                        "correctedByUserEmail": document.get("correctedUserName"),
                        "correctedByUserName": document.get("splitCorrectionUser"),
                        "correctionEndTime": document.get("splitCorrectionEndTime"),
                        "correctionStartTime": document.get("splitCorrectionStartTime")
                    },
                    "CROP_CORRECTION": {
                        "queueAddTime": document.get("cropQueueAddTime"),
                        "correctedByUserEmail": document.get("correctedUserName"),
                        "correctedByUserName": document.get("cropCorrectionUser"),
                        "correctionEndTime": document.get("cropCorrectionEndTime"),
                        "correctionStartTime": document.get("cropCorrectionStartTime")
                    }
                }
            }
            documentData.update(correctedDetails)

        otherFields = {
            "documentExtractionStartDate": document.get("documentExtractionStartDate"),
            "documentReceivedDate": document.get("documentReceivedDate"),
            "lastModifiedDate": document.get("lastModifiedDate"),
            "splitQueueAddTime": document.get("splitQueueAddTime"),
            "classificationStatus": document.get("classificationStatus"),
            "classificationConfidence": document.get("classificationConfidence"),
            "version": document.get("version"),
            "isDocSigned": document.get("isDocSigned"),
            "docSigned": document.get("docSigned"),
            "totalBlankPages": document.get("totalBlankPages"),
            "totalPages": document.get("totalPages")
            }
        documentData.update(otherFields)               
        builtdocumentList.append(documentData)
    output["documents"] = builtdocumentList
    return output