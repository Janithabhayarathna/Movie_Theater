from flask import make_response, abort
from config import db
from models import Movie, Actor, ActorSchema


def read_all():
    """
    This function responds to a request for /api/people/notes
    with the complete list of notes, sorted by note timestamp
    :return:                json list of all notes for all people
    """
    # Query the database for all the notes
    actors = Actor.query.order_by(db.desc(Actor.actor_name)).all()

    # Serialize the list of notes from our data
    actor_schema = ActorSchema(many=True, exclude=["movie.actors"])
    data = actor_schema.dump(actors).data
    return data


def read_one(movie_id, actor_id):
    """
    This function responds to a request for
    /api/people/{person_id}/notes/{note_id}
    with one matching note for the associated person
    :param movie_id:       Id of person the note is related to
    :param theater_id:         Id of the note
    :return:                json string of note contents
    """
    # Query the database for the note
    actors = (
        Actor.query.join(Movie, Movie.movie_id == Actor.movie_id)
        .filter(Actor.movie_id == movie_id)
        .filter(Actor.actor_id == actor_id)
        .one_or_none()
    )

    # Was a note found?
    if actors is not None:
        actor_schema = ActorSchema()
        data = actor_schema.dump(actors).data
        return data

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Actor not found for Id: {actor_id}")


def create(movie_id, actor):

    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()

    # Was a person found?
    if movie is None:
        abort(404, f"Movie not found for Id: {movie_id}")

    # Create a note schema instance
    schema = ActorSchema()
    new_actor = schema.load(actor, session=db.session).data

    # Add the note to the person and database
    movie.actors.append(new_actor)
    db.session.commit()

    # Serialize and return the newly created note in the response
    data = schema.dump(new_actor).data

    return data, 201


def update(movie_id, actor_id, actor):
    """
    This function updates an existing note related to the passed in
    person id.
    :param movie_id:       Id of the person the note is related to
    :param theater_id:         Id of the note to update
    :param content:            The JSON containing the note data
    :return:                200 on success
    """
    update_actor = (
        Actor.query.filter(Actor.movie_id == movie_id)
        .filter(Actor.actor_id == actor_id)
        .one_or_none()
    )

    # Did we find an existing note?
    if update_actor is not None:

        # turn the passed in note into a db object
        schema = ActorSchema()
        update = schema.load(actor, session=db.session).data

        # Set the id's to the note we want to update
        update.movie_id = update_actor.movie_id
        update.actor_id = update_actor.actor_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated note in the response
        data = schema.dump(update_actor).data

        return data, 200

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Actor not found for Id: {actor_id}")


def delete(movie_id, actor_id):
    """
    This function deletes a note from the note structure
    :param movie_id:   Id of the person the note is related to
    :param theater_id:     Id of the note to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the note requested
    actor = (
        Actor.query.filter(Movie.movie_id == movie_id)
        .filter(Actor.actor_id == actor_id)
        .one_or_none()
    )

    # did we find a note?
    if actor is not None:
        db.session.delete(actor)
        db.session.commit()
        return make_response(
            "Actor {actor_id} deleted".format(actor_id=actor_id), 200
        )

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Actor not found for Id: {actor_id}")
