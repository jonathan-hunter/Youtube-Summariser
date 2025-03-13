"""
YouTube Video Summariser
This script fetches the transcript of a YouTube video and generates a summary and tags for the video.
"""

#### Import the required libraries
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import openai
import re
import os
import sys
from datetime import date

#### Input variables
openai.api_key =   os.getenv('OPENAI_API_KEY') # Set the OpenAI API key
youtube_api_key = os.getenv('YOUTUBE_API_KEY') # Set the YouTube API key

# Set the YouTube video ID from the command line argument
video_id = sys.argv[1]

# Set the TEST YouTube video ID
#video_id = 'dQw4w9WgXcQ'

#### Functions
# Wrapper Function - fetch YouTube video transcript, generate summary, tags and export to md file
def yt_summariser(video_id):
    # Function - fetch YouTube video transcript
    def get_transcript(video_id):
        """
        Fetches the transcript of a YouTube video.
        Args:
            video_id (str): The YouTube video ID.
        Returns:
            str: The transcript of the YouTube video.
        """
        
        # Fetch the transcript of the video
        transcripts = YouTubeTranscriptApi.get_transcripts([video_id], languages=['en'])

        # Concatenate the text from the transcript
        output = []
        for key, value in transcripts[0].items():
            concat = ""
            for text in value:
                concat = concat+text['text']+" "
        output.append(concat)
        
        # Return the transcript
        return output[0]

    # Function - generate transcript summary
    def summarize_text(text):
        """
        Uses the OpenAI API to generate a summary of the transcript.
        Args:
            text (str): The transcript of the YouTube video.
        Returns:
            str: The summary of the transcript.
        """
        response =  openai.chat.completions.create(
            model="gpt-4o",  # or another valid model name if you have access
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant that summarizes youtube video transcripts.'},
                {'role': 'user', 'content': f'Please provide a concise summary for the following transcript:\n\n{text}, do not include any sponsored or partner content. If appropriate provide a numbered or bulleted list.'}
            ],
            max_tokens=1000,
            temperature=0.5
        )
        return response.choices[0].message.content
    
    # Function - generate transcript summary title
    def generate_title(text):
        """
        Uses the OpenAI API to generate a summary of the transcript.
        Args:
            text (str): The transcript of the YouTube video.
        Returns:
            str: The summary of the transcript.
        """
        response =  openai.chat.completions.create(
            model="gpt-4o-mini",  # or another valid model name if you have access
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant that summarizes youtube video transcripts.'},
                {'role': 'user', 'content': f'Please provide a brief title capturing the video summary content:\n\n{text}, in 3-6 words.'}
            ],
            max_tokens=100,
            temperature=0.5
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content

    # Function - generate tags from summary
    def generate_tags(text):
        """
        Uses the OpenAI API to generate tags for the summary.
        Args:
            text (str): The summary of the transcript.
        Returns:
            str: The tags generated for the summary.
        """
        response =  openai.chat.completions.create(
            model="gpt-4o-mini",  # or another valid model name if you have access
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant that determines representative tags for youtube video summaries.'},
                {'role': 'user', 'content': f'Please provide up to 3 representative tags for the following summary, prefer conceptually broad, single word tags:\n\n{text}.'}
            ],
            max_tokens=100,
            temperature=0.5
        )
        return response.choices[0].message.content

    # Function - extract tags from OpenAI response
    def extract_tags(tags):
        """
        Extracts the tags from the OpenAI response.
        Args:
            tags (str): The tags generated for the summary.
        Returns:
            list: The list of tags generated for the summary.
        """
        tags_list = re.findall(r"\d+\.\s*(.+)$", tags, re.MULTILINE)        # Strip formating and convert tags to python list.
        return tags_list
    
    # Function - get video title and channel name
    def get_video_details(video_id, api_key):
        """
        Fetches the title and channel name of a YouTube video.
        Args:
            video_id (str): The YouTube video ID.
            api_key (str): The YouTube API key.
        Returns:
            str: The title of the YouTube video.
            str: The channel name of the YouTube video.
        """
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.videos().list(
            part='snippet',
            id=video_id
        )
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            video = response['items'][0]['snippet']
            title = video['title']
            channel_name = video['channelTitle']
            return title, channel_name
        else:
            return None, None
       
    # Function - write tags and summary to md file with YAML header
    def write_to_file(summary, tags_list, youtube_title, channel_name, title):
        """
        Writes the summary and tags to a text file with YAML header.
        Args:
            summary (str): The summary of the transcript.
            tags_list (list): The list of tags generated for the summary.
        Returns:
            None
        """
        def strip_special_chars(text):
            return re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        with open(f'sync/youtube_summariser/Output/{strip_special_chars(title)}.md', 'w') as file:
            file.write("---\n")
            file.write(f"Date: {date.today()}\n")
            file.write("\"[[Tags]]\":\n")
            for tag in tags_list:
                file.write(f"  - \"[[{tag.strip()}]]\"\n")
            file.write(f"Yotube Video Title: {youtube_title}\n")
            file.write(f"Youtube Channel Name: {channel_name}\n")
            file.write(f"Youtube Video ID: {video_id}\n")
            file.write(f"Youtube Video URL: https://www.youtube.com/watch?v={video_id}\n")
            file.write("---\n")
            file.write(summary)
            
    # Fetch the transcript of a YouTube video and generate a summary and tags
    transcript = get_transcript(video_id)
    summary = summarize_text(transcript)
    title = generate_title(summary)
    tags = generate_tags(summary)
    tags_list = extract_tags(tags)
    youtube_title, channel_name = get_video_details(video_id, youtube_api_key)
    write_to_file(summary, tags_list, youtube_title, channel_name, title)

#### Execute the wrapper function    
yt_summariser(video_id)