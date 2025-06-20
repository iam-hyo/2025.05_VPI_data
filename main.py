import os
import json
import time
import pandas as pd
from datetime import datetime
import logging

logging.info("코드 실행 시작")
logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

from youtube.api_key import build_youtube_with_fallback #전역 Youtube 객체
from youtube.get_channel_id import get_channel_id_by_handle
from youtube.get_video_id import get_latest_video_ids
from youtube.get_video_stats import get_video_statistics_batch
from youtube.get_channel_subscriber import get_channel_subscriber_count
from youtube.get_video_id_byPlaylist import get_min_10_video_ids_recent_priority #크레딧최적화 test code

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
        {"handle": "@15ya_egg", "category": "Entertainment"},  # 5
        {"handle": "@LCK", "category": "Gaming"},
        {"handle": "@GH.S", "category": "Gaming"},
        {"handle": "@두치와뿌꾸", "category": "Gaming"},
        {"handle": "@pray94", "category": "Gaming"},
        {"handle": "@군림보", "category": "Gaming"},  # 5
        {"handle": "@이과형", "category": "Science"},
        {"handle": "@scoopknowledge", "category": "Science"},
        {"handle": "@codingapple", "category": "Science"},
        {"handle": "@ebs.science - 사이언스", "category": "Science"},
        {"handle": "@YTNSC", "category": "Science"},  # 5
        {"handle": "@miso_ara", "category": "Pet"},
        {"handle": "@Bodeumofficial", "category": "Pet"},
        {"handle": "@oneroomcat", "category": "Pet"},
        {"handle": "@meow_dad", "category": "Pet"},
        {"handle": "@timon_sns", "category": "Pet"},  # 5
        {"handle": "@hankooktire_global", "category": "AUTO"},
        {"handle": "@차의세계", "category": "AUTO"},
        {"handle": "@black-box", "category": "AUTO"},
        {"handle": "@HANMOONCHULTV", "category": "AUTO"},
        {"handle": "@mocar_official", "category": "AUTO"}, #5
        {"handle": "@MBCNEWS11", "category": "News"}, #News
        {"handle": "@jtbc_news", "category": "News"},
        {"handle": "@ytnnews24", "category": "News"},
        {"handle": "@sbsnews8", "category": "News"},
        {"handle": "@channelA-news", "category": "News"},
        {"handle": "@syukaworld", "category": "News"},
        {"handle": "@야신야덕", "category": "Sports"}, #스포츠
        {"handle": "@SPOTIMESPOTV", "category": "Sports"},
        {"handle": "@AllblancTV", "category": "Sports"},
        {"handle": "@JKartsoccer", "category": "Sports"},
        {"handle": "@fitvely", "category": "Sports"}, 
        {"handle": "@피지컬갤러리", "category": "Sports"},
        {"handle": "@TV-rh6mt", "category": "Travel"}, #Travel
        {"handle": "@JBKWAK", "category": "Travel"},
        {"handle": "@TEAMJINU", "category": "Travel"},
        {"handle": "@SindbadAdventure", "category": "Travel"},
        {"handle": "@ddoddunam", "category": "Travel"},
        {"handle": "@tzuyang6145","category": "Food"}, #Foods
        {"handle": "@user-pq8xn3oq9y","category": "Food"},
    ]


    for channel in channels:
        handle = channel["handle"]
        category = channel["category"]
        # 🔥 JSON 경로를 지정하여 호출
        channel_id = get_channel_id_by_handle(handle, json_path='channels/channelIds_V2.json')
        if not channel_id:
            print(f"[Warning] 채널 ID를 찾을 수 없습니다: {handle}")
            continue

        subscriber_count = get_channel_subscriber_count(channel_id)
        # video_ids = get_latest_video_ids(channel_id, max_results=10)
        video_ids = get_min_10_video_ids_recent_priority(channel_id, days=10)


        video_stats_dict = get_video_statistics_batch(video_ids)

        for video_id in video_ids:
            if video_id not in video_stats_dict:
                print(f"[Warning] 영상 정보 조회 실패: {video_id}")
                continue

            view_count, like_count, comment_count, is_short, published_at, video_title = video_stats_dict[video_id]

            record = {
                "timestamp": timestamp,
                "category": category,
                "channel_id": channel_id,
                "channel_handle": handle,
                "video_id": video_id,
                "video_title": video_title,
                "published_at": published_at,
                "is_short": is_short,
                "view_count": view_count,
                "like_count": like_count,
                "comment_count": comment_count,
                "subscriber_count": subscriber_count
            }
            all_data.append(record)
            print(f"[Info] 수집 완료: {handle}, 영상ID: {video_id}")

    # JSON 저장
    json_file = os.path.join(DATA_DIR, 'raw_data.json')
    with open(json_file, 'a', encoding='utf-8') as f:
        for record in all_data:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    # CSV 저장
    # csv_file = os.path.join(DATA_DIR, 'processed_data.csv')
    csv_file = os.path.join(DATA_DIR, 'processed_data_v2.csv')
    df = pd.DataFrame(all_data)
    df['video_id'] = df['video_id'].apply(lambda x: f"'{x}" if isinstance(x, str) and (x.startswith('=') or x.startswith('-')) else x) 
    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', index=False, header=False, encoding='utf-8-sig')
    else:
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')

    print(f"[Info] 데이터 저장 완료: {timestamp}")

if __name__ == "__main__":
    print("[Start] 유튜브 채널 데이터 수집 시작")
    while True:
        try:
            fetch_and_save_data()
            print("[Info] 다음 실행까지 대기 중... (4시간)")
            time.sleep(3600*4)
        except Exception as e:
            print(f"[Error] 데이터 수집 중 오류 발생: {e}")
            time.sleep(60)
