import random
from typing import Tuple

from flask import Request
from sqlalchemy import asc, func

from app.db_models import Round, RoundLog, Stat, db
from app.helpers import get_or_create


def create_round(request: Request) -> Tuple[dict, int]:
    try:
        user_id = request.json['user_id']
    except KeyError as e:
        return {'error': f'{str(e)} is required.'}, 400
    try:
        round_obj = Round(user_id=user_id)
        stats = get_or_create(user_id=user_id)
        db.session.add(round_obj)
        stats.played_rounds += 1
        db.session.commit()
        db.session.refresh(round_obj)
        db.session.refresh(stats)
    except Exception as e:
        return {'error': str(e)}, 400
    return {'round_id': round_obj.id}, 201


def rotate_roulette(request: Request) -> Tuple[dict, int]:
    try:
        user_id = request.json['user_id']
        round_id = request.json['round_id']
    except KeyError as e:
        return {'error': f'{str(e)} is required.'}, 400
    try:
        round_obj = db.session.query(Round).get_or_404(round_id)
    except Exception as e:
        return {'error': str(e)}, 400
    if round_obj.user_id != user_id:
        return {'error': 'Wrong user_id for that round'}, 400
    if round_obj.jackpot:
        return {'error': 'Round finished, please start new round'}, 400
    cells = round_obj.available_cells.copy()
    if cells:
        value = random.choices(
            list(cells.keys()), weights=list(cells.values())
        )[0]
        cells.pop(value)
        round_obj.available_cells = cells
    else:
        value = 'JACKPOT'
        round_obj.jackpot = True
    log = get_or_create(user_id=round_obj.user_id, round_id=round_obj.id)
    values = log.selected_values.copy()
    values.append(value)
    log.selected_values = values
    db.session.commit()
    db.session.refresh(round_obj)
    db.session.refresh(log)
    return {'value': value}, 200


def get_stats() -> Tuple[dict, int]:
    rounds = (
        db.session.query(Stat.played_rounds)
        .distinct()
        .order_by(asc('played_rounds'))
        .all()
    )
    resp = []
    for round_num in rounds:
        resp.append(
            {
                'round_num': round_num[0],
                'total_players': db.session.query(Stat)
                .filter(Stat.played_rounds >= round_num[0])
                .count(),
            }
        )
    return {'stats': resp}, 200


def get_rating() -> Tuple[dict, int]:
    players = db.session.query(Stat).all()
    resp = []
    for row in players:
        values = (
            db.session.query(RoundLog.selected_values)
            .filter(RoundLog.user_id == row.user_id)
            .all()
        )
        avg = (
            sum([len(rotation[0]) for rotation in values]) / len(values)
            if values
            else 0.0
        )
        resp.append(
            {
                'user_id': row.user_id,
                'total_rounds': row.played_rounds,
                'avg_rotation_num': avg,
            }
        )
    return {'rating': resp}, 200
