from googleapiclient.discovery import build
from youtube.api_key import build_youtube_with_fallback 

youtube = build_youtube_with_fallback()
# from youtube.api_key import API_KEY
# youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_subscriber_count(channel_id):
    request = youtube.channels().list(
        part='statistics',
        id=channel_id
    )
    response = request.execute()
    if response['items']:
        return int(response['items'][0]['statistics']['subscriberCount'])
    return 0
