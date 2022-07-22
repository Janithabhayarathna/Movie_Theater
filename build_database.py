import os
from config import db
from models import Movie, Theater

# Data to initialize database with
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
    },
]

# Delete database file if it exists currently
if os.path.exists("movie.db"):
    os.remove("movie.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for movie in MOVIE:
    content = Movie(movie_name=movie.get("movie_name"), released_year=movie.get("released_year"), movie_type=movie.get("movie_type"))

    # Add the notes for the person
    for theater in movie.get("theaters"):
        theater_name, theater_address, theater_type = theater
        content.theaters.append(
            Theater(
                theater_name=theater_name,
                theater_address=theater_address,
                theater_type=theater_type,
            )
        )
    db.session.add(content)

db.session.commit()
