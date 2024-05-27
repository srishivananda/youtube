#!env zsh

# copy from "BILLION VIEWS CLUB" to my "Global Billion View Songs"
./youtube-playlist-copy.py --source PL7VuK4dN6eJ3tR7zKE_LWCzXFlAMppXHI --target PL-ra8b28zfm23fRh1nK2S31M8IL2OT2SF

# update the top songs playlists
./youtube-playlist-update.py --year 2999 --name "telugu songs"
./youtube-playlist-update.py --year 2999 --name "hindi songs"

# update playlists for year = 2024
./youtube-playlist-update.py --year 2024 --name "telugu trailers"
./youtube-playlist-update.py --year 2024 --name "hindi trailers"
