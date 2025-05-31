from googleapiclient.discovery import build
from youtube.api_key import API_KEY

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_id_by_handle(handle):
    request = youtube.search().list(
        part='snippet',
        q=f'@{handle}',
        type='channel',
        maxResults=1
    )
    response = request.execute()
    if response['items']:
        return response['items'][0]['snippet']['channelId']
    return None
