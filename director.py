from flask import make_response, abort, request
from config import db
from models import Movie, Director, DirectorSchema, MovieDirector


def read_all():

    director_name = request.args.get("name", type=str)

    if director_name is not None:
        return db.session.query(Movie.movie_name).join(MovieDirector).join(Director).filter(
            Director.director_name == director_name).all()

    else:
        directors = Director.query.order_by(db.desc(Director.director_id)).all()

        director_schema = DirectorSchema(many=True)
        data = director_schema.dump(directors).data
        return data


def read_one(director_id):

    director = (
        Director.query.filter(Director.director_id == director_id)
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


def add_existing(movie_id, director_id):
    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()
    director = Director.query.filter(Director.director_id == director_id).one_or_none()

    if movie is None:
        abort(404, f"Movie not found for Id: {movie_id}")

    elif director is None:
        abort(404, f"Director not found for Id: {director_id}")

    movie.directors.append(director)
    db.session.commit()

    return 201


def update(director_id, director):

    update_director = (
        Director.query.filter(Director.director_id == director_id)
        .one_or_none()
    )

    if update_director is not None:

        schema = DirectorSchema()
        update = schema.load(director, session=db.session).data

        update.actor_id = update_director.director_id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_director).data

        return data, 200

    else:
        abort(404, f"Director not found for Id: {director_id}")


def delete(director_id):

    director = (
        Director.query.filter(Director.director_id == director_id)
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
