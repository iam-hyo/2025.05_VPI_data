import pandas as pd

data = [
    {"channel_handle": "@ChimChakMan_Official", "channel_id": "UCUj6rrhMTR9pipbAWBAMvUQ"},
    {"channel_handle": "@GABEEGIRL", "channel_id": "UCoC-ZGuPCvJJrbcz9eMW8zw"},
    {"channel_handle": "@bokyemtv", "channel_id": "UCu9BCtGIEr73LXZsKmoujKw"},
    {"channel_handle": "@미미미누", "channel_id": "UCyNHdF4hMxHUFSsPbY24p6A"},
    {"channel_handle": "@15ya_egg", "channel_id": "UCQ2O-iftmnlfrBuNsUUTofQ"},
    {"channel_handle": "@LCK", "channel_id": "UCw1DsweY9b2AKGjV4kGJP1A"},
    {"channel_handle": "@GH.S", "channel_id": "UCfm0AXrDy-35i8BJc3WUpUg"},
    {"channel_handle": "@두치와뿌꾸", "channel_id": "UCl402YYy7RcH7PBI3npmGPQ"},
    {"channel_handle": "@pray94", "channel_id": "UCSzHok6X5qXEO7cjvVnE62g"},
    {"channel_handle": "@군림보", "channel_id": "UCN5oT4zGJX-_H6pE5isAEeg"},
    {"channel_handle": "@이과형", "channel_id": "UCj-MI9DaXgAz412O9ybQ9WA"},
    {"channel_handle": "@scoopknowledge", "channel_id": "UCwajXTjsIZsXrZkfVk_uY9w"},
    {"channel_handle": "@codingapple", "channel_id": "UCSLrpBAzr-ROVGHQ5EmxnUg"},
    {"channel_handle": "@ebs.science - 사이언스", "channel_id": "UCiFYUP4_TI70yCkkVJAlxoA"},
    {"channel_handle": "@YTNSC", "channel_id": "UCZdBJIbJz0P9xyFipgOj1fA"},
    {"channel_handle": "@miso_ara", "channel_id": "UCuKbAWuSG9F_UEF2Xngbq0A"},
    {"channel_handle": "@Bodeumofficial", "channel_id": "UCee1MvXr6E8qC_d2WEYTU5g"},
    {"channel_handle": "@oneroomcat", "channel_id": "UC0zVOxvxiFlvelR59C_sUzQ"},
    {"channel_handle": "@meow_dad", "channel_id": "UC5AAf4_zZxk-mCl46TogZQQ"},
    {"channel_handle": "@timon_sns", "channel_id": "UCVvPi6vztLioOiuEg5JYavw"}
]

df = pd.DataFrame(data)
df.to_json('channelIds_HJ.json', orient='records', force_ascii=False, indent=4)
print("channelIds_HJ.json 파일 생성 완료!")
