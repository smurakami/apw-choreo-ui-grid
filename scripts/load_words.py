import pandas as pd
import json

# URLからスプレッドシートIDとシートIDを抽出
spreadsheet_id = "1Eo6J_5byaPw8yKT1Vp5UTVyg-MJmyK4JrTouKBRM2PQ"
sheet_id = "1991248054"

# CSV形式でダウンロードするためのURL
csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"

# pandasでCSVデータを読み込み
df = pd.read_csv(csv_url, header = None)

word_list = [list(col) for col in df.to_numpy()]


data = json.load(open('../settings.json'))
data['word_list'] = word_list

json.dump(data, open("../settings.json", 'w'), indent=2)