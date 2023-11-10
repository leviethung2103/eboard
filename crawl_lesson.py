from bs4 import BeautifulSoup
import pandas as pd 
import requests
import json
import time 

def crawl_data(input_file, output_file):
        
    with open(input_file, "r") as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')

    li_elements = soup.select('ul.contents.piechart.small li')

    data1 = []
    data2 = []
    for li in li_elements:
        for item in li.find_all('img'):
            lesson_name = item['alt']
            image = item['src']
            data1.append({'lesson_name': lesson_name, 'image': image})


    for li in li_elements:
        for item in li.find_all("a"):
            if "content" in item['href']:
                lesson_name = item.text
                url = "https://www.eboard.jp" + item['href']
                data2.append({'lesson_name': lesson_name, 'url': url})

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    merged_df  = pd.merge(df1,df2, on = "lesson_name", how='left')
    merged_df.to_csv(output_file, index=False)

def crawl_content(url):
    response = requests.get(url)
    html = response.text
    
    soup = BeautifulSoup(html, 'html.parser')

    contents = [element.text.strip() for element in soup.find_all('li', class_='video assigned') + soup.find_all('li', class_='video')]

    contents = list(set(contents))
    sorted_contents = sorted(contents, key=lambda x: x[0])

    return sorted_contents

if __name__ == "__main__":
    df = pd.read_csv("data/primary_school/eboard_arithmetic.csv")
    data = {}
    for index, row in df.iterrows():
        url = row.url
        lesson_name = row.lesson_name
        contents = crawl_content(url=url)
        data[lesson_name] = contents
        print("Crawled: ", url)
        time.sleep(1)
    
    with open("data/primary_school/eboard_arithmetic_contents.json", 'w', encoding='utf-8') as file:
        json.dump(data,file, ensure_ascii=False)
