from flask import make_response, abort
from config import db
from models import Movie, Theater, TheaterSchema


def read_all():
    """
    This function responds to a request for /api/people/notes
    with the complete list of notes, sorted by note timestamp
    :return:                json list of all notes for all people
    """
    # Query the database for all the notes
    theaters = Theater.query.order_by(db.desc(Theater.theater_name)).all()

    # Serialize the list of notes from our data
    theater_schema = TheaterSchema(many=True, exclude=["movie.theaters"])
    data = theater_schema.dump(theaters).data
    return data


def read_one(movie_id, theater_id):
    """
    This function responds to a request for
    /api/people/{person_id}/notes/{note_id}
    with one matching note for the associated person
    :param movie_id:       Id of person the note is related to
    :param theater_id:         Id of the note
    :return:                json string of note contents
    """
    # Query the database for the note
    theater = (
        Theater.query.join(Movie, Movie.movie_id == Theater.movie_id)
        .filter(Theater.movie_id == movie_id)
        .filter(Theater.theater_id == theater_id)
        .one_or_none()
    )

    # Was a note found?
    if theater is not None:
        theater_schema = TheaterSchema()
        data = theater_schema.dump(theater).data
        return data

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Theater not found for Id: {theater_id}")


def create(movie_id, theater):

    movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()

    # Was a person found?
    if movie is None:
        abort(404, f"Movie not found for Id: {movie_id}")

    # Create a note schema instance
    schema = TheaterSchema()
    new_theater = schema.load(theater, session=db.session).data

    # Add the note to the person and database
    movie.theaters.append(new_theater)
    db.session.commit()

    # Serialize and return the newly created note in the response
    data = schema.dump(new_theater).data

    return data, 201


def update(movie_id, theater_id, theater):
    """
    This function updates an existing note related to the passed in
    person id.
    :param movie_id:       Id of the person the note is related to
    :param theater_id:         Id of the note to update
    :param content:            The JSON containing the note data
    :return:                200 on success
    """
    update_theater = (
        Theater.query.filter(Theater.theater_id == theater_id)
        .filter(Theater.theater_id == theater_id)
        .one_or_none()
    )

    # Did we find an existing note?
    if update_theater is not None:

        # turn the passed in note into a db object
        schema = TheaterSchema()
        update = schema.load(theater, session=db.session).data

        # Set the id's to the note we want to update
        update.movie_id = update_theater.movie_id
        update.theater_id = update_theater.theater_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated note in the response
        data = schema.dump(update_theater).data

        return data, 200

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Theater not found for Id: {theater_id}")


def delete(movie_id, theater_id):
    """
    This function deletes a note from the note structure
    :param movie_id:   Id of the person the note is related to
    :param theater_id:     Id of the note to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the note requested
    theater = (
        Theater.query.filter(Movie.movie_id == movie_id)
        .filter(Theater.theater_id == theater_id)
        .one_or_none()
    )

    # did we find a note?
    if theater is not None:
        db.session.delete(theater)
        db.session.commit()
        return make_response(
            "Theater {theater_id} deleted".format(theater_id=theater_id), 200
        )

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Theater not found for Id: {theater_id}")
