import requests
from bs4 import BeautifulSoup
udaff_parser_all=[]
udaff_parser=dict()
number_of_pages=int(input('Сколько страниц парсить: '))
first_page_to_parce = int(input('С какой страницы парсить (там около 15 000 страниц): '))

for i in range(number_of_pages):
    udaff_parser=dict()
    url = 'http://udaff.com/view_listen/photo/page'+str(first_page_to_parce+i)+'.html'
    udaff_parser['url']=url
    udaff_parser['number']=i
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    div_tag_comments=soup.find('div', class_="comments")
    comment_number=1
    udaff_comment_tmp=[]
    print(url)
    while not div_tag_comments.find('div', class_="item N"+str(comment_number)) is None:
        udaff_comment={}
        udaff_comment['comment_number']=comment_number
        item_tag = div_tag_comments.find('div', class_="item N"+str(comment_number))
        udaff_comment['comment']=item_tag.find('p', class_="c_msg_text").text
        author=item_tag.find('p', class_="author")
        author_name=author.find('a')
        try:
            udaff_comment['author']=author_name.text
        except:
            udaff_comment['author']=author.text
        udaff_comment_tmp.append(udaff_comment)
        # print(udaff_comment)
        comment_number=comment_number+1
    print(f'На странице было {comment_number} комментариев')
    udaff_parser['comments'] = udaff_comment_tmp
    udaff_parser_all.append(udaff_parser)
# print(udaff_parser_all)

import json
with open(f'Udaff_from_{first_page_to_parce}_to_{first_page_to_parce+number_of_pages-1}.json', 'w') as f:
    json.dump({'udaff':udaff_parser_all}, f)