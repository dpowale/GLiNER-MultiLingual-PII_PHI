"""
GLiNER MultiLingual PII and PHI Extraction Pipeline using urchade/gliner_multi_pii-v1 Model
FastAPI service for extracting PII/PHI entities from text
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import torch
from gliner import GLiNER
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model state
model_state = {}

# Supported PII/PHI entity types
SUPPORTED_ENTITIES = [
    "person",
    "organization", 
    "phone number",
    "address",
    "passport number",
    "email",
    "credit card number",
    "social security number",
    "health insurance id number",
    "date of birth",
    "mobile phone number",
    "bank account number",
    "medication",
    "cpf",
    "driver's license number",
    "tax identification number",
    "medical condition",
    "identity card number",
    "national id number",
    "ip address",
    "email address",
    "iban",
    "credit card cvv",
    "credit card expiration date",
    "pin",
    "security code",
    "medical record number",
    "license plate number",
    "insurance number"
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading GLiNER PII model...")
    try:
        model_state["model"] = GLiNER.from_pretrained("urchade/gliner_multi_pii-v1")
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise
    yield
    model_state.clear()

app = FastAPI(
    title="PII Extraction API",
    description="Extract PII/PHI entities from text using GLiNER",
    version="1.0.0",
    lifespan=lifespan
)


class ExtractionRequest(BaseModel):
    text: str = Field(..., description="Text to extract PII from")
    entities: Optional[List[str]] = Field(None, description="Specific entities to extract")
    threshold: float = Field(0.5, ge=0.0, le=1.0, description="Confidence threshold")
    flat_ner: bool = Field(True, description="Whether to use flat NER")

class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int
    score: float

class ExtractionResponse(BaseModel):
    entities: List[Entity]
    text: str
    entity_count: int
    entity_types: Dict[str, int]

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    supported_entities: List[str]

@app.get("/")
async def root():
    return {"message": "PII Extraction API", "docs": "/docs", "health": "/health"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy" if "model" in model_state else "unhealthy",
        model_loaded="model" in model_state,
        supported_entities=SUPPORTED_ENTITIES
    )

@app.get("/entities")
async def get_supported_entities():
    return SUPPORTED_ENTITIES

@app.post("/extract", response_model=ExtractionResponse)
async def extract_pii(request: ExtractionRequest):
    if "model" not in model_state:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    model = model_state["model"]
    entities_to_extract = request.entities or SUPPORTED_ENTITIES
    
    entities = model.predict_entities(
        request.text,
        entities_to_extract,
        threshold=request.threshold,
        flat_ner=request.flat_ner
    )
    
    formatted_entities = [
        Entity(text=e["text"], label=e["label"], start=e["start"], end=e["end"], score=e["score"])
        for e in entities
    ]
    
    entity_types = {}
    for entity in formatted_entities:
        entity_types[entity.label] = entity_types.get(entity.label, 0) + 1
    
    return ExtractionResponse(
        entities=formatted_entities,
        text=request.text,
        entity_count=len(formatted_entities),
        entity_types=entity_types
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
