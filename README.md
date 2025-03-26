# YouTube Video Summariser

yt-summary.py is a python script to create a markdown summary of a YouTube video by fetching its transcript and using the OpenAI API to generate a summary, title and tags. The video title and channel name are acquired via the YouTube API. Video metadata are saved as a YAML header in the markdown summary.

## Requirements

- Python Environment with `pip install google-api-python-client youtube-transcript-api openai`.
- YouTube and OpenAI API keys passed as environment variables.
- YouTube video ID for summarisation.

## Example Usage Script

yt-summary.sh is included as an example bash script which takes the video URL as an input, extracts the YouTube video ID, passes it to yt-summary.py (in this case run within a docker container) and then copies the output markdown summary to an Obsidian vault.
