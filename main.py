import gspread
from oauth2client.service_account import ServiceAccountCredentials
from imdb import IMDb


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/jerin.sr/Projects/discG/credentials.json', scope)
client = gspread.authorize(creds)

spreadsheet_name = 'DVD Collection Temp'
your_personal_email = 'jerinsr19@gmail.com'  # Change this to your Google account email

try:
    spreadsheet = client.open(spreadsheet_name)
    print(f"Spreadsheet '{spreadsheet_name}' already exists.")
except gspread.exceptions.SpreadsheetNotFound:
    spreadsheet = client.create(spreadsheet_name)
    print(f"Created new spreadsheet named '{spreadsheet_name}'.")

spreadsheet.share(creds.service_account_email, perm_type='user', role='writer')
spreadsheet.share(your_personal_email, perm_type='user', role='writer')
print(f"Shared spreadsheet '{spreadsheet_name}' with {your_personal_email}.")

spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
print(f"Access your spreadsheet here: {spreadsheet_url}")

ia = IMDb()
def fetch_movie_data(title):
    movies = ia.search_movie(title)
    if movies:
        movie = ia.get_movie(movies[0].movieID)
        return {
            "Director": ', '.join(str(d) for d in movie.get('directors', [])),
            "Genre": ', '.join(movie.get('genres', [])),
            "Actors": ', '.join(str(a) for a in movie.get('cast', [])[:5]),
            "Duration": movie.get('runtimes', ['Unknown'])[0],
            "Language": ', '.join(movie.get('languages', [])),
            "Rating": movie.get('rating', 'NR'),  
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
        sheet = spreadsheet.sheet1 
        sheet.append_row([title] + list(user_data.values()))

print("Data has been saved to your Google Sheet.")

