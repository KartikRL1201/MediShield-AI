import itertools
import urllib.request
import urllib.parse
import json
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.interaction import DrugInteraction
from app.schemas.interaction import InteractionDetail, InteractionCheckResponse, DuplicateDetail
import collections
import re

def normalize_medicine_name(med: str) -> str:
    # 1. Strip dosages/units (e.g., 650, 500mg, 10 ml)
    med = re.sub(r'\b\d+(\.\d+)?\s*(mg|ml|mcg|g|ug|iu|%|v/v|w/v)?\b', '', med)
    # 2. Strip common release suffixes and modifiers
    med = re.sub(r'\b(xr|er|sr|dt|advance|plus|forte|ds|md|cr|pr)\b', '', med)
    # 3. Clean up formatting
    med = med.replace('-', ' ')
    med = re.sub(r'\s+', ' ', med).strip()
    return med

def check_interactions(medicines: List[str], db: Session, current_user=None) -> InteractionCheckResponse:
    if not medicines:
        return InteractionCheckResponse(interactions=[], duplicates=[], unknown_medicines=[], allergies_triggered=[], status="Safe")

    normalized_meds = [m.lower().strip() for m in medicines]
    
    # 0. MAP BRANDS TO GENERICS & TRACK UNKNOWNS
    generic_to_brands = collections.defaultdict(list)
    unknown_meds = []
    from app.models.medicine import Medicine
    for med in normalized_meds:
        # Step 1: Exact Match
        db_med = db.query(Medicine).filter(Medicine.brand_name == med).first()
        
        # Step 2: The Dosage Stripper
        stripped_med = None
        if not db_med:
            stripped_med = normalize_medicine_name(med)
            if stripped_med and stripped_med != med:
                db_med = db.query(Medicine).filter(Medicine.brand_name == stripped_med).first()
                
        # Step 3: Fuzzy LIKE Fallback
        if not db_med:
            search_term = stripped_med if stripped_med else med
            if search_term:
                db_med = db.query(Medicine).filter(Medicine.brand_name.like(f"{search_term}%")).first()

        if db_med and db_med.generic_name:
            generic_to_brands[db_med.generic_name.lower()].append(med)
        else:
            unknown_meds.append(med)
            generic_to_brands[med].append(med)
            
    generic_meds = list(generic_to_brands.keys())
    
    # Check for duplicates
    duplicates = []
    for gen, brands in generic_to_brands.items():
        if len(brands) > 1:
            duplicates.append(DuplicateDetail(generic_name=gen, brands_found=brands))
    
    # Generate all unique pairs using the generic names
    pairs = list(itertools.combinations(sorted(generic_meds), 2))
    
    # Check for allergies
    allergies_triggered = []
    if current_user and getattr(current_user, 'allergies', None):
        user_allergy_names = [a.generic_name.lower() for a in current_user.allergies]
        for gen in generic_meds:
            if gen in user_allergy_names and gen not in allergies_triggered:
                allergies_triggered.append(gen)
    
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
    if len(details) > 0 or len(allergies_triggered) > 0:
        status = "Dangerous"
    elif len(unknown_meds) > 0:
        status = "Unknown"
    else:
        status = "Safe"
        
    return InteractionCheckResponse(
        interactions=details,
        duplicates=duplicates,
        unknown_medicines=unknown_meds,
        allergies_triggered=allergies_triggered,
        status=status
    )
