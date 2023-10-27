import requests
import re
from bs4 import BeautifulSoup
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
url = "https://www.imdb.com/chart/top"
imbd_url = 'https://www.imdb.com'
def get_next_page_details(title_url:str):
    url = imbd_url + title_url
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      soup = BeautifulSoup(response.text,'html.parser')
      geners = soup.find_all("a", class_="ipc-metadata-list-item__list-content-item")
      gener_list = soup.find_all('a', class_='ipc-chip ipc-chip--on-baseAlt')
      review_title = soup.find('span', class_='sc-27d2f80b-1').text.strip()
      top_review = soup.find('div', class_='ipc-html-content-inner-div').text.strip()

      all_geners = []
      for g in gener_list:
        all_geners.append(g.find('span', class_='ipc-chip__text').text.strip())


      # print(all_geners)
    else:
      all_geners = []
      print("next page is loade failed")
    return all_geners,review_title,top_review,

response = requests.get(url, headers=headers)
# match = re.search(r'(\d+\.\d+)', text)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    movie_id = []
    movie_name = []
    released_year = []
    movie_rating = []
    movie_duration = []
    censor_certificate = []
    total_ratings = []
    all_geners = []
    top_rating = []
    top_review_titles = []

    # Find and iterate over the movie entries with the specified class
    movie_entries = soup.find_all("li", class_="ipc-metadata-list-summary-item")
    index = 1
    for movie in movie_entries:
        # Extract movie data from each movie entry
        next_page_href = movie.find('a').get('href')
        
        geners, top_review_title, top_review = get_next_page_details(next_page_href)
        top_review_titles.append(top_review_title)
        top_rating.append(top_review)
        gener = " | ".join(geners)
        all_geners.append(gener)
        movie_name_with_index:str = movie.find("h3", class_="ipc-title__text").text.strip()
        if movie_name_with_index.count('.') == 1:
            [mv_index, mv_name] = movie_name_with_index.split('.')
        else:
            [mv_index, *mv_names] = movie_name_with_index.split('.')
            mv_name = ".".join(mv_names)
            # mv_name = mv_names.j
        movie_id.append(mv_index)
        movie_name.append(mv_name)
        released_year.append(movie.find("span", class_="sc-c7e5f54-8").text.strip())
        movie_duration.append(movie.select(".sc-c7e5f54-8")[1].text.strip())
        censor_certificate.append(movie.select(".sc-c7e5f54-8")[-1].text.strip())
        rating_full = movie.find("span", class_="ipc-rating-star").text.strip()
        match = re.search(r'(\d+\.\d+)', rating_full)
        if match:
            extracted_value = match.group(1)
        else:
            extracted_value = 5.0
        movie_rating.append(extracted_value)

        total_rating_text = movie.find("span", class_="ipc-rating-star--voteCount").text.strip()
        match = re.search(r'([\d.]+[MKB]?)', total_rating_text)

        if match:
            rating = match.group(1)
            # print(extracted_value)
        total_ratings.append(rating)
        # top_rating.append(movie.find("span", class_="ipc-metadata-list-item").text.strip())
        index += 1
    with open("imdb_top_rated_movies.csv", "w", newline="") as csvfile:
        fieldnames = ["movie_id", "movie_name", "released_year", "movie_duration", 
                      "censor_certificate","rating", "geners","total_ratings", "top_rating_title", "top_rating"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(movie_id)):
            writer.writerow({
                "movie_id": movie_id[i],
                "movie_name": movie_name[i],
                "released_year": released_year[i],
                "movie_duration": movie_duration[i],
                "censor_certificate": censor_certificate[i],
                "rating": movie_rating[i],
                "geners": all_geners[i],
                "total_ratings": total_ratings[i],
                "top_rating_title": top_review_titles[i],
                "top_rating":top_rating[i]
            })

else:
    print("Failed to retrieve data from IMDb.")
