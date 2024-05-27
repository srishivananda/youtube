#!env python3

# imports
import argparse

import youtubeutils as yt

# create a parser, add month and year parameters
parser = argparse.ArgumentParser()
parser.add_argument("--source", type=str, required=True, help="playlist to copy from")
parser.add_argument("--target", type=str, required=True, help="playlist to copy to")

# parse command line inputs
args = parser.parse_args()

# extract year and month from command line
from_playlist_id = args.source
to_playlist_id = args.target

seen = {}

print("copying videos from " + from_playlist_id + " to " + to_playlist_id)

# fetch to playlist video
to_playlist = yt.playlist(to_playlist_id)
to_playlist_videos = yt.playlist_videos(to_playlist)

# fetch from playlist video
from_playlist = yt.playlist(from_playlist_id)
from_playlist_videos = yt.playlist_videos(from_playlist)

for item in from_playlist:
        # fetch the details of the playlist item
        item_id = item['id']
        video_id = item['contentDetails']['videoId']
        title = item['snippet']['title']

        # fetch the details of the video
        video = from_playlist_videos[video_id]
        views = int(video['statistics']['viewCount'])
        
        if video_id not in to_playlist_videos and views >= 1000000000:
            yt.playlist_insert(to_playlist_id, video_id)
        else:
            print(f"   Skipped Title: {title}, Video ID: {video_id}")
