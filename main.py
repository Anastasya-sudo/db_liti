import app
import uvicorn
from fastapi import FastAPI, Request, Depends, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from create_db import Participant, Participation, SessionLocal  # Подключаем нужные модели и сессию
from functional import create_participant, create_participation, get_invited_by_date, get_paid_participants_in_range, \
    get_reports_by_city, get_hotel_needs_by_city
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# Подключаем Jinja2Templates для работы с HTML-шаблонами
templates = Jinja2Templates(directory="templates")


# Зависимость для получения сессии БД, которая используется в запросах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Главная страница
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/admin/participants/invited")
def invited_by_date(invitation_date: str, db: Session = Depends(get_db)):
    participants = get_invited_by_date(db, invitation_date)
    return templates.TemplateResponse("admin_dashboard.html", {"request": {}, "participants": participants})


@app.get("/participants/paid")
def paid_in_range(start_date: str, end_date: str, db: Session = Depends(get_db)):
    participants = get_paid_participants_in_range(db, start_date, end_date)
    return templates.TemplateResponse("admin_dashboard.html", {"request": {}, "participants": participants})

@app.get("/participants/reports")
def reports_by_city(city: str, db: Session = Depends(get_db)):
    participants = get_reports_by_city(db, city)
    return templates.TemplateResponse("admin_dashboard.html", {"request": {}, "participants": participants})


@app.get("/participants/hotel")
def hotel_needs(city: str, db: Session = Depends(get_db)):
    participants =  get_hotel_needs_by_city(db, city)
    return templates.TemplateResponse("admin_dashboard.html", {"request": {}, "participants": participants})

# Панель администратора
@app.get("/admin", response_class=HTMLResponse)
def get_admin_dashboard(request: Request, db: Session = Depends(get_db)):
    participants = db.query(Participant).all()
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "participants": participants})


# Панель пользователя
@app.get("/user", response_class=HTMLResponse)
async def get_user_dashboard(email, db: Session = Depends(get_db)):
    user = db.query(Participant).filter(Participant.email==email).first()
    if not user:
        return HTMLResponse(content="Пользователь с таким email не найден.", status_code=404)
    return templates.TemplateResponse("user_dashboard.html", {"request": {}, "participant": user})


# Добавить участника
@app.post("/admin/add_participant", response_class=HTMLResponse)
def add_participant(request: Request, surname: str = Form(...), name: str = Form(...), patronymic: str = Form(...),
                    academic_degree: str = Form(None), academic_title: str = Form(None),
                    scientific_field: str = Form(None),
                    workplace: str = Form(None), department: str = Form(None), position: str = Form(None),
                    country: str = Form(None), city: str = Form(None), postal_code: str = Form(None),
                    address: str = Form(None), work_phone: str = Form(None), home_phone: str = Form(None),
                    email: str = Form(None), db: Session = Depends(get_db)):

    user = db.query(Participant).filter(Participant.email==email).first()
    if not user:
        # Создаем нового участника
        new_participant = Participant(surname=surname, name=name, patronymic=patronymic,
                                      academic_degree=academic_degree, academic_title=academic_title,
                                      scientific_field=scientific_field, workplace=workplace,
                                      department=department, position=position, country=country, city=city,
                                      postal_code=postal_code, address=address, work_phone=work_phone,
                                      home_phone=home_phone, email=email)
        db.add(new_participant)
        db.commit()
        db.refresh(new_participant)

    # После добавления участника, возвращаем страницу с админ-панелью
    participants = db.query(Participant).all()
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "participants": participants})


# Добавить участие для участника
"""@app.post("/admin/add_participation/{participant_id}", response_class=HTMLResponse)
def add_participation(request: Request, participant_id: int, role: str = Form(...),
                      first_invitation_date: str = Form(...),
                      report_title: str = Form(None), hotel_needed: bool = Form(False), payment_date: str = Form(None),
                      db: Session = Depends(get_db)):
    # Создаем запись о участии
    participation = Participation(participant_id=participant_id, role=role, first_invitation_date=first_invitation_date,
                                  report_title=report_title, hotel_needed=hotel_needed, payment_date=payment_date)
    db.add(participation)
    db.commit()
    db.refresh(participation)

    # После добавления участия, возвращаем страницу с админ-панелью
    participants = db.query(Participant).all()
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "participants": participants})
"""

@app.post("/admin/add_participation/", response_class=HTMLResponse)
def add_participation(
    request: Request,
    participant_id:str =Form(None),
    role: str = Form(...),
    first_invitation_date: str = Form(...),
    application_date: str = Form(None),
    report_title: str = Form(None),
    thesis_received: bool = Form(False),
    second_invitation_date: str = Form(None),
    payment_date: str = Form(None),
    payment_amount: float = Form(None),
    arrival_date: str = Form(None),
    departure_date: str = Form(None),
    hotel_needed: bool = Form(False),
    db: Session = Depends(get_db)
):
    #parcipant =
    # Создаем запись о участии
    participation = Participation(
        participant_id=str(participant_id),
        role=role,
        first_invitation_date=first_invitation_date,
        application_date=application_date,
        report_title=report_title,
        thesis_received=thesis_received,
        second_invitation_date=second_invitation_date,
        payment_date=payment_date,
        payment_amount=payment_amount,
        arrival_date=arrival_date,
        departure_date=departure_date,
        hotel_needed=hotel_needed,
        participant=db.query(Participant).filter(Participant.id == int(participant_id)).first()
    )
    db.add(participation)
    db.commit()
    db.refresh(participation)

    # После добавления участия, возвращаем страницу с админ-панелью
    participants = db.query(Participant).all()
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "participants": participants})



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)