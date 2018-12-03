from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
import jinja2
import os
import urllib.parse as urlparse
# from SQLAlchemy import or_
# from search_formula import search_by_column

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
    # id = request.args.get('id')
    # print(id)
    delete = request.form['delete']
    print(delete)
    if delete:
        id = delete
        print(id)
        movie = Movie.query.filter_by(id=id).first()
        print(movie)
            # movie_to_delete = Movie.query.filter_by(id=id).first()
        db.session.delete(movie)
        db.session.commit()
        return redirect("/")
    else:
        print("GOING TO REDIRECT")
        return redirect("/movie")

def search_by_column(searchterm, movie, column):
    if column == "title":
        title = movie.title
        title = title.lower()
        if searchterm in title:
            return True
    # elif column == "release_year":
    #     release = movie.release_year
    #     if searchterm in release:
    #         return True
    elif column == "director":
        director = movie.director
        director = director.lower()
        if searchterm in director:
            return True
    elif column == "origin_ethnicity":
        origin = movie.origin_ethnicity 
        origin = origin.lower()   
        if searchterm in origin:  
            return True
    elif column == "cast":
        cast = movie.cast
        cast = cast.lower()
        if searchterm in cast:
            return True
    elif column == "genre":
        genre = movie.genre
        genre = genre.lower()
        if searchterm in genre:
            return True
    elif column == "plot":
        plot = movie.plot
        plot = plot.lower()
        if searchterm in plot:
            return True
    else:
        return False
        
def search_all(searchterm, movie):
    title = movie.title
    title = title.lower()
    director = movie.director
    director = director.lower()
    origin = movie.origin_ethnicity
    origin = origin.lower()
    cast = movie.cast
    cast = cast.lower()
    genre = movie.genre
    genre = genre.lower()
    plot = movie.plot
    plot = plot.lower()

    if searchterm in title:
        return True
    # elif searchterm in movie.release_year:
    #     return True
    elif searchterm in director:
        return True
    elif searchterm in origin:
        return True
    elif searchterm in cast:
        return True
    elif searchterm in genre:
        return True
    elif searchterm in plot:
        return True
    else: 
        return False

@app.route("/search", methods=['GET','POST'])
def search_movies():
    if request.method == 'POST':
        list_of_movies = []
        #list_of_columns = ["title", "release_year", "director", "origin_ethnicity", "cast", "genre", "plot"]
        movies = Movie.query.all()
        # column = request.form['column']
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
            
            # # for movie in movies:
            # #     for item in list_of_columns:
            # #         aValue = movie.get[1]
            # #         if searchterm in aValue:
            # #             list_of_movies.append(movie)
            # if len(list_of_movies) > 0:
            #     return render_template("display_all_movies.html", movies=list_of_movies)
            # else:
            #     flash("No Search Results")
            #     return redirect("/search")
    else:
        #request is get
        return render_template("search_form.html")
                
# @app.route("/edit", methods=["POST"])
# def edit_item():
#     id = request.form['edit']
#     movie = Movie.query.filter_by(id=id).first()
    


if __name__=='__main__':
    app.run()