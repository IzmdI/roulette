from flask_sqlalchemy import SQLAlchemy


CELLS = {
    1: 20,
    2: 100,
    3: 45,
    4: 70,
    5: 15,
    6: 140,
    7: 20,
    8: 20,
    9: 140,
    10: 45,
}
db = SQLAlchemy()


class Round(db.Model):
    __tablename__ = 'rounds'

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, index=True)
    available_cells = db.Column(db.PickleType, default=CELLS)
    jackpot = db.Column(db.Boolean, default=False)


class RoundLog(db.Model):
    __tablename__ = 'round_logs'

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, index=True)
    round_id = db.Column(db.Integer, db.ForeignKey('rounds.id'), index=True)
    selected_values = db.Column(db.PickleType, default=[])


class Stat(db.Model):
    __tablename__ = 'stats'

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, index=True)
    played_rounds = db.Column(db.Integer, default=0, index=True)
