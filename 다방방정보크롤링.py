# -*- coding: utf-8 -*-
# HJI
#%%
#필요 라이브러리 import
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
#%%
##새로운 탭으로 주소변환하기
##다방이 새 페이지를 여는 방식으로 탭에서 열기를 택하는데 이는 webdriver에서 페이지가 바뀌었다고 인식하지 못한다
##그래서 페이지가 바뀌었다고 인식하게 해주는 함수
def ChangeAddressToNew():
    last_tab = driver.window_handles[-1]
    driver.switch_to.window(window_name = last_tab)
#%%
#새로운 페이지에서 다시 원래의 검색 탭으로 이동
def GotoOriTab():
    origin_tab = driver.window_handles[0]
    driver.close()
    driver.switch_to.window(window_name=origin_tab)

#%%
#driver초기화
driver = webdriver.Chrome('C:/Users/USER/chromedriver.exe')
driver.implicitly_wait(3)
#다방홈페이지를 띄운다
driver.get('https://www.dabangapp.com/?gclid=Cj0KCQjwqs3rBRCdARIsADe1pfTYYgiN12kTY2htC4w75yhgufFoVGu1BYnUpoOMlFvBDe9pxKHteQMaAqsaEALw_wcB')

# user_input으로 구이름 받기
user_input = input('구명을 입력하세요.')
search_gu = driver.find_element_by_name("keyword")
search_gu.send_keys(user_input+'\n')

#%%
#크롤링할 정보는 크게 월세, 전세로 나뉘어지기 때문에 두개의 DB리스트 생성
MonthDB = []
YearDB = []
#%%
#검색페이지 소스 받기
html = driver.page_source
time.sleep(5)
soup = BeautifulSoup(html,'html.parser')
getul = soup.find('ul',{'class':'styled__Ul-ityzo6-5 fxRDHg'})
#눌러야 하는 버튼의 수를 세기위한 변수 (여기서 버튼의 수는 한페이지에서 볼 수있는 방의 개수와 동일)
ButtonList = getul.find_all('li',{'class':'styled__Li-sc-84urxt-0 hxpbDF'})

#%%
#첫번째 페이지 긁어오기 다방의 경우 첫번째 페이지, 두번째 페이지~마지막 페이지 까지의 구조가 다르다.
#따라서 첫번째 페이지는 따로 크롤링한다.
#매물이 없는 경우
if(ButtonList == None):
    print("매물이 하나도 없습니다")
#매물이 있는 경우 그냥 진행한다
else:
    pass

try:
    #첫번째 방부터 마지막 방까지의 정보를 가지고온다
    for i in range(1,len(ButtonList)+1):
            driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div/div[2]/ul/li[{}]'.format(i)).click()
            ChangeAddressToNew()
            html = driver.page_source
            time.sleep(5)
            soup = BeautifulSoup(html,'html.parser')
            getdiv = soup.find('div',{'class':'styled__Block-sc-123hsgh-0 kZTRnS'})
            RoomData = getdiv.find_all('h1',{'class','styled__Info-cji31o-6 dUuerR'})
            #주소정보 가져오기
            RoomData.append(soup.find('p',{'class','styled__Address-omjh6x-3 hwnvlX'}))
            if RoomData[0].text[0:2] == '월세':
                for j in RoomData:
                    MonthDB.append(j.text)
                MonthDB.append(driver.current_url)
            elif RoomData[0].text[0:2] == '전세':
                for j in RoomData:
                    YearDB.append(j.text)
                YearDB.append(driver.current_url)
            else:
                pass
            GotoOriTab()
except:
    for i in range(1,len(ButtonList)+1):
            driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div/div[2]/ul[2]/li[{}]'.format(i)).click()
            ChangeAddressToNew()
            html = driver.page_source
            time.sleep(5)
            soup = BeautifulSoup(html,'html.parser')
            getdiv = soup.find('div',{'class':'styled__Block-sc-123hsgh-0 kZTRnS'})
            RoomData = getdiv.find_all('h1',{'class','styled__Info-cji31o-6 dUuerR'})
            #주소정보 가져오기
            RoomData.append(soup.find('p',{'class','styled__Address-omjh6x-3 hwnvlX'}))
            if RoomData[0].text[0:2] == '월세':
                for j in RoomData:
                    MonthDB.append(j.text)
                MonthDB.append(driver.current_url)
            elif RoomData[0].text[0:2] == '전세':
                for j in RoomData:
                    YearDB.append(j.text)
                YearDB.append(driver.current_url)
            else:
                pass
            GotoOriTab()
#%%
switch = 1 
#다음 페이지로 넘어간다 
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div/div/button[2]').click()
html2 = driver.page_source
time.sleep(5)

#만약 마지막 페이지라면 버튼이 클릭되지 않는데, 이 때 버튼을 누른 후와 누르기 전의 html코드를 비교하여 
#같다면 버튼이 눌러지지 않는 마지막페이지라는 의미 이므로 반복문에서 나가기위한 switch변수에 1을 더해준다
if html == html2:
    switch += 1
else:
    pass

#두번째 페이지부터 끝까지

while(switch ==1):
    html = driver.page_source
    time.sleep(5)
    soup = BeautifulSoup(html,'html.parser')
    getul = soup.find('ul',{'class':'styled__Ul-ityzo6-5 fxRDHg'})
    #눌러야 하는 버튼의 수를 세기위한 변수
    ButtonList = getul.find_all('li',{'class':'styled__Li-sc-84urxt-0 hxpbDF'})
    print(len(ButtonList))
    #첫번째 페이지 긁는 것과 구조적 동일
    for i in range(1,len(ButtonList)+1):
        driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div/div[2]/ul/li[{}]'.format(i)).click()
        ChangeAddressToNew()
        html = driver.page_source
        time.sleep(5)
        soup = BeautifulSoup(html,'html.parser')
        getdiv = soup.find('div',{'class':'styled__Block-sc-123hsgh-0 kZTRnS'})
        RoomData = getdiv.find_all('h1',{'class','styled__Info-cji31o-6 dUuerR'})
        #주소정보 가져오기
        RoomData.append(soup.find('p',{'class','styled__Address-omjh6x-3 hwnvlX'}))
        
        if RoomData[0].text[0:2] == '월세':
            for j in RoomData:
                MonthDB.append(j.text)
            MonthDB.append(driver.current_url)    
        elif RoomData[0].text[0:2] == '전세':
            for j in RoomData:
                YearDB.append(j.text)
            YearDB.append(driver.current_url)
        else:
            pass
        GotoOriTab()
    html = driver.page_source
    time.sleep(5)
    #다음 페이지로 넘어간다 
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div/div/button[2]').click()
    html2 = driver.page_source
    time.sleep(5)
    #만약 마지막 페이지라면 버튼이 클릭되지 않는데, 이 때 버튼을 누른 후와 누르기 전의 html코드를 비교하여 
    #같다면 버튼이 눌러지지 않는 마지막페이지라는 의미 이므로 반복문에서 나가기위한 switch변수에 1을 더해준다
    if html == html2:
        switch += 10
    else:
        pass
#크롤링이 끝나면 창을 닫아준다.
driver.close()
#%%
#딕셔너리에 넣을 정보를 임시로 담을 변수들
slicelen = 0
temp = []
temp1 = []
월세 = []
보증금 = []
월세방크기 = []
월세생활비 = []
월세주소 = []
월세웹주소 = []
yeartemp = []
전세금 = []
전세방크기 = []
전세생활비 = []
전세주소 = []
전세웹주소 = []
#%%
#딕셔너리에 넣을 정보 정리
#
Many = int(len(MonthDB)/5)
for i in range(int(len(MonthDB)/5)):
    temp = MonthDB[slicelen:slicelen+5]
    temp1 = temp[0][3:].split('/')
    보증금.append(temp1[0])
    월세.append(int(temp1[1]))
    월세방크기.append(temp[1])
    월세생활비.append(temp[2])
    월세주소.append(temp[3])
    월세웹주소.append(temp[4])
    slicelen += 5
    
slicelen = 0
for i in range(int(len(YearDB)/5)):
    yeartemp = YearDB[slicelen:slicelen+5]
    if len(yeartemp[0:4][0][3:]) == 4:
        전세금.append(int(yeartemp[0:4][0][3:]))
    elif len(yeartemp[0:4][0][3:]) == 2:
        전세금.append(int(yeartemp[0:4][0][3:].replace("억","0000")))
    else:
        전세금.append(int(yeartemp[0:4][0][3:].replace("억","0000").split(" ")[0])+int(yeartemp[0:4][0][3:].replace("억","0000").split(" ")[0]))
    전세방크기.append(yeartemp[1])
    전세생활비.append(yeartemp[2])
    전세주소.append(yeartemp[3])
    전세웹주소.append(yeartemp[4])
    slicelen += 5


#%%
#빈딕셔너리 생성
월세방정보 = {'월세':[]}
전세방정보 = {'전세':[]}
#%%
#정보 정리
for i in range(len(월세)):
    월세방정보['월세'].append({'월세':월세[i],'보증금':보증금[i],'방크기':월세방크기[i],'한달생활비':월세생활비[i], '주소':월세주소[i],'웹주소':월세웹주소[i]}) 

for i in range(len(전세금)):
    전세방정보['전세'].append({'전세금':전세금[i],'방크기':전세방크기[i],'한달생활비':전세생활비[i], '주소':전세주소[i], '웹주소':월세웹주소[i]})
#%%

#%%
yeartemp[0:4][0][3:]
#%%
#json으로 만들기
with open('{}월세.json'.format(user_input),'w',encoding = 'UTF-8') as f:
    json.dump(월세방정보,f,indent=4,ensure_ascii=False)
with open('{}전세.json'.format(user_input),'w',encoding = 'UTF-8') as f:
    json.dump(전세방정보,f,indent=4,ensure_ascii=False)

#%%


