#!/bin/bash
# This script is used to summarise a YouTube video
# It takes the URL of the video as input and passes it to the python script for summarisation.

# Change the directory to the location of the script
cd $HOME/Dropbox/Work/Code/Docker/DS_General/sync/youtube_summariser

# Create the Output directory if it doesn't exist
mkdir -p Output

# Remove the contents of the Output directory
rm -rf Output/*

# Ask user for the URL of the video
echo "Enter the URL of the video you want to summarise"
read url

# Extract the video ID from the URL
video_id=$(echo "$url" | sed -n 's/.*v=\([a-zA-Z0-9_-]\{11\}\).*/\1/p' | head -n1)
echo "YouTube Video ID: $video_id"

# Run the python script in docker container to summarise the video
docker exec -it jeh-ds-general venv/bin/python3 sync/youtube_summariser/yt-summary.py $video_id

# Move the contents of the Output directory to the Obsidian vault
mv Output/* "/home/jeh/Documents/My Obsidian Vault/2 - Source Material/YouTube/"