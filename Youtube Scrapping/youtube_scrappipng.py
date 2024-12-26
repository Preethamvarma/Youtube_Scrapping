import os
import time
import pandas as pd
from googleapiclient.discovery import build  # Library for interacting with YouTube API
from youtube_transcript_api import YouTubeTranscriptApi  # Library for fetching YouTube video transcripts
import isodate  # Library for parsing ISO 8601 duration formats

# Set up YouTube API
API_KEY = "AIzaSyDv0SF_cI4-PXIsFnVe7KVwSrPVM2s0xX4"  # Replace with your YouTube API Key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Initialize YouTube API client
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

# Helper function to convert ISO 8601 duration to a user-friendly format (e.g., PT23S to 00:00:23)
def format_duration(duration):
    """
    Converts ISO 8601 duration format to HH:MM:SS format.
    Example: PT2H15M30S -> 02:15:30
    """
    try:
        # Parse the duration using isodate
        parsed_duration = isodate.parse_duration(duration)
        total_seconds = int(parsed_duration.total_seconds())
        
        # Convert seconds to hours, minutes, and seconds
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Return formatted duration string
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    except:
        # Return default value if parsing fails
        return "00:00:00"

# Function to fetch videos by genre
# This fetches up to 500 videos based on the specified genre and sorts them by view count
def fetch_videos_by_genre(genre, max_results=500):
    videos = []  # List to store video details
    next_page_token = None  # Used for paginated results

    while len(videos) < max_results:
        # Fetch videos from YouTube API with sorting by view count
        request = youtube.search().list(
            q=genre,  # The genre or search term
            part="id,snippet",  # Specify the fields to retrieve
            type="video",  # Fetch only videos (not playlists or channels)
            maxResults=min(50, max_results - len(videos)),  # Fetch up to 50 videos per request
            pageToken=next_page_token,  # Handle pagination
            order="viewCount"  # Sort videos by view count
        )
        response = request.execute()  # Execute the API request

        for item in response.get("items", []):
            video_id = item["id"]["videoId"]  # Extract video ID
            video_data = {
                "Video ID": video_id,
                "Title": item["snippet"]["title"],
                "Description": item["snippet"]["description"],
                "Channel Title": item["snippet"]["channelTitle"],
                "Video Published At": item["snippet"]["publishedAt"],
                "Video URL": f"https://www.youtube.com/watch?v={video_id}"
            }
            videos.append(video_data)  # Append the video data to the list

        next_page_token = response.get("nextPageToken")  # Get the next page token
        if not next_page_token or len(videos) >= max_results:  # Stop if no more pages or max results reached
            break  # Stop if there are no more pages or max results reached

    return pd.DataFrame(videos)  # Return the videos as a DataFrame


# Function to fetch additional details for a list of video IDs
def fetch_video_details(video_ids):
    details = []  # List to store video details

    for i in range(0, len(video_ids), 50):  # Process IDs in batches of 50
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics,topicDetails,recordingDetails",  # Fetch additional details
            id=','.join(video_ids[i:i + 50])  # Join video IDs for the request
        )
        response = request.execute()  # Execute the API request

        for item in response.get("items", []):
            details.append({
                "Video ID": item["id"],
                "Keyword Tags": ', '.join(item.get("snippet", {}).get("tags", [])),
                "YouTube Video Category": item["snippet"].get("categoryId"),
                "Video Duration": item["contentDetails"].get("duration"),
                "View Count": item["statistics"].get("viewCount"),
                "Comment Count": item["statistics"].get("commentCount"),
                "Location of Recording": item.get("recordingDetails", {}).get("locationDescription"),
                "Topics": ', '.join(item.get("topicDetails", {}).get("topicCategories", []))
            })

    return pd.DataFrame(details)  # Return the details as a DataFrame

# Function to check and download captions
def fetch_captions(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)  # Fetch the transcript
        caption_text = ' '.join([entry['text'] for entry in transcript])  # Combine all caption text
        return True, caption_text  # Return captions available and the text
    except:
        return False, None  # Return false if captions are not available

# Main function to generate a CSV for a specified genre
def generate_csv(genre):
    print(f"Fetching videos for genre: {genre}")
    video_data = fetch_videos_by_genre(genre)  # Fetch video details
    print(f"Fetched {len(video_data)} videos.")

    video_details = fetch_video_details(video_data["Video ID"].tolist())  # Fetch additional details
    combined_data = pd.merge(video_data, video_details, on="Video ID", how="left")  # Merge data

    captions_data = []  # List to store captions data
    for video_id in combined_data["Video ID"]:
        captions_available, captions_text = fetch_captions(video_id)  # Fetch captions
        captions_data.append({
            "Video ID": video_id,
            "Captions Available": captions_available,
            "Caption Text": captions_text
        })

    captions_df = pd.DataFrame(captions_data)  # Convert captions data to DataFrame
    final_data = pd.merge(combined_data, captions_df, on="Video ID", how="left")  # Merge captions

    output_file = f"{genre}_videos.csv"  # Specify the output file name
    final_data.to_csv(output_file, index=False)  # Save the data to a CSV file
    print(f"Data saved to {output_file}")

# Entry point of the script
if __name__ == "__main__":
    genre_input = input("Enter a genre (e.g., Technology, Music, Education): ")  # Take genre input
    generate_csv(genre_input)  # Generate the CSV for the specified genre
