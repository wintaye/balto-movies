from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
import jinja2
import os
from search_formula import search_all, search_by_column, update_movies

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

@app.route("/", methods=['GET','POST'])
def index():
    return render_template('home_view.html', title="Welcome to the Balto Movie Database!")

@app.route("/addmovie", methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        new_title = request.form['title']
        new_release_year = request.form['release_year']
        new_director = request.form['director']
        new_origin_ethnicity = request.form['origin_ethnicity']
        new_cast = request.form['cast']
        new_genre = request.form['genre']
        new_plot = request.form['plot']
        new_wiki = request.form['wiki']
        if not new_title and new_release_year and new_director and new_origin_ethnicity and new_cast and new_genre and new_plot and new_wiki:
            flash("Please fill out all forms.")
            return render_template('add_movie.html', title="Add a new movie!")
        else: 
            new_movie = Movie(new_title, new_release_year, new_director, new_origin_ethnicity, new_cast, new_genre, new_plot, new_wiki)
            db.session.add(new_movie)
            db.session.commit()
            url = "/movie"
            return redirect(url)
    else:
        return render_template('add_movie.html', title="Add a new movie!")

@app.route("/movie", methods=['GET'])
def display_movies():
    id = request.args.get('id')
    if id:
        movie = Movie.query.filter_by(id=id).first()
        return render_template('display_single_movie.html', movie=movie, title=movie.title)
    else:
        movies = Movie.query.all()
        return render_template('display_all_movies.html', movies=movies)
    
@app.route("/movie", methods=['POST'])
def delete_movie():
    delete = request.form['delete']
    print(delete)
    if delete:
        id = delete
        movie = Movie.query.filter_by(id=id).first()
        db.session.delete(movie)
        db.session.commit()
        return redirect("/movie")
    else:
        return redirect("/movie")

@app.route("/search", methods=['GET','POST'])
def search_movies():
    if request.method == 'POST':
        list_of_movies = []
        movies = Movie.query.all()
        searchterm = request.form['searchterm']
        searchterm = searchterm.lower()
        print(searchterm)
        for movie in movies:
            print(movie)
            aValue = search_all(searchterm, movie)
            print(aValue)
            if aValue == True:
                list_of_movies.append(movie)
        return render_template("display_all_movies.html", movies=list_of_movies)
            # else:
            #     flash("No Search Results")
            #     return redirect("/search")
    else:
        return render_template("search_form.html")
                
@app.route("/edit", methods=['GET', 'POST'])
def retrieve_edit_view():
    if request.method == 'POST':
        id = request.form['edit']
        movie = Movie.query.filter_by(id=id).first()
        return render_template("edit.html", movie=movie)
    else:
        return redirect("/movie")

@app.route("/editmovie", methods=['POST'])
def edit_movie():
    title = request.form['title']
    release_year = request.form['release_year']
    director = request.form['director']
    origin = request.form['origin_ethnicity']
    cast = request.form['cast']
    genre = request.form['genre']
    wiki = request.form['wiki']
    plot = request.form['plot']
    movie = Movie.query.filter_by(id=id).first()
    updated_movie = update_movies(title, release_year, director, origin, cast, genre, wiki, plot, movie)
    db.session.commit()
    return redirect("/movie")

if __name__=='__main__':
    app.run()