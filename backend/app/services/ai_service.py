import re
from sqlalchemy.orm import Session
from google import genai
from google.genai import types
from app.core.config import settings
from app.models.medicine import Medicine
from app.services.interaction_service import normalize_medicine_name

def fetch_medicine_context(medicines: list[str], db: Session) -> str:
    """Retrieves medicine details from the DB to build the RAG knowledge base."""
    context_lines = []
    
    for med in medicines:
        med = med.lower().strip()
        db_med = db.query(Medicine).filter(Medicine.brand_name == med).first()
        
        # Fallback to normalized matching
        if not db_med:
            stripped_med = normalize_medicine_name(med)
            if stripped_med and stripped_med != med:
                db_med = db.query(Medicine).filter(Medicine.brand_name == stripped_med).first()
        
        # Fuzzy fallback
        if not db_med:
            search_term = normalize_medicine_name(med) or med
            if search_term:
                db_med = db.query(Medicine).filter(Medicine.brand_name.like(f"{search_term}%")).first()
                
        if db_med:
            context_lines.append(f"--- Information for {db_med.brand_name.upper()} (Generic: {db_med.generic_name}) ---")
            if db_med.composition:
                context_lines.append(f"Composition: {db_med.composition}")
            if db_med.side_effects:
                context_lines.append(f"Side Effects: {db_med.side_effects}")
            if db_med.food_interactions:
                context_lines.append(f"Food Interactions: {db_med.food_interactions}")
            if db_med.alcohol_interaction:
                context_lines.append(f"Alcohol Interactions: {db_med.alcohol_interaction}")
            if db_med.pregnancy_warning:
                context_lines.append(f"Pregnancy Warning: {db_med.pregnancy_warning}")
            if db_med.prescription_required is not None:
                context_lines.append(f"Prescription Required: {'Yes' if db_med.prescription_required else 'No'}")
        else:
            context_lines.append(f"--- Information for {med.upper()} ---")
            context_lines.append("No reliable clinical information found in the database for this medicine.")
            
    context_lines.append("\n--- KNOWN DRUG INTERACTIONS ---")
    if len(medicines) > 1:
        from app.models.interaction import DrugInteraction
        from itertools import combinations
        
        # Get normalized generic names for the interaction check
        generics = []
        for med in medicines:
            med = med.lower().strip()
            db_med = db.query(Medicine).filter(Medicine.brand_name == med).first()
            if not db_med:
                db_med = db.query(Medicine).filter(Medicine.brand_name == (normalize_medicine_name(med) or "")).first()
            if not db_med:
                db_med = db.query(Medicine).filter(Medicine.brand_name.like(f"{(normalize_medicine_name(med) or med)}%")).first()
            
            if db_med and db_med.generic_name:
                generics.append(db_med.generic_name.lower())
                
        generics = list(set(generics))
        interactions_found = False
        
        for drug_a, drug_b in combinations(generics, 2):
            interaction = db.query(DrugInteraction).filter(
                ((DrugInteraction.drug_a == drug_a) & (DrugInteraction.drug_b == drug_b)) |
                ((DrugInteraction.drug_a == drug_b) & (DrugInteraction.drug_b == drug_a))
            ).first()
            
            if interaction:
                interactions_found = True
                context_lines.append(f"Interaction between {drug_a.upper()} and {drug_b.upper()}:")
                context_lines.append(f"Severity: {interaction.severity}")
                context_lines.append(f"Reason: {interaction.reason}")
                if interaction.recommendation:
                    context_lines.append(f"Recommendation: {interaction.recommendation}")
                    
        if not interactions_found:
            context_lines.append("No known interactions between these medicines in the database.")
            
    return "\n".join(context_lines)

def ask_medical_question(medicines: list[str], query: str, db: Session) -> str:
    if not settings.GEMINI_API_KEY:
        return "System Error: GEMINI_API_KEY is not configured."
        
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    knowledge_base = fetch_medicine_context(medicines, db)
    
    system_instruction = """
    You are an expert clinical pharmacist assistant. 
    Your ONLY purpose is to answer the user's query using strictly the 'Knowledge Base' provided below.
    
    CRITICAL RULES:
    1. DO NOT make any medical decisions, diagnoses, or tell the user to stop/start taking medication.
    2. Simplify complex medical jargon into plain, concise language.
    3. Be concise but ensure all meaningful points from the database are conveyed.
    4. If the user asks about an interaction or multiple medicines (e.g. "both of these"), but the Knowledge Base only contains one medicine, politely inform them that they only provided one medicine and you need the other to check for interactions.
    5. If the information to answer the user's question is completely missing from the Knowledge Base, reply exactly with: "I do not have enough information to answer that based on the available clinical data."
    6. NEVER hallucinate or pull in external medical knowledge beyond what is provided in the Knowledge Base.
    """
    
    prompt = f"""
    Knowledge Base:
    {knowledge_base}
    
    User Query: {query}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2, # Keep it highly deterministic
            )
        )
        return response.text
    except Exception as e:
        return f"Error contacting AI service: {str(e)}"
