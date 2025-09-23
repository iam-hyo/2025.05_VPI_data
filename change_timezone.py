import os
from datetime import datetime, timedelta, timezone
from supabase import create_client, Client
from dotenv import load_dotenv
import re
from tqdm import tqdm  # ✅ tqdm 추가

# .env 로드
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise ValueError("환경 변수 SUPABASE_URL 또는 SUPABASE_SERVICE_KEY가 없습니다.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

KST = timezone(timedelta(hours=9))
three_weeks_ago_utc = (datetime.utcnow() - timedelta(weeks=3)).isoformat()

# 페이징 처리 설정
BATCH_SIZE = 1000
offset = 0
updated_count = 0
total_batches = 0

while True:
    response = supabase.table("video_snapshots")\
        .select("id, collected_at")\
        .gte("collected_at", three_weeks_ago_utc)\
        .range(offset, offset + BATCH_SIZE - 1)\
        .execute()

    rows = response.data

    if not rows:
        break  # 더 이상 데이터 없음

    print(f"\n🔄 Batch {total_batches + 1} - 처리 중 (총 {len(rows)}개 항목)")

    # ✅ tqdm으로 현재 배치 진행률 표시
    for row in tqdm(rows, desc=f"🧪 Batch {total_batches + 1}", unit="row"):
        snapshot_id = row["id"]
        collected_at_str = row["collected_at"]

        try:
            # 마이크로초 보정
            if "." in collected_at_str:
                collected_at_str = re.sub(
                    r'(\.\d{1,6})(\d*)',
                    lambda m: m.group(1).ljust(7, "0"),
                    collected_at_str
                )

            # 문자열 → datetime
            utc_time = datetime.fromisoformat(collected_at_str)

            if utc_time.tzinfo is None:
                utc_time = utc_time.replace(tzinfo=timezone.utc)

            kst_time = utc_time.astimezone(KST).isoformat()

            # Supabase 업데이트
            supabase.table("video_snapshots")\
                .update({"collected_at_kst": kst_time})\
                .eq("id", snapshot_id)\
                .execute()

            updated_count += 1

        except Exception as e:
            print(f"[❌] ID {snapshot_id} 변환 실패: {e}")

    offset += BATCH_SIZE
    total_batches += 1

print(f"\n✅ 전체 완료: {updated_count}개의 행이 collected_at_kst 컬럼으로 업데이트되었습니다.")
