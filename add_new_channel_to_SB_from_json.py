import os
import json
from youtube.api_key import build_youtube_with_fallback
from typing import List, Dict, Set
from supabase import create_client, Client

# Supabase 설정
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def add_new_channels_only(file_path: str):
    """
    JSON 파일에서 채널 목록을 읽어, DB에 channel_id나 channel_handle이
    존재하지 않는 새로운 채널만 추가합니다.
    """
    try:
        # 1. DB에서 기존 ID와 핸들 목록 가져오기
        print("🔍 데이터베이스에서 기존 채널 ID와 핸들 목록을 가져옵니다...")
        response = supabase.table("channel_admin").select("channel_id, channel_handle").execute()
        
        # Set 자료형으로 만들어 검색 속도를 높임
        existing_ids: Set[str] = {item['channel_id'] for item in response.data}
        existing_handles: Set[str] = {item['channel_handle'] for item in response.data}
        print(f"✅ 기존 데이터 {len(existing_ids)}건 확인 완료.")

        # 2. JSON 파일 열고 데이터 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            channels_from_file: List[Dict] = json.load(f)

        # 3. 중복되지 않은, 진짜 새로운 채널만 필터링
        new_channels_to_add = []
        for channel in channels_from_file:
            # channel_id 와 channel_handle 둘 다 DB에 없어야 함
            if channel['channel_id'] not in existing_ids and \
               channel['channel_handle'] not in existing_handles:
                new_channels_to_add.append(channel)

        if not new_channels_to_add:
            print("\nℹ️ 추가할 새로운 채널 데이터가 없습니다.")
            return

        # 4. 필터링된 새로운 데이터만 DB에 삽입 (insert)
        print(f"\n총 {len(channels_from_file)}개 중 {len(new_channels_to_add)}개의 새로운 채널을 추가합니다...")
        insert_response = supabase.table("channel_admin").insert(new_channels_to_add).execute()

        print("✅ 작업 완료! 새로운 채널만 성공적으로 추가되었습니다.")

    except Exception as e:
        print(f"🚨 데이터 처리 중 오류가 발생했습니다: {e}")

# --- 스크립트 실행 ---
if __name__ == "__main__":
    json_file = './data/channels_full.json'
    add_new_channels_only(json_file)