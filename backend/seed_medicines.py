import sys
import os

# Add the backend directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.crud.crud_medicine import create_medicine
from app.schemas.medicine import MedicineCreate

def seed_database():
    db = SessionLocal()
    
    medicines = [
        MedicineCreate(
            brand_name="Tylenol",
            generic_name="Paracetamol",
            composition="Acetaminophen 500mg",
            strength="500mg",
            manufacturer="Johnson & Johnson",
            side_effects="Nausea, stomach pain, loss of appetite, itching, rash, headache, dark urine",
            food_interactions="Can be taken with or without food.",
            alcohol_interaction="Severe. Avoid alcohol. May increase risk of liver damage.",
            pregnancy_warning="Generally considered safe, but consult a doctor.",
            storage="Store at room temperature away from moisture and heat.",
            prescription_required=False
        ),
        MedicineCreate(
            brand_name="Advil",
            generic_name="Ibuprofen",
            composition="Ibuprofen 200mg",
            strength="200mg",
            manufacturer="Pfizer",
            side_effects="Upset stomach, mild heartburn, nausea, vomiting, bloating, gas, diarrhea, constipation",
            food_interactions="Take with food or milk to prevent stomach upset.",
            alcohol_interaction="Moderate. Avoid alcohol. May increase risk of stomach bleeding.",
            pregnancy_warning="Avoid during the last 3 months of pregnancy.",
            storage="Store at room temperature away from moisture and heat.",
            prescription_required=False
        ),
        MedicineCreate(
            brand_name="Amoxil",
            generic_name="Amoxicillin",
            composition="Amoxicillin 500mg",
            strength="500mg",
            manufacturer="GlaxoSmithKline",
            side_effects="Nausea, vomiting, diarrhea, rash",
            food_interactions="Can be taken with or without food. Space doses evenly.",
            alcohol_interaction="Mild. Does not interact directly, but alcohol may delay recovery.",
            pregnancy_warning="Generally considered safe during pregnancy.",
            storage="Store capsules at room temperature. Liquid suspensions should be refrigerated.",
            prescription_required=True
        ),
        MedicineCreate(
            brand_name="Prilosec",
            generic_name="Omeprazole",
            composition="Omeprazole 20mg",
            strength="20mg",
            manufacturer="Procter & Gamble",
            side_effects="Headache, abdominal pain, nausea, diarrhea, vomiting, flatulence",
            food_interactions="Take before a meal, preferably in the morning.",
            alcohol_interaction="Mild. Does not directly interact, but alcohol can worsen acid reflux.",
            pregnancy_warning="Use only if the potential benefit justifies the potential risk.",
            storage="Store at room temperature away from moisture and heat.",
            prescription_required=False
        ),
        MedicineCreate(
            brand_name="Glucophage",
            generic_name="Metformin",
            composition="Metformin Hydrochloride 500mg",
            strength="500mg",
            manufacturer="Merck",
            side_effects="Nausea, vomiting, stomach upset, diarrhea, weakness, or a metallic taste in the mouth",
            food_interactions="Take with meals to reduce stomach/bowel side effects.",
            alcohol_interaction="Severe. Avoid alcohol. May increase the risk of lactic acidosis.",
            pregnancy_warning="Generally considered safe, insulin is often preferred.",
            storage="Store at room temperature away from light and moisture.",
            prescription_required=True
        )
    ]

    print("Seeding medicines into the database...")
    for med in medicines:
        try:
            create_medicine(db, med)
            print(f"Added {med.brand_name} ({med.generic_name})")
        except Exception as e:
            print(f"Error adding {med.brand_name}: {e}")
            
    db.close()
    print("Seeding complete!")

if __name__ == "__main__":
    seed_database()
