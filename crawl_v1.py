
import requests
from bs4 import BeautifulSoup
import re

#1 link
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
link_base = "https://lbaronline.com/buyers-sellers/find-a-realtor/"

#2. lay du lieu
r= requests.get(link_base, headers= headers)
soup = BeautifulSoup(r.text, "html.parser")
element_father = soup.select_one("div.fl-post-feed")
elements = element_father.children

#3. file
f= open('../data/dataEx.csv','a')

i = 0
for e in elements:
    if str(type(e)) != "<class 'bs4.element.NavigableString'>":
        row = e.find_all("div", class_="row")
        tag_name = row[0].select("div:nth-child(1) > h2 > a")
        link2 = str(tag_name[0]['href'])
        # print('link: '+ link2)
        r2 = requests.get(link2, headers= headers)
        soup2 = BeautifulSoup(r2.text, "html.parser")
        str_data = ""
        name_tag = soup2.select("#fl-main-content > div > div.fl-row.fl-row-full-width.fl-row-bg-none.fl-node-5e8e0a8d8166e > div > div > div > div.fl-col.fl-node-5e8e0a8d843d4.fl-col-has-cols > div > div.fl-module.fl-module-heading.fl-node-5e8e0ac33bbe5 > div > h1 > span")
        str_data = str_data + str(name_tag[0].get_text().strip())+','
        tag_data1 = soup2.find_all('div',class_ = "fl-html")
        for data in tag_data1:
            for child in data.children:
                if str(type(child)) != "<class 'bs4.element.NavigableString'>":
                    if child.name == 'a':
                        if child.get_text().strip() == 'Email':
                            mail_str = child['href'].strip()
                            m_index = mail_str.index(':')
                            # mail_str = str(mail_str[m_index+1:])
                            str_data = str_data + mail_str[m_index+1:] + ','
                        elif re.match("[0-9]{2,4}-[0-9]{2,4}-[0-9]{2,4}",child.get_text().strip()):
                            str_data =str_data +  child.get_text().strip()+'\n'
                        else:
                            str_data =str_data +  child.string.strip() + ','
                            str_data =str_data +  child['href'].strip()+ ','
                else:
                    if child.string .strip() != "":
                        str_data = str_data +  child.string .strip() + ','
        # print(str_data)
        f.write(str_data)
        i += 1
        print(i)     
f.close()