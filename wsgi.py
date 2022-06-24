from app.main import app


if __name__ == '__main__':
    try:
        app.run()
    except Exception:
        raise
