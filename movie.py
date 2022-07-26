from flask import make_response, abort
from config import db
from models import Movie, MovieSchema, Theater


def read_all():

    movie = Movie.query.order_by(Movie.movie_name).all()

    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movie).data
    return data


def read_one(movie_id):

    movie = (
        Movie.query.filter(Movie.movie_id == movie_id)
        .outerjoin(Theater)
        .one_or_none()
    )

    if movie is not None:

        movie_schema = MovieSchema()
        data = movie_schema.dump(movie).data
        return data

    else:
        abort(404, f"Movie not found for Id: {movie_id}")


def create(movie):

    movie_name = movie.get("movie_name")
    released_year = movie.get("released_year")
    movie_type = movie.get("movie_type")

    existing_movie = (
        Movie.query.filter(Movie.movie_name == movie_name)
        .filter(Movie.released_year == released_year)
        .filter(Movie.movie_type == movie_type)
        .one_or_none()
    )

    if existing_movie is None:

        schema = MovieSchema()
        new_movie = schema.load(movie, session=db.session).data

        db.session.add(new_movie)
        db.session.commit()

        data = schema.dump(new_movie).data

        return data, 201

    else:
        abort(409, f"Movie {movie_name} exists already")


def update(movie_id, movie):

    update_movie = Movie.query.filter(
        Movie.movie_id == movie_id
    ).one_or_none()

    if update_movie is not None:

        schema = MovieSchema()
        update = schema.load(movie, session=db.session).data

        update.movie_id = update_movie.movie_id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_movie).data

        return data, 200

    else:
        abort(404, f"Movie not found for Id: {movie_id}")


def delete(movie_id):

    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()

    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(f"Movie {movie_id} deleted", 200)

    else:
        abort(404, f"Movie not found for Id: {movie_id}")
