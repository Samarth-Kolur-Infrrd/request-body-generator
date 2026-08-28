from fastapi import FastAPI,Body
import uvicorn

from generator import generateRequestBody

app = FastAPI()

@app.get("/requestGenerator/{document_id}")
async def requestgenerator(document_id: str):
    inputId = {"documentId": document_id}
    outputRequest = generateRequestBody(inputId)
    return outputRequest

if "__main__" == __name__:
    uvicorn.run(app)