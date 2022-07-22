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

        # Add the person to the database
        db.session.add(new_movie)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_movie).data

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(409, f"Movie {movie_name} exists already")


def update(movie_id, movie):
    """
    This function updates an existing person in the people structure
    :param movie_id:   Id of the person to update in the people structure
    :param movie:      person to update
    :return:            updated person structure
    """
    # Get the person requested from the db into session
    update_movie = Movie.query.filter(
        Movie.movie_id == movie_id
    ).one_or_none()

    # Did we find an existing person?
    if update_movie is not None:

        # turn the passed in person into a db object
        schema = MovieSchema()
        update = schema.load(movie, session=db.session).data

        # Set the id to the person we want to update
        update.movie_id = update_movie.movie_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_movie).data

        return data, 200

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Movie not found for Id: {movie_id}")


def delete(movie_id):
    """
    This function deletes a person from the people structure
    :param movie_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()

    # Did we find a person?
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(f"Movie {movie_id} deleted", 200)

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Movie not found for Id: {movie_id}")
