from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.reminder import MedicineSchedule, DoseLog, DoseStatusEnum
from app.schemas.reminder import ScheduleCreate, DoseLogUpdate

def create_schedule(db: Session, user_id: str, schedule_data: ScheduleCreate) -> MedicineSchedule:
    db_schedule = MedicineSchedule(
        user_id=user_id,
        medicine_name=schedule_data.medicine_name,
        dosage=schedule_data.dosage,
        frequency=schedule_data.frequency,
        time_of_day=schedule_data.time_of_day
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def get_or_generate_todays_logs(db: Session, user_id: str):
    """
    1. Fetches all active schedules for the user.
    2. Checks if a DoseLog exists for today for each schedule.
    3. If not, generates one.
    4. Evaluates pending doses to see if they are >1 hour late -> marks as MISSED.
    5. Returns all logs for today.
    """
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    
    schedules = db.query(MedicineSchedule).filter(MedicineSchedule.user_id == user_id).all()
    
    for schedule in schedules:
        # Simple daily logic for MVP
        # In a full app, we'd check if today matches the 'weekly' or 'custom' logic.
        
        # Check if a log already exists for today
        existing_log = db.query(DoseLog).filter(
            DoseLog.schedule_id == schedule.id,
            DoseLog.scheduled_for >= today_start,
            DoseLog.scheduled_for < today_end
        ).first()
        
        if not existing_log:
            # Parse time_of_day (e.g. "08:00")
            try:
                hour, minute = map(int, schedule.time_of_day.split(':'))
                scheduled_time = today_start.replace(hour=hour, minute=minute)
                
                new_log = DoseLog(
                    schedule_id=schedule.id,
                    scheduled_for=scheduled_time,
                    status=DoseStatusEnum.PENDING
                )
                db.add(new_log)
            except ValueError:
                continue # Bad time format
                
    db.commit()
    
    # Now, evaluate all pending logs for today (and past) to mark them as missed if > 1 hour late
    all_pending_logs = db.query(DoseLog).join(MedicineSchedule).filter(
        MedicineSchedule.user_id == user_id,
        DoseLog.status == DoseStatusEnum.PENDING
    ).all()
    
    for log in all_pending_logs:
        if now > log.scheduled_for + timedelta(hours=1):
            log.status = DoseStatusEnum.MISSED
            
    db.commit()
    
    # Fetch today's logs to return to frontend
    todays_logs = db.query(DoseLog).join(MedicineSchedule).filter(
        MedicineSchedule.user_id == user_id,
        DoseLog.scheduled_for >= today_start,
        DoseLog.scheduled_for < today_end
    ).order_by(DoseLog.scheduled_for.asc()).all()
    
    return todays_logs

def update_dose_status(db: Session, user_id: str, log_id: str, update_data: DoseLogUpdate) -> DoseLog:
    log = db.query(DoseLog).join(MedicineSchedule).filter(
        DoseLog.id == log_id,
        MedicineSchedule.user_id == user_id
    ).first()
    
    if not log:
        raise ValueError("Dose log not found or unauthorized.")
        
    log.status = update_data.status
    log.action_taken_at = datetime.utcnow()
    
    if update_data.status == DoseStatusEnum.SNOOZED and update_data.snooze_minutes:
        # Push the scheduled_for forward by snooze_minutes, and set back to pending
        log.scheduled_for = log.scheduled_for + timedelta(minutes=update_data.snooze_minutes)
        log.status = DoseStatusEnum.PENDING
        
    db.commit()
    db.refresh(log)
    return log

def calculate_adherence(db: Session, user_id: str):
    """
    Adherence = Taken / (Taken + Skipped + Missed) * 100
    Snoozed/Pending are ignored from the denominator until resolved or missed.
    """
    logs = db.query(DoseLog).join(MedicineSchedule).filter(
        MedicineSchedule.user_id == user_id,
        DoseLog.status.in_([DoseStatusEnum.TAKEN, DoseStatusEnum.SKIPPED, DoseStatusEnum.MISSED])
    ).all()
    
    total = len(logs)
    if total == 0:
        return {
            "total_scheduled": 0,
            "total_taken": 0,
            "total_missed": 0,
            "adherence_percentage": 100.0
        }
        
    taken = sum(1 for log in logs if log.status == DoseStatusEnum.TAKEN)
    missed_skipped = total - taken
    
    return {
        "total_scheduled": total,
        "total_taken": taken,
        "total_missed": missed_skipped,
        "adherence_percentage": round((taken / total) * 100, 2)
    }
