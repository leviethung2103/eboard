from bs4 import BeautifulSoup
import pandas as pd 

def crawl_data(input_file, output_file):
        
    with open(input_file, "r") as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')

    li_elements = soup.select('ul.contents.piechart.small li')

    data1 = []
    data2 = []
    for li in li_elements:
        for item in li.find_all('img'):
            topic_name = item['alt']
            image = item['src']
            data1.append({'topic_name': topic_name, 'image': image})


    for li in li_elements:
        for item in li.find_all("a"):
            if "content" in item['href']:
                topic_name = item.text
                url = "https://www.eboard.jp" + item['href']
                data2.append({'topic_name': topic_name, 'url': url})

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    merged_df  = pd.merge(df1,df2, on = "topic_name", how='left')
    merged_df.to_csv(output_file, index=False, encoding='utf_8_sig')

if __name__ == "__main__":
    input_file = "data/primary_school/eboard_arithmetic.html"
    output_file = "data/primary_school/eboard_arithmetic.csv"
    crawl_data(input_file,output_file)
