from main import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    director = db.Column(db.String(120))
    release_year = db.Column(db.Integer)
    origin_ethnicity = db.Column(db.String(50)) 
    cast = db.Column(db.String(1000)) 
    genre = db.Column(db.String(120)) 
    wiki = db.Column(db.String(120)) 
    plot = db.Column(db.String(1000)) 
    
    def __init__(self, title, release_year, director, origin_ethnicity, cast, genre, wiki, plot):
        self.title = title
        self.release_year = release_year
        self.director = director
        self.origin_ethnicity = origin_ethnicity
        self.cast = cast
        self.genre = genre
        self.wiki = wiki
        self.plot = plot

    def is_valid(self):
        if self.title and self.release_year and self.director and self.origin_ethnicity and self.cast and self.genre and self.wiki and self.plot:
            return True
        else:
            return False

