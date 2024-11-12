"""File: movie_service_gpt.py"""


def read_file(pathname: str, year: int = 0) -> list:
    """
    Reads data from a CSV file and returns a list of movies, each
    represented as a list of attributes. Filters by the specified
    starting year if provided.
    
    Args:
        pathname (str): Path to the CSV file.
        year (int, optional): Filter movies released in or after
        this year. Defaults to 0 (no filter).

    Returns:
        list: List of movie entries, where each movie is represented as a list of its attributes.

    >>> read_file('films.csv', 2014)[:2]
    [['1', 'Guardians of the Galaxy', 'Action,Adventure,Sci-Fi', \
'A group of intergalactic criminals are forced to work together to stop \
a fanatical warrior from taking control of the universe.', 'James Gunn', \
'Chris Pratt, Vin Diesel, Bradley Cooper, Zoe Saldana', '2014', '121', '8.1', \
'757074', '333.13', '76.0'], ['3', 'Split', 'Horror,Thriller', \
'Three girls are kidnapped by a man with a diagnosed 23 distinct personalities. \
They must try to escape before the apparent emergence of a frightful new 24th.', \
'M. Night Shyamalan', 'James McAvoy, Anya Taylor-Joy, Haley Lu Richardson, Jessica Sula', \
'2016', '117', '7.3', '157606', '138.12', '62.0']]
    """
    movie_data = []
    try:
        with open(pathname, 'r', encoding='utf-8') as file:
            headers = file.readline().strip().split(';')
            for line in file:
                row = line.strip().split(';')
                try:
                    movie_year = int(row[6])
                    if year == 0 or movie_year >= year:
                        movie_data.append(row)
                except ValueError:
                    # Skip entries with invalid year formats
                    continue
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {pathname} could not be found.")
    except IOError:
        raise IOError(f"An error occurred while reading the file {pathname}.")
    return movie_data


def sort_key(movie):
    """
    Key function for sorting movies by average rating descending, and lexicographically by title.

    Args:
        movie (tuple): A tuple in the form (Title, Rating, Actors_Rating, Average_rating)

    Returns:
        tuple: A sorting key with negative average rating for descending order and title for
        lexicographical order.
    """
    return (-movie[3], movie[0])


def top_n(data: list, genre: str = '', n: int = 0) -> list:
    """
    Selects the top-rated movies filtered by genre and
    calculates an adjusted actor-based rating.

    Args:
        data (list): List of movie entries from the read_file function.
        genre (str, optional): Genre or multiple genres (comma-separated)
        to filter movies by. Defaults to '' (no filter).
        n (int, optional): Number of top movies to return. If 0,
        returns all matching movies. Defaults to 0.

    Returns:
        list: List of tuples of (Title, Average_rating), sorted by
        Average_rating in descending order.

    >>> top_n(read_file('films.csv', 2014), genre='Action', n=5)
    [('Dangal', 8.8), \
('Bahubali: The Beginning', 8.3), \
('Guardians of the Galaxy', 8.1), \
('Mad Max: Fury Road', 8.1), \
('Star Wars: Episode VII - The Force Awakens', 8.1)]

    >>> top_n(read_file('films.csv', 2014), genre='Action,Adventure', n=5)
    [('Dangal', 8.8), \
('Interstellar', 8.6), \
('Bahubali: The Beginning', 8.3), \
('Inside Out', 8.2), \
('Guardians of the Galaxy', 8.1)]

    >>> top_n(read_file('films.csv', 0), genre='', n=4)
    [('The Dark Knight', 9.0), ('Dangal', 8.8), \
('Inception', 8.8), ('The Prestige', 8.625)]

    >>> top_n(read_file('films.csv', 0), genre='Thriller,Horror', n=10)
    [('The Dark Knight Rises', 8.575), ('The Departed', 8.5375), \
('The Lives of Others', 8.5), ('Shutter Island', 8.1875), \
('The Revenant', 8.175), ('The Bourne Ultimatum', 8.149999999999999), \
('Blood Diamond', 8.1), ('No Country for Old Men', 8.1), \
('Relatos salvajes', 8.1), ('The Imitation Game', 8.1)]

    >>> len(top_n(read_file('films.csv', 0), genre='', n=0))
    1000
    """
    filtered_movies = []
    genres = set(genre.split(',')) if genre else set()

    def calculate_actor_rating(actors, data):
        """Calculates the average highest rating for each actor across all movies."""
        actor_ratings = []
        for actor in actors.split(','):
            highest_rating = max(
                float(movie[8]) for movie in data if actor.strip() in movie[5]
            )
            actor_ratings.append(highest_rating)
        return sum(actor_ratings) / len(actor_ratings) if actor_ratings else 0

    for movie in data:
        movie_genres = set(movie[2].split(','))
        if not genres or genres.intersection(movie_genres):
            try:
                title = movie[1]
                rating = float(movie[8])
                actors_rating = calculate_actor_rating(movie[5], data)
                average_rating = (rating + actors_rating) / 2
                filtered_movies.append((title, rating, actors_rating, average_rating))
            except ValueError:
                # Skip entries with invalid rating formats
                continue

    # Sort by average rating descending, then by title lexicographically
    filtered_movies.sort(key=sort_key)

    # Return top n or all if n is 0
    result = [(title, avg_rating) for title, _, _, avg_rating in filtered_movies]
    return result[:n] if n > 0 else result


def write_file(top: list, file_name: str) -> None:
    """
    Writes the list of top movies to a specified file, each entry on a new line.

    Args:
        top (list): List of tuples (Title, rating) to write to the file.
        file_name (str): Name of the output file.

    >>> top_movies = [('The Dark Knight', 9.0), ('Inception', 8.8), ('Interstellar', 8.6)]
    >>> write_file(top_movies, 'top_movies.txt')
    >>> with open('top_movies.txt', 'r', encoding='utf-8') as file:
    ...     for line in list(file):
    ...         print(line.strip())
    The Dark Knight, 9.0
    Inception, 8.8
    Interstellar, 8.6
    """
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            for title, rating in top:
                file.write(f"{title}, {rating:.1f}\n")
    except IOError:
        raise IOError(f"An error occurred while writing to the file {file_name}.")


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
