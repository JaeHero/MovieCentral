import pandas as pd
import requests
import json
import os

file_path = "C:\\Users\\jdher\\Downloads\\title_id_map.csv"
df = pd.read_csv(file_path)

def query_csv(value):
    filtered_df = df[df[' Title'] == value]
    return filtered_df

def main():
    search_value = input('Enter a movie or tv show: ')

    result = query_csv(search_value)

    if not result.empty:
        watchmode_id = result['Watchmode ID'].iloc[0]
    else:
        watchmode_id = None


    if watchmode_id is not None:
        print(watchmode_id)
        search_type = input('Would you like to receive details, sources, or cast-crew ?\n ')
    else:
        print("Watchmode ID not found")

    if watchmode_id is not None and search_type in ['details', 'sources', 'cast-crew']:
        # API endpoint
        url = "https://api.watchmode.com/v1/title/{}/{}/?apiKey=SZicWMb0OHWlsXVWF03oMnGctBKy51Ps1IPQbZeh".format(
            watchmode_id, search_type)

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            if search_type == "details":
                plot_overview = data.get("plot_overview", "Plot overview not available")
                title = data.get("title", "Title not available")
                genres = data.get("genre_names", "Genres not available")
                releaseDate = data.get("release_date", "Release Date not available")
                trailer = data.get("trailer", "Trailer not available")

                print("\n" + title + " Details : ")
                print(plot_overview)
                print(genres)
                print(releaseDate)
                print(trailer)

            elif search_type == "sources":
                for x in data:
                    print(x.get("name", "Source does not exist"))
                    print(x.get("web_url", "URL does not exist"))

            else:

                for x in data:
                    if(x.get("type") == "Crew"):
                        continue

                    print("Crew member name: " + x.get("full_name", "Crew member name not available"))
                    print(x.get("type", "type not available"))
                    print("Crew member role: " + x.get("role", "Crew member role not available"))
                    print("\n")

        else:
            print("Failed to retrieve data, status code: {}".format(response.status_code))

    else:
        print("Invalid input or Watchmode ID not provided")

    retry = input("\nEnter yes to rerun or any other key to exit: ")
    if retry == "Yes" or retry=="yes":
        main()
main()