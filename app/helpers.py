import os
from typing import Optional, Union

from flask import Flask

from app.db_models import RoundLog, Stat, db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "default")
    app.config['SQLALCHEMY_DATABASE_URI'] = ''.join(
        (
            f"postgresql://{os.environ['POSTGRES_USER']}:",
            f"{os.environ['POSTGRES_PASSWORD']}@db:5432/",
            f"{os.environ['POSTGRES_DB']}",
        )
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    return app


def get_or_create(
    user_id: int, round_id: Optional[int] = None
) -> Union[Stat, RoundLog]:
    if round_id:
        obj = (
            db.session.query(RoundLog)
            .filter(RoundLog.round_id == round_id, RoundLog.user_id == user_id)
            .first()
        )
    else:
        obj = db.session.query(Stat).filter(Stat.user_id == user_id).first()
    if obj:
        return obj
    if round_id:
        obj = RoundLog(round_id=round_id, user_id=user_id)
    else:
        obj = Stat(user_id=user_id)
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)
    return obj
