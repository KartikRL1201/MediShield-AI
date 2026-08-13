import sys
import os
sys.path.append(os.path.abspath('.'))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.reminder import MedicineSchedule, FrequencyEnum
from app.core.security import get_password_hash

def seed_db():
    db = SessionLocal()
    
    users = db.query(User).all()
    if not users:
        print("No users found.")
        db.close()
        return

    for user in users:
        schedules = db.query(MedicineSchedule).filter(MedicineSchedule.user_id == str(user.id)).all()
        if len(schedules) == 0:
            s1 = MedicineSchedule(
                user_id=str(user.id),
                medicine_name="Amoxicillin 500mg",
                dosage="1 tablet",
                frequency=FrequencyEnum.DAILY,
                time_of_day="08:00"
            )
            s2 = MedicineSchedule(
                user_id=str(user.id),
                medicine_name="Dolo 650",
                dosage="1 tablet",
                frequency=FrequencyEnum.DAILY,
                time_of_day="13:00"
            )
            s3 = MedicineSchedule(
                user_id=str(user.id),
                medicine_name="Amoxicillin 500mg",
                dosage="1 tablet",
                frequency=FrequencyEnum.DAILY,
                time_of_day="20:00"
            )
            db.add_all([s1, s2, s3])
            print(f"Created 3 default schedules for {user.email}")
        else:
            print(f"Schedules already exist for {user.email}")
            
    db.commit()
    db.close()
    
if __name__ == "__main__":
    seed_db()
