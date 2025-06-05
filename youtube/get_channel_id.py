'''
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
'''

import json

def get_channel_id_by_handle(handle, json_path='channels/channelIds_HJ.json'):
    """
    로컬 JSON 파일에서 채널 핸들을 통해 채널ID를 반환합니다.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        channels = json.load(f)

    for channel in channels:
        if channel['channel_handle'] == handle:
            return channel['channel_id']

    print(f"[Error] 핸들 {handle} 에 해당하는 채널ID를 찾지 못했습니다.")
    return None
