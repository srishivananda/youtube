#!env python3

# imports
import re
import logging

import youtubeutils as yt

for language in yt.playlists:
    print(language)

    language_playlists = yt.playlists[language]['playlists']
    playlist_languages = yt.playlists[language]['languages']
    for year in language_playlists:
        print(" " + str(year))
        playlist_id = language_playlists[year]
        playlist = yt.playlist(playlist_id)
        videolist = yt.playlist_videos(playlist)

        seen = {}
        for item in playlist:
            try:
                # fetch the details of the playlist item
                item_id = item['id']
                playlist_id = item['snippet']['playlistId']
                video_id = item['contentDetails']['videoId']

                # fetch the details of the video
                video = videolist[video_id]
                video_title = video['snippet']['title']
                views = int(video['statistics']['viewCount'])
                published = video['snippet']['publishedAt']
                published_year = int(published[0:4])

                video_language = "**"
                if "defaultAudioLanguage" in video['snippet']:
                    video_language = video['snippet']["defaultAudioLanguage"][0:2].lower() 

                # handy debug print when needed
                # print(" : ".join([item_id, playlist_id, video_id, str(published_year), str(views)]))

                # delete if the language is not a match
                if video_language not in playlist_languages:
                    yt.playlist_delete(playlist_id, item_id)

                # delete items with less than 1M views
                if views < 1000000:
                    yt.playlist_delete(playlist_id, item_id)

                # delete items that do not match "trailer"
                if not re.search(r'trailer', video_title, flags=re.IGNORECASE):
                    yt.playlist_delete(playlist_id, item_id)
               
                # dedupe
                if video_id in seen:
                    yt.playlist_delete(playlist_id, item_id)
                else:
                    seen[video_id] = 1

                # if the target year does not have a playlist, move it to 2010 playlist
                if published_year not in language_playlists.keys():
                    published_year = 2010
                     
                # relocate by published year
                # add to the right playlist, remove from the wrong playlist
                # yes, this will remove videos for years with no playlists
                if year != published_year:
                    target_playlist_id = language_playlists[published_year]
                    print("  Moving video " + video_id + " from " + playlist_id + " to " + target_playlist_id) 
                    yt.playlist_insert(target_playlist_id, video_id)

                    # remove from the playlist it does not belong to
                    yt.playlist_delete(playlist_id, item_id)

            except Exception as exception:
                logging.warning(str(exception))