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
    # TODO: Implement function to read CSV file and filter movies by year.
    pass


def top_n(data: list[list[str]], genre: str = '', n: int = 0) -> list[tuple[str, float]]:
    """
    Filter and rank the top N movies by rating and actor rating, based on the specified genre.

    :param data: list[list[str]], List of movie records, each containing movie details.
    :param genre: str, Genre(s) to filter by, separated by commas for multiple genres.
    :param n: int, Number of top results to return. If n is 0, return all movies.
    :return: list[tuple[str, float]], List of tuples (Title, Average_rating), ordered by rating.
    """
    # TODO: Implement function to calculate actor ratings and return top N movies.
    pass


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
    movies_data = read_file('films.csv', 2014)
    top_movies = top_n(movies_data, genre='Action', n=5)
    write_file(top_movies, 'top_movies.txt')
