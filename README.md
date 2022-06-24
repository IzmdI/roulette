# Roulette

This is a simple service, which allows to spin roulette and store statistics.  

## Before Started

You will need [Docker](https://docs.docker.com/get-docker/) to run it. Install last version depending from your OS. After installation just clone this repository.

### Starting

First, open a `.env.example` file, set some variables and save it as `.env` without `.example` extension.  
IMPORTANT: Make your own unique secret variables.

```
# Application secret key
SECRET_KEY=<YOUR_SECRET_KEY>
# Database config
POSTGRES_USER=system_admin  //set own
POSTGRES_PASSWORD=<YOUR_DB_PASSWORD>
POSTGRES_DB=roulette
```

Start building and setting up.

```
docker-compose up
```

Service will accessible locally at 8000 port.

```
localhost:8000
```

The following endpoints are available.  
* `/new`  
    * POST - create round
        * Required json-data:
           * user_id: integer
        * Returning json-data:
           * round_id: integer
* `/rotate`
    * POST - spin roulette
        * Required json-data:
           * user_id: integer
           * round_id: integer
        * Returning json-data:
           * value: integer or string (if jackpot)
* `/stats`  
    * GET - get statistics
        * Returning json-data:
           * list with round numbers and number of players
* `/rating`  
    * GET - get rating
        * Returning json-data:
           * list with user_id, total played rounds, average number of rotations

## Built With

* [Flask](https://palletsprojects.com/p/flask/) - lightweight WSGI web application framework
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - extension for Flask that adds support for [SQLAlchemy](https://www.sqlalchemy.org/)
* [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) - service for web-applications hosting
* [Docker](https://www.docker.com/) - Containerized system

## Author

* **[Andrew Smelov](https://github.com/IzmdI)**

## License

This project is licensed under the MIT License - see the LICENSE.md file for details  
