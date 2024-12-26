# YouTube Video Scraper

This Python project scrapes YouTube videos based on a specified genre and saves detailed information about the videos in a CSV format. It uses the YouTube API and YouTube Transcript API to fetch video details, including descriptions, view counts, captions, and more.

## Features:
- Fetches up to 500 videos of a specific genre.
- Sorts the videos by view count.
- Extracts video details (e.g., title, description, channel, views).
- Fetches additional metadata like video duration, tags, and topics.
- Downloads captions if available for each video.
- Saves the combined data (video details, captions) in a CSV file.

## Requirements:
- Python 3.x
- `googleapiclient` (for interacting with YouTube API)
- `youtube_transcript_api` (for fetching captions)
- `pandas` (for storing and handling video data)
- `isodate` (for parsing ISO 8601 video durations)

## Setup:
1. Clone the repository:
   ```bash
   git clone https://github.com/Preethamvarma/Youtube_Scrapping.git
   ```

2. Install the required libraries:
   ```bash
   pip install google-api-python-client youtube-transcript-api pandas isodate
   ```

3. Replace the `API_KEY` in the code with your own [YouTube API key](https://developers.google.com/youtube/registering_an_application).

## Usage:
1. Run the script:
   ```bash
   python script_name.py
   ```

2. When prompted, enter a genre (e.g., "Technology", "Music", "Education").
3. The script will fetch the top 500 videos in that genre, gather additional metadata, fetch captions (if available), and save the data in a CSV file.

## Output:
The data will be saved as `genre_videos.csv`, containing the following columns:
- Video ID
- Title
- Description
- Channel Title
- Published At
- Video URL
- Keyword Tags
- Category ID
- Duration
- View Count
- Comment Count
- Location of Recording
- Topics
- Captions Available
- Caption Text

## Example:
For a genre like "Technology", the script will output a CSV with details like:

```plaintext
Video ID, Title, Description, Channel Title, Published At, Video URL, ...
```
