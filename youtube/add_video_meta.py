# add_video_meta.py

import os
import isodate
from datetime import datetime
from typing import List, Dict
from youtube.api_key import build_youtube_with_fallback


from supabase import create_client, Client

# Supabase 설정
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)