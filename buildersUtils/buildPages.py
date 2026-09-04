def buildPages(pages:list)->dict:
    builtpages = []
    for page in pages:
        structured_page = {
            "id": page.get("_id"),
            "pageNumber": page.get("pageNumber"),
            "status": page.get("status"),
            "imageUrl": page.get("imageUrl"),
            "pageFilePath": page.get("pageFilePath"),
            "imageFilePath": page.get("imageFilePath"),
            "height": page.get("height"),
            "width": page.get("width"),
            "dpiRes": page.get("dpiRes"),
            "scaledDpiRes": page.get("scaledDpiRes"),
            "startX": page.get("startX"),
            "startY": page.get("startY"),
            "endX": page.get("endX"),
            "endY": page.get("endY"),
            "optimizedImageUrl": page.get("optimizedImageUrl"),
            "rotation": page.get("rotation")
        }
        builtpages.append(structured_page)
    return builtpages
