from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Sample(Base):
    __tablename__ = "samples"
    
    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(String, unique=True, index=True, nullable=False)
    phenotype = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    variants = relationship("Variant", back_populates="sample")

class Variant(Base):
    __tablename__ = "variants"
    
    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(Integer, ForeignKey("samples.id"))
    chrom = Column(String, index=True)
    pos = Column(Integer)
    ref = Column(String)
    alt = Column(String)
    gene = Column(String, index=True)
    classification = Column(String, index=True) # e.g. Pathogenic
    
    # MongoDB reference ID (for complex annotation blobs)
    mongo_annotation_id = Column(String, nullable=True)
    
    sample = relationship("Sample", back_populates="variants")
