from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey, MetaData
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "postgresql://stas:123@localhost:5438/my_db"  # Настройте это под свою базу

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Модель для участников
class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String, index=True)
    name = Column(String)
    patronymic = Column(String)
    academic_degree = Column(String)
    academic_title = Column(String)
    scientific_field = Column(String)
    workplace = Column(String)
    department = Column(String)
    position = Column(String)
    country = Column(String)
    city = Column(String)
    postal_code = Column(String)
    address = Column(String)
    work_phone = Column(String)
    home_phone = Column(String)
    email = Column(String, unique=True)

    participation = relationship("Participation", back_populates="participant")

# Модель для участия
class Participation(Base):
    __tablename__ = 'participations'

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    first_invitation_date = Column(Date)
    application_date = Column(Date)
    report_title = Column(String)
    thesis_received = Column(Boolean)
    second_invitation_date = Column(Date)
    payment_date = Column(Date)
    payment_amount = Column(Integer)
    arrival_date = Column(Date)
    departure_date = Column(Date)
    hotel_needed = Column(Boolean)

    participant_id = Column(Integer, ForeignKey('participants.id'))

    participant = relationship("Participant", back_populates="participation")

# Модель для пользователей (для разделения прав доступа)
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # "admin" или "user"



if __name__ == "__main__":
    Base.metadata.create_all(engine)