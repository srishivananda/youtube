__package__ = "youtubeutils"

# imports
import os
import pickle
import calendar
import datetime

# google api client libraries
import googleapiclient.discovery
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# disable OAuthlib's HTTPS verification when running locally
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# constants
max_results = 50

# youtube API configuration
api_version = "v3"
api_service_name = "youtube"
token_pickle_file = "token.pickle"
client_secrets_file = "client_secret.json"
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# check if token pickle exists
if os.path.exists(token_pickle_file):
    with open(token_pickle_file, "rb") as token:
        credentials = pickle.load(token)
else:
    # get credentials and create an API client
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server()

    # pickle the credentials for the next run
    with open(token_pickle_file, "wb") as token:
        pickle.dump(credentials, token)

# instantiate a youtube api client
youtube = googleapiclient.discovery.build(
    api_service_name,
    api_version,
    credentials=credentials
)

# playlist metadata
playlists = {
    "hindi trailers": {
        "search": "bollywood official trailer intitle:trailer",
        "languages": ["hi", "en"],
        "count": 500,
        "playlists" : {
            2010: 'PL-ra8b28zfm3c0bd79uLk6GMiSAc9emTH',
            2020: 'PL-ra8b28zfm0UOHy9_HojajeGVOw18ek1',
            2021: 'PL-ra8b28zfm0COwM_AYd6iyhX7Wiqii8m',
            2022: 'PL-ra8b28zfm1gmWaHGcooeCBfQ7inn2_N',
            2023: 'PL-ra8b28zfm1fhMcwX6QECZrU022Obntx',
            2024: 'PL-ra8b28zfm15GlLEZe3MfIOd3l-W3yYg',
        }
    },        
    "telugu trailers": {
        "search": "telugu trailer intitle:trailer",
        "languages": ["te"],
        "count": 500,
        "playlists": {
            2010: 'PL-ra8b28zfm22G2TjPv7O-gKdIzvvY4Lr',
            2020: 'PL-ra8b28zfm3LREIB4WKTzEkVacV4D1IW',
            2021: 'PL-ra8b28zfm1lWHIYAydBOXNnBxGspb5J',
            2022: 'PL-ra8b28zfm0_YS1KuUOVQiQC4u252f5q',            
            2023: 'PL-ra8b28zfm0Nv3VbSiUQF-_APfQP0l4x',
            2024: 'PL-ra8b28zfm24ywdN8X2X1TP7sHs2aoMe',
        }
    },
    "hindi songs": {
        "search": "bollywood songs -intitle:live -intitle:rhymes -intitle:kids",
        "languages": ["hi", "en"],
        "count": 50,
        "playlists" : {
            2999: 'PL-ra8b28zfm07uZ3r0-BN4CO5hXWV_4IT',
        }
    },
    "telugu songs": {
        "search": "telugu songs -intitle:live -intitle:rhymes -intitle:kids",
        "languages": ["te", "en", ""],
        "count": 50,
        "playlists" : {
            2999: 'PL-ra8b28zfm3z5sShaR3WNZlzR2Tc_1uI',
        }
    },
}

def playlist(playlist_id):
    # Set the initial value of the next page token
    next_page_token = None

    items = []

    # Iterate until there are no more pages of results
    while True:

        # build the request object
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=max_results,
            playlistId=playlist_id,
            pageToken=next_page_token
        )

        # accumulate the playlist items and the next page token
        response = request.execute()
        items.extend(response['items'])
        next_page_token = response.get("nextPageToken")

        # when there is no more results, bail
        if not next_page_token:
            break

    return items

def search_by_start_and_end_dates(query, sdate, edate, count=500):
    # Set the initial value of the next page token
    next_page_token = None

    items = []
    start = f'{sdate:%Y-%m-%dT00:00:00Z}'
    end = f'{edate:%Y-%m-%dT23:59:59Z}'

    # Iterate until there are no more pages of results
    while True:
        # Perform the search
        request = youtube.search().list(
            part='snippet',
            q=query,
            maxResults=max_results,
            type='video',
            publishedAfter=start,
            publishedBefore=end,
            order='viewCount',
            pageToken=next_page_token
        )
        print(" searching for '" + query + "' between " + start + " and " + end + "")

        # execute request
        response = request.execute()

        items.extend(response['items'])
        next_page_token = response.get("nextPageToken")

        # when there is no more results, bail
        if not next_page_token or len(items) > (count-1):
            break

    return items

def search_by_year_and_month(search, year, month, count):
    (junk, lastday) = calendar.monthrange(year, month)
    sdate = datetime.datetime(year, month, 1)
    edate = datetime.datetime(year, month, lastday)

    return search_by_start_and_end_dates(search, sdate, edate, count)

def search_by_year(search, year, count):
    (junk, lastday) = calendar.monthrange(year, 12)
    sdate = datetime.datetime(year, 1, 1)
    edate = datetime.datetime(year, 12, lastday)

    return search_by_start_and_end_dates(search, sdate, edate, count)

def search(search, count):
    sdate = datetime.datetime(1900, 1, 1)
    edate = datetime.datetime(2029, 12, 31)

    return search_by_start_and_end_dates(search, sdate, edate, count)

def videos(ids):
    items = {}

    # Iterate until there are no more pages of results
    for i in range(0, len(ids), 50):
        id_list = ",".join(ids[i:i+50])
        request = youtube.videos().list(
            part="snippet,statistics",
            id=id_list,
        )

        # Get the playlist items and the next page token
        response = request.execute()
        for item in response['items']:
            items[item['id']] = item

    return items

def playlist_videos(playlist):
    video_map = {}
    for item in playlist: 
        video_id = item['contentDetails']['videoId']
        video_map[video_id] = 1        

    return videos(list(video_map.keys()))

def search_videos(search_items):
    video_map = {}
    for item in search_items: 
        video_id = item['id']['videoId']
        video_map[video_id] = 1        

    return videos(list(video_map.keys()))
    
def playlist_print(playlist):
    for item in playlist: 
        item_id = item['id']
        playlist_id = item['snippet']['playlistId']
        video_id = item['contentDetails']['videoId']

        print("   " + " : ".join([playlist_id, video_id, item_id]))

def playlist_insert(playlist_id, video_id):
    request = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }

    response = youtube.playlistItems().insert(
        part="snippet",
        body=request
    ).execute()
    print("   Adding video " + video_id + " to playlist " + playlist_id)

    return response

def playlist_delete(playlist_id, item_id):
    request = youtube.playlistItems().delete(
        id=item_id
    )
    request.execute()
    print("   Deleting playlist item " + item_id + " from playlist " + playlist_id)
