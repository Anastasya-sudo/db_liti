from sqlalchemy.orm import Session
from datetime import datetime
from create_db import Participant, Participation

# Получить список приглашенных на указанную дату первого приглашения
def get_invited_by_date(db: Session, invitation_date: str):
    date_obj = datetime.strptime(invitation_date, '%Y-%m-%d')
    return db.query(Participant).join(Participation).filter(Participation.first_invitation_date == date_obj).all()

# Получить список участников, которые заплатили в указанный период
def get_paid_participants_in_range(db: Session, start_date: str, end_date: str):
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    return db.query(Participant).join(Participation).filter(
        Participation.payment_date.between(start_date_obj, end_date_obj)
    ).all()

# Получить список тезисов докладов по городу
def get_reports_by_city(db: Session, city: str):
    return db.query(Participation.report_title).join(Participant).filter(Participant.city == city).all()

# Получить участников, которые нуждаются в гостинице для указанного города
def get_hotel_needs_by_city(db: Session, city: str):
    return db.query(Participant.surname, Participant.name, Participant.patronymic).join(Participation).filter(
        Participant.city == city, Participation.hotel_needed == True
    ).all()

# Добавить участника
def create_participant(db: Session, participant_data: dict):
    db_participant = Participant(**participant_data)
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

# Добавить участие для участника
def create_participation(db: Session, participant_id: int, participation_data: dict):
    db_participation = Participation(
        participant_id=participant_id,
        **participation_data
    )
    db.add(db_participation)
    db.commit()
    db.refresh(db_participation)
    return db_participation
