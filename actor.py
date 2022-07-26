from flask import make_response, abort
from config import db
from models import Movie, Actor, ActorSchema


def read_all():
    actors = Actor.query.order_by(db.desc(Actor.actor_name)).all()

    actor_schema = ActorSchema(many=True, exclude=["movie.actors"])
    data = actor_schema.dump(actors).data
    return data


def read_one(movie_id, actor_id):
    actors = (
        Actor.query.join(Movie, Movie.movie_id == Actor.movie_id)
        .filter(Actor.movie_id == movie_id)
        .filter(Actor.actor_id == actor_id)
        .one_or_none()
    )

    if actors is not None:
        actor_schema = ActorSchema()
        data = actor_schema.dump(actors).data
        return data

    else:
        abort(404, f"Actor not found for Id: {actor_id}")


def create(movie_id, actor):
    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()

    if movie is None:
        abort(404, f"Movie not found for Id: {movie_id}")

    schema = ActorSchema()
    new_actor = schema.load(actor, session=db.session).data

    movie.actors.append(new_actor)
    db.session.commit()

    data = schema.dump(new_actor).data

    return data, 201


def update(movie_id, actor_id, actor):

    update_actor = (
        Actor.query.filter(Actor.movie_id == movie_id)
        .filter(Actor.actor_id == actor_id)
        .one_or_none()
    )

    if update_actor is not None:

        schema = ActorSchema()
        update = schema.load(actor, session=db.session).data

        update.movie_id = update_actor.movie_id
        update.actor_id = update_actor.actor_id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_actor).data

        return data, 200

    else:
        abort(404, f"Actor not found for Id: {actor_id}")


def delete(movie_id, actor_id):

    actor = (
        Actor.query.filter(Movie.movie_id == movie_id)
        .filter(Actor.actor_id == actor_id)
        .one_or_none()
    )

    if actor is not None:
        db.session.delete(actor)
        db.session.commit()
        return make_response(
            "Actor {actor_id} deleted".format(actor_id=actor_id), 200
        )

    else:
        abort(404, f"Actor not found for Id: {actor_id}")
