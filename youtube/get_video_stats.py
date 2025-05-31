from googleapiclient.discovery import build
from youtube.api_key import API_KEY

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_statistics(video_id):
    request = youtube.videos().list(
        part='statistics',
        id=video_id
    )
    response = request.execute()
    if response['items']:
        stats = response['items'][0]['statistics']
        view_count = int(stats.get('viewCount', 0))
        like_count = int(stats.get('likeCount', 0))
        comment_count = int(stats.get('commentCount', 0))
        return view_count, like_count, comment_count
    return 0, 0, 0
