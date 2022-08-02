from flask import make_response, abort, request
from config import db
from models import Movie, Theater, TheaterSchema, TheaterShowSchema, MovieTheater


def read_all():
    theater_name = request.args.get("name", type=str)

    if theater_name is not None:
        return db.session.query(Movie.movie_name).join(MovieTheater).join(Theater).filter(
            Theater.theater_name == theater_name).all()

    else:
        theaters = Theater.query.order_by(db.desc(Theater.theater_id)).all()

        theater_schema = TheaterSchema(many=True)
        data = theater_schema.dump(theaters).data
        return data


def read_one(theater_id):
    theater = (
        Theater.query.filter(Theater.theater_id == theater_id)
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

    schema = TheaterShowSchema()
    new_theater_data = schema.load(theater, session=db.session).data

    movie.theaters.append(new_theater_data)
    db.session.commit()

    data = schema.dump(new_theater_data).data

    return data, 201


def add_existing(movie_id, theater_id):
    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()
    theater = Theater.query.filter(Theater.theater_id == theater_id).one_or_none()

    if movie is None:
        abort(404, f"Movie not found for Id: {movie_id}")

    elif theater is None:
        abort(404, f"Theater not found for Id: {theater_id}")

    movie.theaters.append(theater)
    db.session.commit()

    return 201


def update(theater_id, theater):
    update_theater = (
        Theater.query.filter(Theater.theater_id == theater_id)
        .one_or_none()
    )

    if update_theater is not None:

        schema = TheaterSchema()
        update = schema.load(theater, session=db.session).data

        update.theater_id = update_theater.theater_id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_theater).data

        return data, 200

    else:
        abort(404, f"Theater not found for Id: {theater_id}")


def delete(theater_id):
    theater = (
        Theater.query.filter(Theater.theater_id == theater_id)
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
