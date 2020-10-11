from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
# Create your views here.
def get_html(city):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    print(session)
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city=city.replace(' ', '+')
    html_content=session.get(f'https://www.google.com/search?q=weather+in+{city}').text
    return html_content
def home(request):
    flag=False
    m=False
    if 'city' in request.GET:
        city=request.GET.get('city')
        htm_content=get_html(city)
        soup=BeautifulSoup(htm_content,'html.parser')
        if (soup.find('span',attrs={'id':'wob_tm'}))!=None and (soup.find('div',attrs={'id':'wob_dcp'}))!=None and (soup.find('div',attrs={'id':'wob_loc'}))!=None and (soup.find('div',attrs={'id':'wob_dts'}))!=None:
            reg =soup.find('div',attrs={'id':'wob_loc'}).text
        
            datetime =soup.find('div',attrs={'id':'wob_dts'}).text
            climate =soup.find('div',attrs={'id':'wob_dcp'}).text
            #img =soup.find('div',attrs={'id':'wob_tci'}).text
            temp =soup.find('span',attrs={'id':'wob_tm'}).text
            print(reg,datetime,climate,temp)
            pass
            flag=True
            return render(request,'todayweather/homepage.html',{'temp':temp,'reg':reg,'climate':climate,'datetime':datetime,'f':flag})
        else:
            m=True
            messages.warning(request, 'The Server is busy please try after sometime.')
            return render(request,'todayweather/homepage.html',{'m':m})
    return render(request,'todayweather/homepage.html',{'f':flag})