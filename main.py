import json
from youtube.api_key import API_KEY
from youtube.get_channel_id import get_channel_id_by_handle
from youtube.get_channel_subscriber import get_channel_subscriber_count
from youtube.get_video_id import get_latest_video_ids
from youtube.get_video_stats import get_video_statistics

def save_data_to_json(data, filename='youtube_data.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"데이터가 '{filename}'에 저장되었습니다.")

if __name__ == "__main__":
    handle = 'LCK'  # 예시 핸들
    channel_id = get_channel_id_by_handle(handle)
    print(f"채널 ID: {channel_id}")

    subscriber_count = get_channel_subscriber_count(channel_id)
    print(f"채널 구독자수: {subscriber_count}")

    video_ids = get_latest_video_ids(channel_id, max_results=3)
    print(f"최근 3개 영상 ID: {video_ids}")

    data = []
    for video_id in video_ids:
        view_count, like_count, comment_count = get_video_statistics(video_id)
        data.append({
            'channel_id': channel_id,
            'subscriber_count': subscriber_count,
            'video_id': video_id,
            'view_count': view_count,
            'like_count': like_count,
            'comment_count': comment_count
        })

    save_data_to_json(data)
