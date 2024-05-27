#!env python3

# imports
import argparse

import youtubeutils as yt

# create a parser, add month and year parameters
parser = argparse.ArgumentParser()
parser.add_argument("--year", type=int, required=True, help="year to search videos for")
parser.add_argument("--month", type=int, required=False, help="month to search videos for")
parser.add_argument("--name", type=str, required=False, help="play list name")

# parse command line inputs
args = parser.parse_args()

# extract year and month from command line
year = args.year
month = args.month

seen = {}
names = [args.name] if args.name else yt.playlists.keys()
for name in names:
    print(" : ".join([name, str(year), str(month)]))

    # fetch playlists
    language_playlists = yt.playlists[name]['playlists']

    # fetch playlist video
    playlist_id = language_playlists[year]
    playlist = yt.playlist(playlist_id)
    playlist_videos = yt.playlist_videos(playlist)
    
    # fetch the query for the playlist
    query = yt.playlists[name]['search']
    count = yt.playlists[name]['count']
    playlist_languages = yt.playlists[name]["languages"]

    search_items = []
    # run a search for the query, depending on time window
    if args.month:
        search_items = yt.search_by_year_and_month(query, year, month, count)
    elif args.year < 2999:
        search_items = yt.search_by_year(query, year, count)
    else:
        search_items = yt.search(query, count)

    # get video metadata for search items
    videolist = yt.search_videos(search_items)
    
    # Print the search results (video titles and video IDs)
    for item in search_items:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']   

        # fetch the details of the video
        video = videolist[video_id]
        views = int(video['statistics']['viewCount'])

        video_language = "**"
        if "defaultAudioLanguage" in video['snippet']:
            video_language = video['snippet']["defaultAudioLanguage"][0:2].lower() 

        if (video_id not in playlist_videos
            and video_language in playlist_languages
            and views > 1000000):

            yt.playlist_insert(playlist_id, video_id)
        else:
            print(f"   Skipped id: {video_id} title: {video_title}, , Views: {views}")
