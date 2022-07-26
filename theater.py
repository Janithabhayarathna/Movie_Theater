from flask import make_response, abort
from config import db
from models import Movie, Theater, TheaterSchema


def read_all():

    theaters = Theater.query.order_by(db.desc(Theater.theater_name)).all()

    theater_schema = TheaterSchema(many=True, exclude=["movie.theaters"])
    data = theater_schema.dump(theaters).data
    return data


def read_one(movie_id, theater_id):

    theater = (
        Theater.query.join(Movie, Movie.movie_id == Theater.movie_id)
        .filter(Theater.movie_id == movie_id)
        .filter(Theater.theater_id == theater_id)
        .one_or_none()
    )

    if theater is not None:
        theater_schema = TheaterSchema()
        data = theater_schema.dump(theater).data
        return data

    else:
        abort(404, f"Theater not found for Id: {theater_id}")


def create(movie_id, theater):

    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()

    if movie is None:
        abort(404, f"Movie not found for Id: {movie_id}")

    schema = TheaterSchema()
    new_theater = schema.load(theater, session=db.session).data

    movie.theaters.append(new_theater)
    db.session.commit()

    data = schema.dump(new_theater).data

    return data, 201


def update(movie_id, theater_id, theater):

    update_theater = (
        Theater.query.filter(Theater.movie_id == movie_id)
        .filter(Theater.theater_id == theater_id)
        .one_or_none()
    )

    if update_theater is not None:

        schema = TheaterSchema()
        update = schema.load(theater, session=db.session).data

        update.movie_id = update_theater.movie_id
        update.theater_id = update_theater.theater_id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_theater).data

        return data, 200

    else:
        abort(404, f"Theater not found for Id: {theater_id}")


def delete(movie_id, theater_id):

    theater = (
        Theater.query.filter(Movie.movie_id == movie_id)
        .filter(Theater.theater_id == theater_id)
        .one_or_none()
    )

    if theater is not None:
        db.session.delete(theater)
        db.session.commit()
        return make_response(
            "Theater {theater_id} deleted".format(theater_id=theater_id), 200
        )

    else:
        abort(404, f"Theater not found for Id: {theater_id}")
