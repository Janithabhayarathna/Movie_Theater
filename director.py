from flask import make_response, abort, request
from config import db
from models import Movie, Director, DirectorSchema, SearchMovieSchema


def read_all():

    directors = Director.query.order_by(db.desc(Director.director_name)).all()

    director_schema = DirectorSchema(many=True, exclude=["movie.directors"])
    data = director_schema.dump(directors).data
    return data


def read_all_movies():

    director_name = request.args.get("name", type=str)

    if director_name is not None:
        director = Director.query.filter_by(director_name=director_name).all()
        director_schema = SearchMovieSchema(many=True)
        return director_schema.jsonify(director)

    else:
        abort(404, "Director name not found")


def read_one(movie_id, director_id):

    director = (
        Director.query.join(Movie, Movie.movie_id == Director.movie_id)
        .filter(Director.movie_id == movie_id)
        .filter(Director.director_id == director_id)
        .one_or_none()
    )

    if director is not None:
        director_schema = DirectorSchema()
        data = director_schema.dump(director).data
        return data

    else:
        abort(404, f"Director not found for Id: {director_id}")


def create(movie_id, director):

    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()

    if movie is None:
        abort(404, f"Movie not found for Id: {movie_id}")

    schema = DirectorSchema()
    new_director = schema.load(director, session=db.session).data

    movie.directors.append(new_director)
    db.session.commit()

    data = schema.dump(new_director).data

    return data, 201


def update(movie_id, director_id, director):

    update_director = (
        Director.query.filter(Director.movie_id == movie_id)
        .filter(Director.director_id == director_id)
        .one_or_none()
    )

    if update_director is not None:

        schema = DirectorSchema()
        update = schema.load(director, session=db.session).data

        update.movie_id = update_director.movie_id
        update.actor_id = update_director.director_id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_director).data

        return data, 200

    else:
        abort(404, f"Director not found for Id: {director_id}")


def delete(movie_id, director_id):

    director = (
        Director.query.filter(Movie.movie_id == movie_id)
        .filter(Director.director_id == director_id)
        .one_or_none()
    )

    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(
            "Director {director_id} deleted".format(director_id=director_id), 200
        )

    else:
        abort(404, f"Director not found for Id: {director_id}")
