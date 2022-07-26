from config import db, ma
from marshmallow import fields


class Movie(db.Model):
    __tablename__ = "movie"
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(32))
    released_year = db.Column(db.String(4))
    movie_type = db.Column(db.String(12))

    theaters = db.relationship(
        "Theater",
        backref="movie",
        cascade="all, delete, delete-orphan",
    )

    actors = db.relationship(
        "Actor",
        backref="movie",
        cascade="all, delete, delete-orphan",
    )

    directors = db.relationship(
        "Director",
        backref="movie",
        cascade="all, delete, delete-orphan",
    )


class Theater(db.Model):
    __tablename__ = "theater"
    theater_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"))
    theater_name = db.Column(db.String)
    theater_address = db.Column(db.String(32))
    theater_type = db.Column(db.String(2))


class Actor(db.Model):
    __tablename__ = "actor"
    actor_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"))
    actor_name = db.Column(db.String)
    actor_address = db.Column(db.String(32))
    actor_rank = db.Column(db.Integer)


class Director(db.Model):
    __tablename__ = "director"
    director_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"))
    director_name = db.Column(db.String)
    director_address = db.Column(db.String(32))


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

    movie = fields.Nested("TheaterMovieSchema", default=None)


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

    movie = fields.Nested("ActorMovieSchema", default=None)


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

    movie = fields.Nested("DirectorMovieSchema", default=None)


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
