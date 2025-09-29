import pandas as pd
import json

# URLからスプレッドシートIDとシートIDを抽出
spreadsheet_id = "1Eo6J_5byaPw8yKT1Vp5UTVyg-MJmyK4JrTouKBRM2PQ"
sheet_id = "336284760"

# CSV形式でダウンロードするためのURL
csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"

# pandasでCSVデータを読み込み
df = pd.read_csv(csv_url, header=1)

# 一列目を削除
df = df.drop(df.columns[0], axis=1)

layer_words_list = []
for col in df.columns:
    layer_words = []
    for val in df[col]:
        if pd.notnull(val):
            layer_words.append(val)

    layer_words_list.append(layer_words)

term_words = layer_words_list[-1]

print(layer_words_list)

data = json.load(open('../settings.json'))

for layer_index, layer_words in enumerate(layer_words_list):
    layer_num = layer_index + 1
    layer = data['selection_list'][layer_index]
    selections = layer['selections']
    
    
    for i in range(len(selections)):
        selection = selections[i]
        pos = layer_words[i*2]
        neg = layer_words[i*2+1]
        selection["positive_label_text"] = pos.upper()
        selection["nagative_label_text"] = neg.upper()
        
        if layer_num >= 3 and layer_num != 5:        
            step = 2 ** (4 - layer_index)

            ii = i * 2
            pos_sub = term_words[step*ii:step*(ii+1)]
            pos_sub = " / ".join([word.lower() for word in pos_sub])
            neg_sub = term_words[step*(ii+1):step*(ii+2)]
            neg_sub = " / ".join([word.lower() for word in neg_sub])
            
            selection["positive_sub_text"] = pos_sub
            selection["negative_sub_text"] = neg_sub

json.dump(data, open("../settings.json", 'w'), indent=2)