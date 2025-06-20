with open("data/test_data.csv", encoding="utf-8-sig") as f:
    for i, line in enumerate(f):
        print(line)
        if i == 5: break