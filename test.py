# import requests
# from bs4 import BeautifulSoup
# first_page_to_parce=13843
# i=0
# url = 'http://udaff.com/view_listen/photo/page'+str(first_page_to_parce+i)+'.html'
# soup = BeautifulSoup(requests.get(url).text, 'html.parser')
# div_tag_pic="http://udaff.com"+soup.find('div', class_="pic-cont").find('img').get('src')
# print(div_tag_pic)