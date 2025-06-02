import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import FuncFormatter
import os

font_path = './static/NanumGothic-Regular.ttf'
if not os.path.exists(font_path):
    raise FileNotFoundError(f"{font_path} 폰트 파일이 없습니다. 경로를 확인하세요.")

font_prop = fm.FontProperties(fname=font_path)
fm.fontManager.addfont(font_path)
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('./data/processed_data.csv', parse_dates=['timestamp'])

channels = df['channel_handle'].unique()

for channel in channels:
    df_channel = df[df['channel_handle'] == channel].sort_values('timestamp')
    videos = df_channel['video_id'].unique()[:10]

    fig, ax1 = plt.subplots(figsize=(14, 8))

    for vid in videos:
        df_vid = df_channel[df_channel['video_id'] == vid]
        ax1.plot(df_vid['timestamp'], df_vid['view_count'], label=f'Video {vid}')

    ax1.set_xlabel('시간', fontproperties=font_prop)
    ax1.set_ylabel('조회수', fontproperties=font_prop)
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    sub_df = df_channel[['timestamp', 'subscriber_count']].drop_duplicates('timestamp')
    ax2.plot(sub_df['timestamp'], sub_df['subscriber_count'], 'k--', label='구독자수')
    ax2.set_ylabel('구독자수', fontproperties=font_prop)

    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

    plt.title(f'채널: {channel} 조회수 및 구독자수 추이', fontproperties=font_prop)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 범례 합치기
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., prop=font_prop)

    # 파일 이름에 채널명 포함 (특수문자 제거해서 파일명으로 적합하게 변환)
    safe_channel = channel.replace('@', '').replace(' ', '_')
    filename = f'./data/{safe_channel}_view_subscriber_trend.png'

    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
