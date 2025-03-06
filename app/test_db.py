from sqlalchemy.orm import Session
from app.config import SessionLocal, Base, engine
from app.models.models import User, EHR

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create a session
db: Session = SessionLocal()

try:
    # 1️⃣ Create a new user with all required details
    new_user = User(
        username="testuser",
        email="test@example.com",
        password="securepass",
        role="doctor",  # ✅ Explicitly setting role
        phone_number="1234567890"  # ✅ Providing phone number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"✅ User added: ID={new_user.user_id}, Username={new_user.username}, Email={new_user.email}, Role={new_user.role}, Phone={new_user.phone_number}")

    # 2️⃣ Add an EHR record for the user with all required fields
    new_ehr = EHR(
        record_id=1,  # ✅ Explicitly providing record_id
        patient_id=new_user.user_id,  # ✅ Setting ForeignKey reference
        diagnosis="Flu",
        treatment="Rest and hydration",
        notes="Follow up in a week"
    )
    db.add(new_ehr)
    db.commit()
    db.refresh(new_ehr)
    print(f"✅ EHR added: Record ID={new_ehr.record_id}, Patient ID={new_ehr.patient_id}, Diagnosis={new_ehr.diagnosis}, Treatment={new_ehr.treatment}, Notes={new_ehr.notes}")

    # 3️⃣ Fetch the user and check EHRs
    user_with_ehrs = db.query(User).filter(User.user_id == new_user.user_id).first()
    print(f"🩺 {user_with_ehrs.username}'s EHRs:")
    for ehr in user_with_ehrs.ehrs:
        print(f"   - Record ID={ehr.record_id}, Diagnosis={ehr.diagnosis}, Treatment={ehr.treatment}, Notes={ehr.notes}")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    db.close()
