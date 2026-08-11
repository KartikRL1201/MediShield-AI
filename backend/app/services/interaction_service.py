import itertools
import urllib.request
import urllib.parse
import json
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.interaction import DrugInteraction
from app.schemas.interaction import InteractionDetail, InteractionCheckResponse

def check_interactions(medicines: List[str], db: Session) -> InteractionCheckResponse:
    if not medicines or len(medicines) < 2:
        return InteractionCheckResponse(interactions=[], unknown_medicines=[], status="Safe")

    normalized_meds = [m.lower().strip() for m in medicines]
    
    # 0. MAP BRANDS TO GENERICS & TRACK UNKNOWNS
    generic_meds = []
    unknown_meds = []
    from app.models.medicine import Medicine
    for med in normalized_meds:
        db_med = db.query(Medicine).filter(Medicine.brand_name == med).first()
        if db_med and db_med.generic_name:
            generic_meds.append(db_med.generic_name.lower())
        else:
            unknown_meds.append(med)
            generic_meds.append(med)
    
    # Generate all unique pairs using the generic names
    pairs = list(itertools.combinations(sorted(generic_meds), 2))
    
    details: List[InteractionDetail] = []
    
    for drug_a, drug_b in pairs:
        # STRICT LOCAL DATABASE CHECK (NIH API is deprecated)
        db_interaction = db.query(DrugInteraction).filter(
            and_(DrugInteraction.drug_a == drug_a, DrugInteraction.drug_b == drug_b)
        ).first()
        
        # Also check reverse order just in case
        if not db_interaction:
            db_interaction = db.query(DrugInteraction).filter(
                and_(DrugInteraction.drug_a == drug_b, DrugInteraction.drug_b == drug_a)
            ).first()
        
        if db_interaction and db_interaction.severity != "None":
            details.append(InteractionDetail(
                drug_a=drug_a.capitalize(),
                drug_b=drug_b.capitalize(),
                severity=db_interaction.severity,
                reason=db_interaction.reason,
                recommendation=db_interaction.recommendation
            ))
        
    # Evaluate the clinical status
    if len(details) > 0:
        status = "Dangerous"
    elif len(unknown_meds) > 0:
        status = "Unknown"
    else:
        status = "Safe"
        
    return InteractionCheckResponse(
        interactions=details,
        unknown_medicines=unknown_meds,
        status=status
    )
