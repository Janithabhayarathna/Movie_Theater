from flask import make_response, abort
from config import db
from models import Movie, Director, DirectorSchema


def read_all():
    """
    This function responds to a request for /api/people/notes
    with the complete list of notes, sorted by note timestamp
    :return:                json list of all notes for all people
    """
    # Query the database for all the notes
    directors = Director.query.order_by(db.desc(Director.director_name)).all()

    # Serialize the list of notes from our data
    director_schema = DirectorSchema(many=True, exclude=["movie.directors"])
    data = director_schema.dump(directors).data
    return data


def read_one(movie_id, director_id):
    """
    This function responds to a request for
    /api/people/{person_id}/notes/{note_id}
    with one matching note for the associated person
    :param movie_id:       Id of person the note is related to
    :param theater_id:         Id of the note
    :return:                json string of note contents
    """
    # Query the database for the note
    director = (
        Director.query.join(Movie, Movie.movie_id == Director.movie_id)
        .filter(Director.movie_id == movie_id)
        .filter(Director.director_id == director_id)
        .one_or_none()
    )

    # Was a note found?
    if director is not None:
        director_schema = DirectorSchema()
        data = director_schema.dump(director).data
        return data

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Director not found for Id: {director_id}")


def create(movie_id, director):

    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()

    # Was a person found?
    if movie is None:
        abort(404, f"Movie not found for Id: {movie_id}")

    # Create a note schema instance
    schema = DirectorSchema()
    new_director = schema.load(director, session=db.session).data

    # Add the note to the person and database
    movie.directors.append(new_director)
    db.session.commit()

    # Serialize and return the newly created note in the response
    data = schema.dump(new_director).data

    return data, 201


def update(movie_id, director_id, director):
    """
    This function updates an existing note related to the passed in
    person id.
    :param movie_id:       Id of the person the note is related to
    :param theater_id:         Id of the note to update
    :param content:            The JSON containing the note data
    :return:                200 on success
    """
    update_director = (
        Director.query.filter(Director.movie_id == movie_id)
        .filter(Director.director_id == director_id)
        .one_or_none()
    )

    # Did we find an existing note?
    if update_director is not None:

        # turn the passed in note into a db object
        schema = DirectorSchema()
        update = schema.load(director, session=db.session).data

        # Set the id's to the note we want to update
        update.movie_id = update_director.movie_id
        update.actor_id = update_director.director_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated note in the response
        data = schema.dump(update_director).data

        return data, 200

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Director not found for Id: {director_id}")


def delete(movie_id, director_id):
    """
    This function deletes a note from the note structure
    :param movie_id:   Id of the person the note is related to
    :param theater_id:     Id of the note to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the note requested
    director = (
        Director.query.filter(Movie.movie_id == movie_id)
        .filter(Director.director_id == director_id)
        .one_or_none()
    )

    # did we find a note?
    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(
            "Director {director_id} deleted".format(director_id=director_id), 200
        )

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Director not found for Id: {director_id}")
