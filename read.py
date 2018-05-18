import csv
with open('./data/navernews_data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['title'])
        print(row['content'])