from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models
from .database import engine, get_db, annotations_collection

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="VarPipe-Dx API", description="Clinical Variant Query API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to VarPipe-Dx API"}

@app.get("/samples")
def get_samples(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    samples = db.query(models.Sample).offset(skip).limit(limit).all()
    return samples

@app.get("/variants")
def get_variants(gene: str = None, classification: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Variant)
    if gene:
        query = query.filter(models.Variant.gene == gene)
    if classification:
        query = query.filter(models.Variant.classification == classification)
    return query.limit(100).all()

@app.get("/variants/{variant_id}/annotations")
def get_variant_annotations(variant_id: int, db: Session = Depends(get_db)):
    variant = db.query(models.Variant).filter(models.Variant.id == variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
        
    if not variant.mongo_annotation_id or annotations_collection is None:
        return {"message": "No detailed annotations found or MongoDB not connected."}
        
    # Fetch from MongoDB
    annotation = annotations_collection.find_one({"_id": variant.mongo_annotation_id})
    if annotation:
        annotation["_id"] = str(annotation["_id"])
    return annotation
