import pandas as pd
import json

# URLからスプレッドシートIDとシートIDを抽出
spreadsheet_id = "1Eo6J_5byaPw8yKT1Vp5UTVyg-MJmyK4JrTouKBRM2PQ"
sheet_id = "1991248054"

# CSV形式でダウンロードするためのURL
csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"

# pandasでCSVデータを読み込み
df = pd.read_csv(csv_url, header = None)

word_list = df.to_numpy()
word_list = [list(["" if pd.isnull(x) else x for x in col]) for col in word_list]
print(word_list)


data = json.load(open('../settings.json'))
data['word_list'] = word_list

json.dump(data, open("../settings.json", 'w'), indent=2)