from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from draft import smart_response_generation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Chatbot/Mailtools Service",
    root_path="/api/convomail",  
    docs_url="/swagger",         
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailInput(BaseModel):
    text: str


@app.get("/health", include_in_schema=False)
def health():
    return {"ok": True}

@app.post("/replies")
def generate_replies(request: Request, body: EmailInput):
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Text is required for generating replies.")
    replies = smart_response_generation(body.text)
    if not replies:
        raise HTTPException(status_code=500, detail="Failed to generate replies.")
    return {"response": replies}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)