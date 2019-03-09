import urllib
import docx
import re
import datetime
from bs4 import BeautifulSoup

list = ['/ta/review-frontend', '/ta/review-java', '/ta/review-network', '/ta/front-end-interview', '/ta/nine-chapter']
titles = ['前端面试常考HTML+CSS', 'JAVA面试常考知识点', '计算机网络面试常考点', 'JS面试经典题目合集', 'BAT经典面试题汇总']
url = 'https://www.nowcoder.com'

def parserHtml(soup, url1,index):
    print(titles[index])
    file = docx.Document()
    tlist = soup.findAll('table')[0]
    i=0
    pul=soup.select('.pagination ul');
    if(len(pul)>0):
        pagetotal = int(pul[0]['data-total'])
        for pagenow in range(1, pagetotal):
            for tr in tlist.tbody.findAll('tr'):
                if (pagenow != 1):
                    soup = __crawHtml__(url1 + '?query=&asc=true&order=&page=' + str(pagenow))
                o = tr.select('td:nth-of-type(2)')
                if (len(o) > 0):
                    tag = o[0].find('a')
                    i+=1
                    href=tag['href']
                    soup1 = __crawHtml__(url + href)
                    file.add_paragraph(str(i) + '.' + soup1.select('.final-question')[0].text.replace('\n', ''))
                    print(str(i) + '.' + tag.text)
                    answers = soup1.select('.design-answer-box')[0]
                    for txt in answers.select('p'):
                        line = re.sub('<[^<]+?>', '', txt.text).replace('\n', '').strip()
                        file.add_paragraph(line)
                        print(line)
    file.save("D:\\temp\\"+titles[index]+".docx")


def __crawHtml__(url0):
    res = urllib.request.urlopen(url0)
    html = res.read().decode('utf-8')
    return BeautifulSoup(html, 'html.parser')


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    for index in range(len(list)):
        url0 = url + list[index]
        soup0 = __crawHtml__(url0)
        parserHtml(soup0, url0,index)
    endtime = datetime.datetime.now()
    print ('执行结束，共计'+str((endtime - starttime).seconds)+'s')
