import os
import json
import time
import pandas as pd
from datetime import datetime

from youtube.get_channel_id import get_channel_id_by_handle
from youtube.get_video_id import get_latest_video_ids
from youtube.get_video_stats import get_video_statistics
from youtube.get_channel_subscriber import get_channel_subscriber_count

DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_and_save_data():
    all_data = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    channels = [
        {"handle": "@ChimChakMan_Official", "category": "Entertainment"},
        {"handle": "@GABEEGIRL", "category": "Entertainment"},
        {"handle": "@bokyemtv", "category": "Entertainment"},
        {"handle": "@미미미누", "category": "Entertainment"},
        {"handle": "@15ya_egg", "category": "Entertainment"}, #5
        {"handle": "@LCK", "category": "Gaming"},
        {"handle": "@GH.S", "category": "Gaming"},
        {"handle": "@두치와뿌꾸", "category": "Gaming"},
        {"handle": "@pray94", "category": "Gaming"},
        {"handle": "@군림보", "category": "Gaming"}, #5
        {"handle": "@이과형", "category": "Science"},
        {"handle": "@scoopknowledge", "category": "Science"},
        {"handle": "@codingapple", "category": "Science"},
        {"handle": "@ebs.science - 사이언스", "category": "Science"},
        {"handle": "@YTNSC", "category": "Science"}, #5
        {"handle": "@miso_ara", "category": "Pet"},
        {"handle": "@Bodeumofficial", "category": "Pet"},
        {"handle": "@oneroomcat", "category": "Pet"},
        {"handle": "@meow_dad", "category": "Pet"},
        {"handle": "@timon_sns", "category": "Pet"} #5
    ]

    for channel in channels:
        handle = channel["handle"]
        category = channel["category"]
        channel_id = get_channel_id_by_handle(handle)
        if not channel_id:
            print(f"[Warning] 채널 ID를 찾을 수 없습니다: @{handle}")
            continue
        
        subscriber_count = get_channel_subscriber_count(channel_id)
        video_ids = get_latest_video_ids(channel_id, max_results=10)

        for video_id in video_ids:
            view_count, like_count, comment_count = get_video_statistics(video_id)
            record = {
                "timestamp": timestamp,
                "category": category,
                "channel_id": channel_id,
                "channel_handle": handle,
                "video_id": video_id,
                "view_count": view_count,
                "like_count": like_count,
                "comment_count": comment_count,
                "subscriber_count": subscriber_count
            }
            all_data.append(record)
            print(f"[Info] 수집 완료: @{handle}, 영상ID: {video_id}")

    # JSON 저장
    json_file = os.path.join(DATA_DIR, 'raw_data.json')
    with open(json_file, 'a', encoding='utf-8') as f:
        for record in all_data:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    # CSV 저장
    csv_file = os.path.join(DATA_DIR, 'processed_data.csv')
    df = pd.DataFrame(all_data)
    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', index=False, header=False)
    else:
        df.to_csv(csv_file, index=False)
    
    print(f"[Info] 데이터 저장 완료: {timestamp}")

if __name__ == "__main__":
    print("[Start] 유튜브 채널 데이터 수집 시작")
    while True:
        try:
            fetch_and_save_data()
            print("[Info] 다음 실행까지 대기 중... (1시간)")
            time.sleep(3600)
        except Exception as e:
            print(f"[Error] 데이터 수집 중 오류 발생: {e}")
            time.sleep(60)
