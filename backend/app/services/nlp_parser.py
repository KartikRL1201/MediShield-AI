import re
import spacy
from typing import List, Optional
from app.schemas.prescription import ExtractedMedicine, OCRResult

# Load the small English model
# Suppress the warning if the model is not found, but typically we ensure it's installed.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

from app.core.database import SessionLocal
from app.models.medicine import Medicine

KNOWN_MEDICINES = set()

def load_known_medicines():
    global KNOWN_MEDICINES
    try:
        db = SessionLocal()
        # Load all brand_names and generic_names into the set
        meds = db.query(Medicine.brand_name).all()
        for m in meds:
            if m[0]:
                KNOWN_MEDICINES.add(m[0].lower())
        db.close()
        print(f"NLP Parser loaded {len(KNOWN_MEDICINES)} medicines into memory.")
    except Exception as e:
        print(f"NLP Parser Warning: Could not load medicines from database: {e}")

# Load them immediately when this module is imported by FastAPI
load_known_medicines()

if not KNOWN_MEDICINES:
    # Fallback just in case the database is empty
    KNOWN_MEDICINES = {
        "amoxicillin", "amoxil", "ibuprofen", "advil", "omeprazole", "prilosec",
        "paracetamol", "tylenol", "metformin", "glucophage", "lisinopril", "atorvastatin"
    }

def parse_prescription_text(raw_text: str) -> OCRResult:
    """
    NLP-based parser that takes raw OCR string text and extracts structured medicine data.
    Uses spaCy for tokenization and Regex for pattern matching.
    """
    
    # 1. Preprocessing: Combine wrapped lines
    raw_lines = raw_text.split('\n')
    combined_lines = []
    current_line = ""
    for r in raw_lines:
        r = r.strip()
        if not r:
            continue
        # If line starts with a number (e.g. "1.") or a known medicine, treat it as a new prescription item
        first_word = r.lower().split()[0]
        first_word_clean = re.sub(r'[^a-z]', '', first_word)
        if re.match(r'^\d+[\.\)]', r) or first_word_clean in KNOWN_MEDICINES:
            if current_line:
                combined_lines.append(current_line)
            current_line = r
        else:
            current_line += " " + r
            
    if current_line:
        combined_lines.append(current_line)
        
    # If it failed to find numbered lists, fallback to standard split
    if not combined_lines:
        combined_lines = raw_lines

    extracted_medicines = []
    
    for raw_line in combined_lines:
        if not raw_line.strip():
            continue
            
        # Clean the combined line
        line = raw_line.lower()
        line = re.sub(r'[^a-z0-9\s\.\/]', ' ', line)
            
        line_doc = nlp(line)
        tokens = [token.text for token in line_doc]
        
        name = None
        dosage = None
        frequency = None
        duration = None
        instructions = None
        
        # 2. Medicine Name Extraction (Dictionary Lookup)
        for token in tokens:
            if token in KNOWN_MEDICINES:
                name = token.capitalize()
                break
                
        # If no known medicine found, we can try to guess the first noun, but for safety, we skip.
        if not name:
            # Simple heuristic: first word if it looks like a medicine name (length > 4, not a stop word)
            first_words = [t for t in line_doc if not t.is_stop and len(t.text) > 4 and t.is_alpha]
            if first_words:
                name = first_words[0].text.capitalize()
            else:
                continue # Skip lines that don't have a discernible medicine
                
        # 3. Dosage Extraction (RegEx)
        # Looks for patterns like "500mg", "10 ml", "2.5 g"
        dosage_match = re.search(r'\b(\d+(\.\d+)?\s*(mg|g|ml|mcg|tablet|cap|tabs))\b', line)
        if dosage_match:
            dosage = dosage_match.group(0).strip()
            
        # 4. Frequency Extraction (RegEx & Heuristics)
        freq_patterns = [
            r'\b(twice a day|b\.i\.d|bid|2x\/?day|2 times a day)\b',
            r'\b(once a day|q\.d|qd|1x\/?day|daily|once daily)\b',
            r'\b(three times a day|t\.i\.d|tid|3x\/?day)\b',
            r'\bevery \d+ hours\b',
            r'\b(as needed|prn)\b'
        ]
        for pattern in freq_patterns:
            match = re.search(pattern, line)
            if match:
                frequency = match.group(0).strip()
                break
                
        # 5. Duration Extraction (RegEx)
        duration_match = re.search(r'\bfor (\d+) (days|weeks|months)\b', line)
        if duration_match:
            duration = duration_match.group(0).strip()
            
        # 6. Instructions Extraction
        if "with food" in line or "after meals" in line:
            instructions = "Take with food"
        elif "empty stomach" in line or "before meals" in line or "before breakfast" in line:
            instructions = "Take on an empty stomach"
            
        # 7. Confidence Scoring
        score = 1.0
        if not dosage:
            score -= 0.2
        if not frequency:
            score -= 0.2
        if name.lower() not in KNOWN_MEDICINES:
            score -= 0.5 # Harsher penalty for unverified drug name
            
        # Ensure score doesn't drop below 0
        score = max(0.0, round(score, 2))
        
        med = ExtractedMedicine(
            name=name,
            dosage=dosage,
            frequency=frequency,
            duration=duration,
            instructions=instructions,
            confidence_score=score
        )
        extracted_medicines.append(med)
        
    return OCRResult(medicines=extracted_medicines, raw_text=raw_text)
