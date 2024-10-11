import pandas as pd
import matplotlib.pyplot as plt
import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

first_json = load_json('data/mayo_clinic/mayo_diseases.json')
second_json = load_json('data/wikipedia/wikipedia_diseases.json')
merged_json = {**first_json, **second_json}
save_json('merged.json', merged_json)

merged_df = pd.DataFrame.from_dict(merged_json, orient='index')

# ver percentagem de entradas vazias em cada coluna (não vai aparecer no pie chart o "overview" pq a percentagem é 0%)
# missing_percentages = merged_df.isnull().mean() * 100
# missing_percentages = missing_percentages[missing_percentages > 0]
#
# plt.figure(figsize=(8, 8))
# plt.pie(
#     missing_percentages, 
#     labels=missing_percentages.index, 
#     autopct='%1.1f%%', 
#     startangle=90
# )
# plt.title("Percentage of empty values ​​per column",pad=50)
# plt.show()


# ver percentagem do tamanho médio das entradas em cada coluna
def mean_string_length(column):
    strings = column.dropna().astype(str)
    string_lengths = strings.apply(len)
    return string_lengths.mean()

mean_lengths = merged_df.apply(mean_string_length)
mean_lengths = mean_lengths.dropna()

plt.figure(figsize=(8, 8))
plt.pie(mean_lengths, labels=mean_lengths.index, autopct='%1.1f%%', startangle=90)
plt.title("Average String Length per Column", pad=50)
plt.show()