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

def search_by_column(searchterm, movie, column):
    if column == "title":
        title = movie.title
        title = title.lower()
        if searchterm in title:
            return True
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

def update_movies(title, release_year, director, origin, cast, genre, wiki, plot, movie):
    if title:
        movie.title = title
    if release_year:
        movie.release_year = release_year
    if director:
        movie.director = director
    if origin:
        movie.origin = origin
    if cast:
        movie.cast = cast
    if genre:
        movie.genre = genre
    if wiki:
        movie.wiki = wiki
    if plot:
        movie.plot = plot
    return movie
    