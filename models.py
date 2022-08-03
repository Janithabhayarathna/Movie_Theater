from config import db, ma
from marshmallow import fields
from datetime import datetime


class MovieTheater(db.Model):
    __tablename__ = "movie_theater"
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), primary_key=True)
    theater_id = db.Column(db.Integer, db.ForeignKey("theater.theater_id"), primary_key=True)
    showtime = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)


class Movie(db.Model):
    __tablename__ = "movie"
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(32), nullable=False, unique=True)
    released_year = db.Column(db.String(4))
    movie_type = db.Column(db.String(12))

    theaters = db.relationship(
        "Theater",
        secondary='movie_theater'
    )

    actors = db.relationship(
        "Actor",
        secondary='movie_actor'
    )

    directors = db.relationship(
        "Director",
        secondary='movie_director'
    )


class Theater(db.Model):
    __tablename__ = "theater"
    theater_id = db.Column(db.Integer, primary_key=True)
    theater_name = db.Column(db.String(32), nullable=False)
    theater_address = db.Column(db.String(32))
    theater_type = db.Column(db.String(2))

    movies = db.relationship(Movie, secondary='movie_theater')


class Actor(db.Model):
    __tablename__ = "actor"
    actor_id = db.Column(db.Integer, primary_key=True)
    actor_name = db.Column(db.String(32), nullable=False)
    actor_address = db.Column(db.String(32))
    actor_rank = db.Column(db.String(2))

    movies = db.relationship(Movie, secondary='movie_actor')


class MovieActor(db.Model):
    __tablename__ = "movie_actor"
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("actor.actor_id"), primary_key=True)


class Director(db.Model):
    __tablename__ = "director"
    director_id = db.Column(db.Integer, primary_key=True)
    director_name = db.Column(db.String(32), nullable=False)
    director_address = db.Column(db.String(32))

    movies = db.relationship(Movie, secondary='movie_director')


class MovieDirector(db.Model):
    __tablename__ = "movie_director"
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), primary_key=True)
    director_id = db.Column(db.Integer, db.ForeignKey("director.director_id"), primary_key=True)


class MovieSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Movie
        sqla_session = db.session

    theaters = fields.Nested("MovieTheaterSchema", default=[], many=True)
    actors = fields.Nested("MovieActorSchema", default=[], many=True)
    directors = fields.Nested("MovieDirectorSchema", default=[], many=True)


class MovieTheaterSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    theater_id = fields.Int()
    movie_id = fields.Int()
    theater_name = fields.Str()
    theater_address = fields.Str()
    theater_type = fields.Str()


class TheaterSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Theater
        sqla_session = db.session


class TheaterShowSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Theater
        sqla_session = db.session

    show_time = fields.Str()


class TheaterMovieSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    movie_id = fields.Int()
    movie_name = fields.Str()
    released_year = fields.Str()
    movie_type = fields.Str()


class ActorSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Actor
        sqla_session = db.session


class MovieActorSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    actor_id = fields.Int()
    movie_id = fields.Int()
    actor_name = fields.Str()
    actor_address = fields.Str()
    actor_rank = fields.Int()


class ActorMovieSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    movie_id = fields.Int()
    movie_name = fields.Str()
    released_year = fields.Str()
    movie_type = fields.Str()


class DirectorSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Director
        sqla_session = db.session


class MovieDirectorSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    director_id = fields.Int()
    movie_id = fields.Int()
    director_name = fields.Str()
    director_address = fields.Str()


class DirectorMovieSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    movie_id = fields.Int()
    movie_name = fields.Str()
    released_year = fields.Str()
    movie_type = fields.Str()


class ShowtimeSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    theater_id = fields.Int()
    showtime = fields.DateTime()
