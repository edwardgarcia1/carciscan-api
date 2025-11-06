from sqlalchemy import Column, Integer, String, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Smiles(Base):
    """
    Represents the smiles table, mapping CIDs to SMILES strings.
    This will be our primary table for chemical identities.
    """
    __tablename__ = "smiles"

    # Using CID as the primary key for easy lookups and relationships
    cid = Column(BigInteger, primary_key=True, index=True)
    smiles = Column(String)

    # Establishing one-to-many relationships
    synonyms = relationship("Synonyms", back_populates="chemical")
    t3db_data = relationship("T3db", back_populates="chemical")


class Synonyms(Base):
    """
    Represents the synonyms table.
    """
    __tablename__ = "synonyms"

    # Define a composite primary key using the existing columns
    cid = Column(BigInteger, ForeignKey("smiles.cid"), primary_key=True)
    synonyms = Column(String, primary_key=True)

    # Establishing the many-to-one relationship back to the Smiles table
    chemical = relationship("Smiles", back_populates="synonyms")


class T3db(Base):
    """
    Represents the t3db table, containing toxicology data.
    """
    __tablename__ = "t3db"

    # The foreign key linking to the chemical identity
    cid = Column(Float, ForeignKey("smiles.cid"), primary_key=True) # Using Float as per schema

    # All the toxicological data fields
    categories = Column(String)
    route_of_exposure = Column(String)
    mechanism_of_toxicity = Column(String)
    metabolism = Column(String)
    lethal_dose = Column(String)
    carcinogenicity = Column(String)
    uses_sources = Column(String)
    minimum_risk_level = Column(String)
    health_effects = Column(String)
    symptoms = Column(String)
    treatment = Column(String)

    # Establishing the many-to-one relationship back to the Smiles table
    chemical = relationship("Smiles", back_populates="t3db_data")