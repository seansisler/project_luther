import cloudscraper
scraper = cloudscraper.create_scraper()
import time
from bs4 import BeautifulSoup
import re
import publicsuffix
import urllib.parse

def get_page(url, root=False):
    """
    URL is provided and the output should be the scraped page's HTML. There are many different request attempts 
    before False is returned, meaning that the URL should be set aside to try again later or find another means
    to scrape it. 
    """
    
    user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    ]
    
    headers1 = {'User-Agent': np.random_choice(user_agent_list)}
    
    headers2 = {'User-Agent': np.random_choice(user_agent_list), 
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8', 
                'Connection': 'keep-alive'}

    response = requests.get(url)
    if response.status_code == 200:
        time.sleep(3)
        return bs(response.text, 'html.parser')
    
    time.sleep(5)
    response = scraper.get(url, headers=headers)
    if response.status_code == 200:
        time.sleep(3)
        return bs(response.text, 'html.parser')
    
    time.sleep(5)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        time.sleep(3)
        return bs(response.text, 'html.parser')
    time.sleep(3)
    
    response = scraper.get(url, headers=headers2)
    if response.status_code == 200:
        time.sleep(3)
        return bs(response.text, 'html.parser')
    time.sleep(5)
    
    response = requests.get(url, headers=headers2)
    if response.status_code == 200:
        time.sleep(3)
        return bs(response.text, 'html.parser')
    time.sleep(5)
    
    ## getting root of url
    if not root:
        psl = publicsuffix.fetch()
        hostname = parse.urlparse(url).hostname
        root = publicsuffix.get_public_suffix(hostname, psl)
        
    ## getting cookies to try one last time
    session = requests.Session()
    cookies = session.get(root)
    response = requests.get(url, cookies=cookies, header=headers1)
    if response.status_code == 200:
        time.sleep(3)
        return bs(response.text, 'html.parser')
    
    ## one last try for the sake of hope
    response = scraper.get(url)
    if response.status_code == 200:
        time.sleep(3)
        return False
    else:
        return bs(response.text, 'html.parser')
    
def page_movies_info(html):
    """
    Takes a list of HTMLs, each HTML being the webpage that had the results for 100 movies in the rank from highest metascore to the lowest. Returns a DataFrame with the release date, the link to the individual film, the MPAA rating, and the metacritic and userscore. 
    """
    all_movies = []
    tables = bs.find_all('table')
    for table in tables:
        movies = table.find_all('td', class_='clamp-summary-wrap')
        for movie in movies:
            title_link = movie.find('a', class_="title", href=True)
            title = title_link.text
            href = title_link['href']
            link = f'https://www.metacritic.com/{href}'
            release_details = movie.find('div', class_="clamp-details")
            release_date = release_details.find('span', class_=False).text
            mpaa = release_details.find('span', class_=True)
            if mpaa is None:
                mpaa = 'Not Rated'
            else:
                mpaa = mpaa.text.replace('|', '').strip()
            metacritic = movie.find('div', class_="clamp-metascore").text.replace('Metascore:', '').strip()
            userscore = movie.find('div', class_='clamp-userscore').text.replace('User Score:', '').strip()
            all_movies.append([title, release_date, link, mpaa, metacritic, userscore])
    df =  pd.DataFrame(all_movies, columns=['title', 'release_date', 'link', 'mpaa', 'metacritic', 'userscore'])
    df.release_date = pd.to_datetime(df.release_date)
    return df   

    
def get_cast_crew_details_page(row):
    """
    Takes in the link to another webpage
    """
    link = row.loc['link']
    movie_detail_link = f'{link}/details'
    # return will either be website's HTML or False because we weren't able to webscrape
    return get_page(movie_detail_link, root='https://www.metacritic.com')
    
def table_search(movie_title, role_or_details):
    """
    Takes in the film title and returns a tag to help find the table. 
    """
    table_finder = {
        'ends_with_s': {'Details': f'{movie_title} Details and Credits', 
                        'Director': f"{movie_title}' Director Credits", 
                        'Writer': f"{movie_title}' Writer Credits", 
                        'Principle cast': f"{movie_title}' Principal Cast Credits",
                        'Supporting cast': f"{movie_title}' Cast Credits",
                        'Producer': f"{movie_title}' Producer Credits"},
                    
        'other': {'Details': f'{movie_title} Details and Credits', 
                  'Director': f"{movie_title}'s Director Credits", 
                  'Writer': f"{movie_title}'s Writer Credits", 
                  'Princple cast': f"{movie_title}'s Principal Cast Credits", 
                  'Supporting cast': f"{movie_title}'s Cast Credits", 
                  'Producer': f"{movie_title}'s Producer Credits"}
                   }
    
    if movie_title[-1] in ['s', 'S']:
        table = table_finder['ends_with_s'][role_or_details]
    else:
        table = table_finder['other'][role_or_details]
        
    return table




def get_details(htmls, movie_list):
    credit_details = []
    count = 0
    for html in htmls:
        
        if not html:
            credit_details.append([count, None, None])
            count += 1
            continue
        
        movie_title = movie_list.iloc[0]['movie_title']
        year = movie_list.iloc[0]['release_date'].year
        
        table_details = html.find('table', class_="details", 
                                  summary=table_search(movie_title, 
                                                       'Details'))
        if not table_details:
            table_details = html.find('table', class_="details", 
                                      summary=f'{movie_title} ({year}) Details and Credits')
            if not table_details: 
                credit_details.append([count, None, None])
                count += 1
                continue
    
        detail_trs = table_details.find_all('tr')
        for tr in detail_trs:
            label = ''.join(tr['class']).strip().replace('_', ' ')
            data = tr.find('td', class_='data').text.strip()
            credit_details.append([count, label, data])
            count += 1
            
    return pd.DataFrame(credit_details, columns=['movie_id', 'label', 'data'])
    
def get_cast_crew(htmls, movie_list):
    
    ## all data that is collected from metacritic will be appended here and then we will insert into PostgreSQL
    cast_crew_credits = []
    
    ## the count will help us keep track of the movie ID that we are on so that everything matches up at the end 
    ## to insert into PostgreSQL
    count = 0
    for html in htmls:
        
        # append the count and None values to mark there was no html for this and then move on to the next html
        if not html:
            cast_crew_credits.append([count, None, None, None])
            count += 1
            continue 
        
        # otherwise, first step is to look up the name of the movie
        movie_title = movie_list.iloc[0].movie_title
        
        # find director table
        table_directors = soup.find('table', class_="credits", 
                                    summary=table_search(movie_title, 'Director'))
        
        # if no table move on 
        if not table_directors:
            cast_crew_credits.append([count, None, None, None])
            
        # look up the value for the director(s) and append them to the list
        else:
            director_tds = table_directors.find_all('td', class_="person")
            for td in director_tds:
                label = 'Director'
                data = get_person(tr)
                href = get_href(tr)
                cast_crew_credits.append([count, label, data, link])
                
        ## for the writers, cast members, and other production workers the same operation as above will happen
        table_writers = soup.find('table', class_="credits", 
                                  summary=table_search(movie_title, 'Writer'))
        if table_writers is None:
            cast_crew_credits.append([count, None, None, None])   
        else:
            writer_tds = table_writers.find_all('td', class_="person")
            for td in writer_tds:
                label = 'Writer'
                data = get_person(tr)
                href = get_href(tr)
                cast_crew_credits.append([count, label, data, link])

        table_prin_cast = soup.find('table', class_="credits", 
                                    summary=table_search(movie_title, 'Principle cast'))
        if table_prin_cast is None:
            cast_crew_credits.append([count, None, None, None])
        else:
            prin_cast_tds = table_prin_cast.find_all('td', class_="person")
            for td in prin_cast_tds:
                label = 'Principle Cast'
                data = get_person(tr)
                href = get_href(tr)
                cast_crew_credits.append([count, label, data, link])

        table_cast = soup.find('table', class_="credits", 
                               summary=table_search(movie_title, 'Supporting cast'))
        if table_cast is None:
            cast_crew_credits.append([count, None, None, None])
        else:
            cast_tds = table_cast.find_all('td', class_="person")
            for td in cast_tds:
                label = 'Cast (non-principle)'
                data = get_person(tr)
                href = get_href(tr)
                cast_crew_credits.append([count, label, data, link])

        table_producer = soup.find('table', class_="credits", 
                                   summary=table_search(movie_title, 'Producer'))
        
        if table_producer is None:
            ## adding one to the count because this is the last step for current row, if table is existant then 
            ## one will be added to the count below
            cast_crew_credits.append([count, label, data, link])   
            count += 1
                                    
        else:       
            producer_trs = table_producer.find_all('tr')
            for tr in producer_trs:
                label = get_label(tr)
                if not label:
                    cast_crew_credits.append([count, label, data, link])
                else:
                    data = get_person(tr)
                    href = get_href(tr)
                    cast_crew_credits.append([count, label, data, link])
            count += 1
    return pd.DataFrame(cast_crew_credits, columns=['movie_id', 'label', 'person', 'link'])
    
                    
def get_label(data):
    "Returns the role or credit a person or item had in the film."
    label = data.find('td', class_="role")
    if not label:
        return False
    return label.text.strip()

def get_person(data):
    "Returns the person or text for an item in the HTML."
    wanted = data.find('a')
    return wanted.text.strip()

def get_href(data):
    "Return the link back for a page's link to another page. "
    wanted = data.find('a')
    href = wanted['href'].strip()
    if not href:
        link = np.nan
    else:
        link = f'https://www.metacritic.com{href}'
    return link

def get_metacritic(start_page=0, end_page=136, list_of_pages=False):
    """
    The input for this function is set to how many pages of released films there were at the time. Should this 
    code be reused the pages can be set to whatever need be. The first page that shows up with top scoring movie 
    #1 to #100 is considered page 0 in the URL. 
    The return consists of the retry pages that will need to be run again, the list of all films and their scores as well as release dates, the cast and crew involved with each film, and the runtime, production company, etc details. 
    """
    if not list_of_pages:
        pages = range(startpage, end_page+1)
    else:
        pages = list_of_pages
    metacritic_scores_dates = False
    retry = []
    cast_crew_retry = []
    details = False
    cast_crew = False
    for page in pages:
        html = get_html(f'https://www.metacritic.com/browse/movies/score/metascore/all/filtered?page={page}')
        if not html:
            retry.append(page)
            continue 
        films_list = page_movies_info(html)
        
        if not metacritic_scores_dates:
            metacritic_scores_dates = films_list
        else:
            metacritic_scores_date = pd.concat([metacritic_score_dates, films_list])
        
        movie_credit_htmls = films_list.apply(lambda x: get_cast_crew_details_page(row=x['link']))
        film_details = get_details(movie_credit_htmls, films_list)
        cast_crew_credits = get_cast_crew(movie_credit_htmls, films_list)
        
        ## if details is still None then we are assigning it the first DataFrame
        if not details:
            details = film_details
        ## if details is assigned a DataFrame then we are assigning it the concat of the two
        else:
            details = pd.concat([detail, film_details])
        ## the same deal with the cast and crew DataFrame and the cast_crew variable
        if not cast_crew:
            cast_crew = cast_crew_credits
        else:
            cast_crew = pd.concat([cast_crew, cast_crew_credits])
        
    return retry, metacritic_scores_dates, details, cast_crew
    