from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
import jinja2
import os


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jobinterview:password@localhost:8889/jobinterview'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'a;slkfjalskdfjl;aksdfj;alksdfjl;askdflksjfdlksjdfglk;'

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    director = db.Column(db.String(120))
    release_year = db.Column(db.Integer)
    origin_ethnicity = db.Column(db.String(50)) 
    cast = db.Column(db.String(1000)) 
    genre = db.Column(db.String(120)) 
    wiki = db.Column(db.String(120)) 
    plot = db.Column(db.String(1000)) 

    #owner_id = db.relationship('Blog', backref='owner')
    
    def __init__(self, title, release_year, origin_ethnicity, cast, genre, wiki, plot):
        self.title = title
        self.release_year = release_year
        self.origin_ethnicity = origin_ethnicity
        self.cast = cast
        self.genre = genre
        self.wiki = wiki
        self.plot = plot

    def is_valid(self):
        if self.title and self.release_year and self.origin_ethnicity and self.cast and self.genre and self.wiki and self.plot:
            return True
        else:
            return False

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('home_view.html', title="Welcome to the Balto Movie Database!")
    else:
        return render_template('home_view.html', title="Welcome to the Balto Movie Database!")

@app.route("/addmovie", methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        new_title = request.form['title']
        new_release_year = request.form['release_year']
        new_origin_ethnicity = request.form['origin_ethnicity']
        new_cast = request.form['cast']
        new_genre = request.form['genre']
        new_plot = request.form['plot']
        new_wiki = request.form['wiki']
        if not new_title and new_release_year and new_origin_ethnicity and new_cast and new_genre and new_plot and new_wiki:
            flash("Please fill out all forms.")
            return render_template('add_form', title="Add a new movie!")
        else: 
            new_movie = Movie(new_title, new_release_year, new_origin_ethnicity, new_cast, new_genre, new_plot, new_wiki)
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/display_all_movies')
    else:
        return render_template('add_movie.html', title="Add a new movie!")

@app.route("/display_all_movies", methods=['GET'])
def display_all_movies():
        movies = Movie.query.all()
        return render_template('display_all_movies.html', movies=movies)


if __name__=='__main__':
    app.run()