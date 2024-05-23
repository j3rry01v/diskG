import gspread
from oauth2client.service_account import ServiceAccountCredentials
from imdb import IMDb

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_credentials_file.json', scope)
client = gspread.authorize(creds)
sheet = client.open('DVD Collection temp').sheet1 


ia = IMDb()
def fetch_movie_data(title):
    movies = ia.search_movie(title)
    if movies:
        movie = ia.get_movie(movies[0].movieID)
        return {
            "Director": ', '.join(str(d) for d in movie.get('directors', [])),
            "Genre": ', '.join(movie.get('genres', [])),
            "Actors": ', '.join(str(a) for a in movie.get('cast', [])[:5]),  # Top 5 actors
            "Duration": movie.get('runtimes', ['Unknown'])[0],
            "Language": ', '.join(movie.get('languages', [])),
            "Rating": movie.get('rating', 'NR'),  # Not Rated if not available
            "Release Date": movie.get('year', 'Unknown'),
            "Studio": ', '.join(str(c) for c in movie.get('production companies', []))
        }
    return None


title = input("Enter the DVD title: ")
user_data = fetch_movie_data(title)


if user_data:
    print("Found data for the movie:")
    for key, value in user_data.items():
        print(f"{key}: {value}")

    save = input("Save this information to Google Sheets? (yes/no): ")
    if save.lower() == 'yes':
        sheet.append_row([title] + list(user_data.values()))

print("Data has been saved to your Google Sheet.")


