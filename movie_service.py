"""
A Python code-based service that allows the user to specify the genre, the year, and
the number of top rated movies they want to receive and returns to them a list of
matching movies ordered by rating in descending order.
"""
def compare_rating(movie_rating: tuple[str, float, float]) -> tuple[float, str]:
    """
    Comparison function for sorting movies by combined rating and actor rating.

    :param movie_rating: tuple[str, float, float], A tuple containing (Title,
        Rating, Actor Rating Average).
    :return: tuple[float, str], Returns a tuple for sorting by average descending
        rating and then by title alphabetically.
    """
    return (-(movie_rating[1] + movie_rating[2]) / 2, movie_rating[0])


def read_file(pathname: str, year: int = 0) -> list[list[str]] | None:
    """
    Read data from a CSV file containing movie information,
    starting from the specified year.

    :param pathname: str, The path to the CSV file.
    :param year: int, The starting year for filtering movies. If 0, include all years.
    :return: list[list[str]], A list of lists where each inner list contains details
        for a single movie. Return None if the input is not valid.

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
    if not (isinstance(pathname, str) and isinstance(year, int)):
        print("The input is not valid.")
        return None
    if year < 0:
        print('The given year is not valid.')
        return None

    results = []
    try:
        with open(pathname, "r", encoding="utf-8") as file:
            file.readline()
            for line in file:
                line = [i.strip() for i in line.split(';')]
                film_year = line[6]

                if len(line) != 12:
                    raise ValueError

                if int(film_year) < year:
                    continue

                results.append(line)
    except FileNotFoundError:
        print(f"File {pathname} not found.")
        return None
    except ValueError:
        print("The data in the input file is not valid.")
        return None

    return results


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

    >>> top_n(read_file('films.csv', 2014), genre='Action,Adventure', n=5)
    [('Dangal', 8.8), \
('Interstellar', 8.6), \
('Bahubali: The Beginning', 8.3), \
('Inside Out', 8.2), \
('Guardians of the Galaxy', 8.1)]

    >>> top_n(read_file('films.csv', 0), genre='', n=4)
    [('The Dark Knight', 9.0), \
('Dangal', 8.8), \
('Inception', 8.8), \
('Interstellar', 8.6)]

    >>> top_n(read_file('films.csv', 0), genre='Thriller,Horror', n=10)
    [('The Dark Knight Rises', 8.583333333333332), \
('The Departed', 8.5375), \
('The Lives of Others', 8.5), \
('Shutter Island', 8.216666666666667), \
('The Revenant', 8.175), \
('The Bourne Ultimatum', 8.149999999999999), \
('Blood Diamond', 8.1), \
('No Country for Old Men', 8.1), \
('Relatos salvajes', 8.1), \
('The Imitation Game', 8.1)]

    >>> len(top_n(read_file('films.csv', 0), genre='', n=0))
    1000
    """
    if not (isinstance(data, list) and isinstance(genre, str) and isinstance(n, int) and n >= 0):
        print("The input is not valid.")
        return None

    try:
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
    except (IndexError, ZeroDivisionError):
        print("The input data is not valid.")
        return None

    movies_rating.sort(key=compare_rating)

    return [(top_movie[0], (top_movie[1] + top_movie[2]) / 2)
            for top_movie in movies_rating[:n if n else len(movies_rating)]]


def write_file(top: list[tuple[str, float]], file_name: str) -> None:
    """
    Write the list of top movies to a specified file, each on a separate line.

    :param top: list[tuple[str, float]], List of top-rated movies with their ratings.
    :param file_name: str, The name of the output file.
    :return: None

    Each line in the output file contains a movie title and its average rating, 
    separated by a comma.

    >>> top_movies = [('The Dark Knight', 9.0), ('Inception', 8.8), ('Interstellar', 8.6)]
    >>> write_file(top_movies, 'top_movies.txt')
    >>> with open('top_movies.txt', 'r', encoding='utf-8') as file:
    ...     for line in list(file):
    ...         print(line.strip())
    The Dark Knight, 9.0
    Inception, 8.8
    Interstellar, 8.6
    """
    if (not isinstance(top, list) or
        not all(isinstance(movie, tuple) and len(movie) == 2 for movie in top)):
        print("The input is not valid.")
        return

    if not isinstance(file_name, str) or not file_name.endswith('.txt'):
        print("Invalid file name: The output file must be a .txt file.")
        return

    try:
        results = []
        with open(file_name, 'w', encoding='utf-8') as file:
            for title, rating in top:
                results.append(f"{title}, {rating:.1f}")

            _ = file.write('\n'.join(results))
    except IOError:
        print(f"Could not write to file {file_name}")


def main():
    """
    Main service function to provide top-rated movies based on user input.
    Provides user input prompts and calls the necessary functions to get the results.
    """
    print("Welcome to the Top Rated Movies service!")
    file_path = input("Enter the path to the CSV file with movie data: ")
    try:
        year = int(input("Enter the starting year for filtering movies (0 for all years): "))
    except ValueError:
        year = 0
    genre = input("Enter the genre(s) to filter by (separate by commas for multiple genres): ")
    try:
        n = int(input("Enter the number of top-rated movies to return (0 for all movies): "))
    except ValueError:
        n = 0

    movies_data = read_file(file_path, year)
    if movies_data:
        top_movies = top_n(movies_data, genre, n)
        if top_movies:
            write_file(top_movies, 'top_movies.txt')
            print("The top-rated movies have been written to 'top_movies.txt'.")
        else:
            print("No movies found for the given criteria.")
    else:
        print("No valid data found for the given input.")


if __name__ == "__main__":
    # import doctest
    # print(doctest.testmod())

    main()
