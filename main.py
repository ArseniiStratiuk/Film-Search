"""
A Python code-based service that allows the user to specify the genre, the year, and
the number of top rated movies they want to receive and returns to them a list of
matching movies ordered by rating in descending order.
"""


def read_file(pathname: str, year: int = 0) -> list[list[str]]:
    """
    Read data from a CSV file containing movie information,
    starting from the specified year.

    :param pathname: str, The path to the CSV file.
    :param year: int, The starting year for filtering movies. If 0, include all years.
    :return: list[list[str]], A list of lists where each inner list contains details
        for a single movie.
    """

    # had to write this function to test the second one
    # 
    with open(pathname, "r", encoding="utf-8") as file:
        return [row.split(";") for row in file.read().split("\n") if row and row[0].isdigit() and int(row.split(";")[6]) >= year]

def top_n(data: list[list[str]], genre: str = '', n: int = 0) -> list[tuple[str, float]]:
    """
    Filter and rank the top N movies by rating and actor rating, based on the specified genre.

    :param data: list[list[str]], List of movie records, each containing movie details.
    :param genre: str, Genre(s) to filter by, separated by commas for multiple genres.
    :param n: int, Number of top results to return. If n is 0, return all movies.
    :return: list[tuple[str, float]], List of tuples (Title, Average_rating), ordered by rating.

    >>> top_n(read_file('films.csv', 2014), genre='Action', n=5)
    [('Dangal', 8.8), \
('Bahubali: The Beginning', 8.3), \
('Guardians of the Galaxy', 8.1), \
('Mad Max: Fury Road', 8.1), \
('Star Wars: Episode VII - The Force Awakens', 8.1)]

    >>> top_n(read_file('films.csv', 0), genre='', n=4)
    [('The Dark Knight', 9.0), \
('Dangal', 8.8), \
('Inception', 8.8), \
('Interstellar', 8.6)]

    >>> len(top_n(read_file('films.csv', 0), genre='', n=0))
    1000
    """

    actors_max = {}
    for movie in data:
        for actor in movie[5].split(", "):
            actors_max[actor] = max(actors_max.get(actor, 0), float(movie[8]))

    movies_rating = []
    for movie in data:
        if not genre or set(genre.split(",")).intersection(set(movie[2].split(","))):
            actors_values = [actors_max[actor] for actor in movie[5].split(", ")]
            movies_rating.append((
                movie[1],
                float(movie[8]),
                sum(actors_values) / len(actors_values)
            ))

    def compare_rating(movie_rating):
        return (-(movie_rating[1] + movie_rating[2]) / 2, movie_rating[0])

    movies_rating.sort(key=compare_rating)

    return [(top_movie[0], (top_movie[1] + top_movie[2]) / 2)
            for top_movie in movies_rating[:n if n else len(movies_rating)]]

def write_file(top: list[tuple[str, float]], file_name: str) -> None:
    """
    Write the list of top movies to a specified file, each on a separate line.

    :param top: list[tuple[str, float]], List of top-rated movies with their ratings.
    :param file_name: str, The name of the output file.
    :return: None
    """
    # TODO: Implement function to write top movies to a file, each on a separate line.
    pass


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())

    movies_data = read_file('films.csv', 2014)
    top_movies = top_n(movies_data, genre='Action', n=5)
    write_file(top_movies, 'top_movies.txt')
