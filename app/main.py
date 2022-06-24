from flask import request

from app import handlers, helpers


app = helpers.create_app()


@app.route('/new', methods=['POST'])
def new_round():
    return handlers.create_round(request)


@app.route('/rotate', methods=['POST'])
def rotate():
    return handlers.rotate_roulette(request)


@app.route('/stats', methods=['GET'])
def stats():
    return handlers.get_stats()


@app.route('/rating', methods=['GET'])
def rating():
    return handlers.get_rating()
