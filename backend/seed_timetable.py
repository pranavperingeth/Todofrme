from app.database import SessionLocal
from app.models import TimetableEntry

entries = [
    # Monday
    {"day_of_week": "monday", "subject": "MA2002E: Maths-III [MAT3]", "start_time": "09:00", "end_time": "09:50", "room": "ELHC-402"},
    {"day_of_week": "monday", "subject": "CS2001E: DSA [AVP]", "start_time": "10:00", "end_time": "10:50", "room": "ELHC-402"},
    {"day_of_week": "monday", "subject": "CS2002E: Comp. Org. [TMS]", "start_time": "12:00", "end_time": "12:50", "room": "ELHC-402"},
    
    # Tuesday
    {"day_of_week": "tuesday", "subject": "CS2001E: DSA [AVP]", "start_time": "09:00", "end_time": "09:50", "room": "ELHC-402"},
    {"day_of_week": "tuesday", "subject": "CS2002E: Comp. Org. [TMS]", "start_time": "11:00", "end_time": "11:50", "room": "ELHC-402"},
    {"day_of_week": "tuesday", "subject": "IE2001E: Innov & Entrep [IE-3]", "start_time": "12:00", "end_time": "12:50", "room": "ELHC-402"},

    # Wednesday
    {"day_of_week": "wednesday", "subject": "CS2002E: Comp. Org. [TMS]", "start_time": "10:00", "end_time": "10:50", "room": "ELHC-402"},
    {"day_of_week": "wednesday", "subject": "IE2001E: Innov & Entrep [IE-3]", "start_time": "11:00", "end_time": "11:50", "room": "ELHC-402"},
    {"day_of_week": "wednesday", "subject": "MA2002E: Maths-III [MAT3]", "start_time": "12:00", "end_time": "12:50", "room": "ELHC-402"},
    {"day_of_week": "wednesday", "subject": "CS2091E: DSA Lab [AVP, SW]", "start_time": "14:00", "end_time": "16:50", "room": "BDL"},

    # Thursday
    {"day_of_week": "thursday", "subject": "CS2002E: Comp. Org. [TMS]", "start_time": "09:00", "end_time": "09:50", "room": "ELHC-402"},
    {"day_of_week": "thursday", "subject": "IE2001E: Innov & Entrep [IE-3]", "start_time": "10:00", "end_time": "10:50", "room": "ELHC-402"},
    {"day_of_week": "thursday", "subject": "MA2002E: Maths-III [MAT3]", "start_time": "11:00", "end_time": "11:50", "room": "ELHC-402"},
    {"day_of_week": "thursday", "subject": "CS2001E: DSA [AVP]", "start_time": "12:00", "end_time": "12:50", "room": "ELHC-402"},
    {"day_of_week": "thursday", "subject": "CS2092E: Hardware Lab [TMS]", "start_time": "14:00", "end_time": "16:50", "room": "BDL"},

    # Friday
    {"day_of_week": "friday", "subject": "IE2001E: Innov & Entrep [IE-3]", "start_time": "09:00", "end_time": "09:50", "room": "ELHC-402"},
    {"day_of_week": "friday", "subject": "MA2002E: Maths-III [MAT3]", "start_time": "10:00", "end_time": "10:50", "room": "ELHC-402"},
    {"day_of_week": "friday", "subject": "CS2001E: DSA [AVP]", "start_time": "11:00", "end_time": "11:50", "room": "ELHC-402"},
]

def seed_db():
    with SessionLocal() as session:
        # Clear existing
        session.query(TimetableEntry).delete()
        
        # Add new
        for entry in entries:
            new_entry = TimetableEntry(
                user_id="b30f1c9e-60d1-4795-8265-82756643224a",
                day_of_week=entry["day_of_week"],
                subject=entry["subject"],
                start_time=entry["start_time"],
                end_time=entry["end_time"],
                room=entry["room"]
            )
            session.add(new_entry)
        
        session.commit()
        print("Successfully seeded timetable database synchronously!")

if __name__ == "__main__":
    seed_db()
