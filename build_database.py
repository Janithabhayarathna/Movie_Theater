import os
from config import db
from models import Movie, Theater, Actor, Director

MOVIE = [
    {
        "movie_name": "Last",
        "released_year": "2021",
        "movie_type": "Drama",
        "theaters": [
            ("Regal", "Kandy", "3D"),
            ("Savoy", "Wellawatta", "5D"),
            ("CCC", "Colombo", "6D"),
        ],
        "actors": [
            ("Reeves", "Kandy", 7),
            ("John", "Colombo", 6),
        ],
        "directors": [
            ("Jason", "Colombo"),
            ("Kamal", "Rathnapura"),
        ],
    },
]

if os.path.exists("movie.db"):
    os.remove("movie.db")

db.create_all()

for movie in MOVIE:
    content = Movie(movie_name=movie.get("movie_name"), released_year=movie.get("released_year"), movie_type=movie.get("movie_type"))

    for theater in movie.get("theaters"):
        theater_name, theater_address, theater_type = theater
        content.theaters.append(
            Theater(
                theater_name=theater_name,
                theater_address=theater_address,
                theater_type=theater_type,
            )
        )

    for actor in movie.get("actors"):
        actor_name, actor_address, actor_rank = actor
        content.actors.append(
            Actor(
                actor_name=actor_name,
                actor_address=actor_address,
                actor_rank=actor_rank,
            )
        )

    for director in movie.get("directors"):
        director_name, director_address = director
        content.directors.append(
            Director(
                director_name=director_name,
                director_address=director_address,
            )
        )

    db.session.add(content)

db.session.commit()
