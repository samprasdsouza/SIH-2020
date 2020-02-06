from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import ParseData

import threading
from bs4 import BeautifulSoup
from datetime import date,timedelta,datetime
import urllib.request
import urllib.parse
import ast
import json
#import requests

#import sys
#import pymysql
import requests
#import urllib.request as request
# Create your views here.

keyword_to_be_searched ="pornography"
def landing(request):
    print("hello world")
    # .objects.all().delete()
    return render(request,'base/index.html')

def keyword(request):
    print("Inside ")
    ParseData.objects.all().delete()
    global keyword_to_be_searched
    keyword_to_be_searched = request.POST['keyword']
    if keyword_to_be_searched=="":
        keyword_to_be_searched="pornography"
    #conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='test1')
    #cur = conn.cursor()
    # creating thread 
    t1 = threading.Thread(target=toi, name='t1')
    t2 = threading.Thread(target=bing, name='t2')
    t3 = threading.Thread(target=reuter, name='t3')
    t4 = threading.Thread(target=google, name='t4')
    t5 = threading.Thread(target=facebook, name='t5')

    # starting thread 1 
    t1.start()
    # starting thread 2 
    t2.start()

    t3.start()
    
    t4.start()
    

    # wait until thread 1 is completely executed 
    t1.join()
    # wait until thread 2 is completely executed 
    t2.join()
    t3.join()
    t4.join()
    t5.start()
    t5.join()
    # both threads completely executed 
    print("Done!")

    d={'else':keyword_to_be_searched}
    return render(request,'base/index.html',d)
    
def filter(request):
    print("Inside filter")
    #getting the data from the url 
    #location = request.POST['Location']
    k = request.POST.get('passValue1',False)
    # k2 = request.POST.get('passValue2',False)
    location = request.POST.get('Location',False)
    NewsArticle  = request.POST.get('newsArticle',False)
    #newArticle = request.POST['newsArticle']
    # if 'socialMedia' in request.POST:
    # SocialMedia = request.POST['socialMedia']
    # else:
    # SocialMedia = False
    SocialMedia = request.POST.get('socialMedia', False)
    # SocialMedia = request.POST['socialMedia']
    CaseStudy = request.POST.get('caseStudy', False)
    Organisation = request.POST.get('organisation', False)

    DateFrom = request.POST.get('Date', False)
    DateTo = request.POST.get('DateTo', False)
    # Date2 = request.POST.get('Date',False)
    ##
    #CaseStudy = request.POST['caseStudy']
    #Organisation = request.POST['organisation']
    #DateFrom = request.POST['DateFrom']
    #DateTo = request.POST['DateTo']   
    print(k)
    # print(k2)
    print(location)
    print(NewsArticle)
    print(SocialMedia)
    print(CaseStudy)
    print(Organisation)
    print("date from:",DateFrom)
    print("date to:",DateTo) 
    # print("Date2:",Date2
    # res = ParseData.objects.filter(date_gt)
    if len(str(DateFrom)) > 0 and (DateFrom != False):
        print("yes ")
        # DateFrom = str(DateFrom)
        # DateFrom+="-01"
        # print(DateFrom)
        # find=ParseData.objects.filter(date__gt=DateFrom)
        # d= {'find':find}
        # print(find)
    d = {'else':k,'location':location,'NewsArticle':NewsArticle,'SocialMedia':SocialMedia,'CaseStudy':CaseStudy,'Organisation':Organisation,'DateForm':DateFrom,'DateTo':DateTo}
    
    return render(request,'base/index.html',d)




# inp='child abuse'
def toi():
    global keyword_to_be_searched
    inp= keyword_to_be_searched
    print(keyword_to_be_searched,inp)
    inp=inp.replace(' ','-')
    base_url='https://timesofindia.indiatimes.com/topic/'+inp
    r=requests.get(base_url)
    soup=BeautifulSoup(r.content,'lxml')
    #main=soup.find('div',class_='main-container')
    main=soup.find(id='c_01')

    m=main.find('div',class_='tab_content')
    article=m.findAll('li',class_='article')
    for i in article:
        c=i.find('div',class_='content')
        link=c.find('a').get('href')
        link='https://timesofindia.indiatimes.com'+link
        link=link.strip()
        title=c.find('span',class_='title').text
        date=c.find('span',class_='meta').text
        desc=c.find('p').text
        desc=title+' '+desc
        source = "News"
        date=datetime.strptime(date,'%d %b %Y')
        print(link)
        print(desc)
        print(date)
        print(source)
        ParseData.objects.create(href=link,source=source,description=desc,date=date)
        print('---------------------------------------------------------------------------------')




def bing():
        global keyword_to_be_searched
        inp=keyword_to_be_searched
        print(keyword_to_be_searched,inp)
        inp=inp.replace(' ','+')
        base_url='https://www.bing.com/news/search?q='+inp+'&FORM=HDRSC6'
        r=requests.get(base_url)
        soup=BeautifulSoup(r.content,'lxml')
        #main=soup.find('div',class_='main-container')
        main=soup.find(id='algocore')
        url=main.findAll('div',class_='news-card newsitem cardcommon')#.get('url')
        #snip=url.find('div',class_='snippet').get('title')
        #print(snip)
        for i in url:
            href=i.get('url')
            
            t=i.find('div',class_='t_t')
            title=t.find('a').text
            #print(title)
            snip=i.find('div',class_='snippet').get('title')
            #print(snip)
            s=i.find('div',class_='source')
            src=s.find('a').get('aria-label')
            src=src+" "+title+" "+snip
            
            day=s.find_all('span')[2].get('aria-label')
            if day[1]=='hour' or day[1]=='hours' or day[1]=='minute' or day[1]=='minutes' or day[1]=='second' or day[1]=='seconds':
                today = date.today()
   
            else:
                p=int(day[0])
                today = date.today()-timedelta(p)
    
            d1 = today
            source = "News"
            print(href)
            print(src)
            print(d1)
            print(source)
            ParseData.objects.create(href=href,source=source,description=src,date=d1)
            print('---------------------------------')


def reuter():
    global keyword_to_be_searched
    inp=keyword_to_be_searched
    print(keyword_to_be_searched,inp)
    inp=inp.replace(' ','+')
    base_url='https://in.reuters.com/assets/searchArticleLoadMoreJson?blob='+inp+'&bigOrSmall=big&articleWithBlog=true&sortBy=&dateRange=&numResultsToShow=100&pn=1&callback=addMoreNewsResults'
    r=requests.get(base_url)
    soup=BeautifulSoup(r.content,'lxml')
    a=soup.find('body')
    p=a.find('p').text
    try:
        use=p.split('news')[1][1:]
        use=use.replace('\n','')
        use=use.replace('\r','').strip()
        use=use[1:].strip()
        user=use.split('{')[1:]
    except:
        pass
    l=[]
    #print(user)
    for j in user:
        #print(j)
        #print("--------------------------")
        try:
            a=str(j).strip()
            a=a.split(',')
        except:
            continue
        
        
        d={}
        c=0
        flag=False
        for i in a:
       # print("i",i)
            try:
                #print(i)
                if ':' not in i:
                    continue
                keyvalue=i.split(':')
                #print(keyvalue)
                key,value=keyvalue[0].strip(),keyvalue[1].strip()
                if c==0:
                    value='https://in.reuters.com/article/id'+value[1:-1]
                if flag:
                    print("Raj tenzu")
                    try:
                        
                        dt=d['date']+' '+key[:4]
                        dt=dt.strip()
                        dt=dt[1:]
                        
                        datetime_object = datetime.strptime(dt, '%B %d %Y')
                        d['date']=datetime_object
                        
                        print(datetime_object)
                    except:
                        continue
                    break
                c+=1
                d[key]=value
                if key=="date":
                    flag=True
            except:
                continue
        try:
            source ="News" 
            print(d['id'])
            print(d['headline'])
            print(d['date'])
            print(source)
            ParseData.objects.create(href=d['id'],source=source,description=d['headline'],date=d['date'])
            print('--------------------------------------------------')
            l.append(d)
        except:
            continue
    #print("reuters=",l)
    
    
def google():
    global keyword_to_be_searched
    inp=keyword_to_be_searched+' case study'
    print(keyword_to_be_searched,inp)
    inp=inp.replace(' ','+')
    url= urllib.parse.quote('https://www.google.com/search?q='+inp)
    handler = urllib.request.urlopen('https://api.proxycrawl.com/scraper?token=kyRSsw-VmmO267ke4AMkHw&url=' + url)
    firfir=handler.read().decode('utf-8',errors='ignore')
    useful=json.loads(firfir)
    l=[]
    #mon=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    for i in useful['body']['searchResults']:
        d={}
        d['id']=i['url']
        #d['title']=i['title']
        des=i['description']


        if des[13] is '-':
            dat=des.split('-')
            if ',' in dat[0]:
                ddat=dat[0].replace(',','').strip()
                d['description']=dat[1]+i['title']
            else:
                ddat='Jan 10 2020'
                d['description']=dat[0]+dat[1]+i['title']
            #print(ddat)
            datetime_object = datetime.strptime(ddat, '%b %d %Y')
            d['date']= datetime_object
            d['description']=dat[1]+i['title']
        else:
            d['description']=des+i['title']
            d['date']=datetime.today()
        l.append(d)
        source = "case study"
        print(d['id'])
        print(d['date'])
        print(d['description'])
        print(source)
        ParseData.objects.create(href=d['id'],source=source,description=d['description'],date=d['date'])
        print('-----------------------------------------------------------------')

def facebook():
    global keyword_to_be_searched
    inp=keyword_to_be_searched+' facebook'
    print(keyword_to_be_searched,inp)
    inp=inp.replace(' ','+')
    print(inp)
    url= urllib.parse.quote('https://www.google.com/search?q='+inp)
    handler = urllib.request.urlopen('https://api.proxycrawl.com/scraper?token=kyRSsw-VmmO267ke4AMkHw&url=' + url)
    firfir=handler.read().decode('utf-8',errors='ignore')
    useful=json.loads(firfir)
    l=[]
    #mon=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    for i in useful['body']['searchResults']:
        d={}
        d['id']=i['url']
        #d['title']=i['title']
        des=i['description']
        if '-' in des:
            dat=des.split('-')
            print("dat",dat)
            #ddat=dat[0].replace(',','').strip()
            if ',' in dat[0]:
                ddat=dat[0].replace(',','').strip()
                d['description']=dat[1]+i['title']
            else:
                ddat='Jan 10 2020'
                d['description']=dat[0]+dat[1]+i['title']
            #print(ddat)
            datetime_object = datetime.strptime(ddat, '%b %d %Y')
            d['date']= datetime_object
            d['description']=dat[1]+i['title']
        else:
            d['description']=des+i['title']
            d['date']=datetime.today()
        l.append(d)
        source = "social media"
        print(d['id'])
        print(d['date'])
        print(d['description'])
        print(source)
        ParseData.objects.create(href=d['id'],source=source,description=d['description'],date=d['date'])
        print('-----------------------------------------------------------------')





