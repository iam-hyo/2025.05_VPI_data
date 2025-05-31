from googleapiclient.discovery import build
from youtube.api_key import API_KEY

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_latest_video_ids(channel_id, max_results=3):
    request = youtube.search().list(
        part='id',
        channelId=channel_id,
        order='date',
        maxResults=max_results,
        type='video'
    )
    response = request.execute()
    video_ids = []
    for item in response['items']:
        video_ids.append(item['id']['videoId'])
    return video_ids
