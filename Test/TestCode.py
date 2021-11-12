from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import json
import time


driver = Chrome('../chromedriver_win32/chromedriver.exe')
driver.maximize_window()


def clickAndSleep(driver,str):
    driver.find_element_by_xpath(str).click()
    time.sleep(2)


def getAnswer(URL,counts,re_MessagesList,re_AnswersList):
    titleSets=set()
    set_counts=0
    patient,lastNums=0,0

    MessagesListReal=[]
    AnswersListReal=[]

    with open('./TestMessage.txt',mode='w',encoding='utf-8') as f_result:
        driver.get(URL)
        time.sleep(3)
        # //*[@id="dataCollectionContainer"]
        li_list=driver.find_elements_by_xpath('//*[@id="content_listContainer"]/li')

        for li in li_list:
            message = li.find_element_by_xpath('./div[3]/table/tbody/tr[2]/td[2]/div').text
            answers = li.find_elements_by_xpath('./div[3]/table/tbody/tr[3]/td/table/tbody/tr')
            an_list=[]
            try:
                for an in answers:
                    t=an.find_element_by_xpath('./td[2]/div/span[3]/div/label').text
                    an_list.append(str(t))
            except:
                t=an.find_element_by_xpath('./td[2]/div/span[2]').text
                an_list.append(str(t))

            answer_str=an_list

            MessagesListReal.append(message)
            AnswersListReal.append(answer_str)

        for i in range(len(re_AnswersList)):
            for j in range(len(re_AnswersList[i])):
                if re_AnswersList[i][j] in AnswersListReal[i]:
                    re_AnswersList[i][j]=re_AnswersList[i][j]+'-'*10
        
        for mes,ans in zip(re_MessagesList,re_AnswersList):
            ans='\n'.join(ans)
            print(mes)
            print(ans)


def getQuestion(URL,counts):
    titleSets=set()
    set_counts=0
    patient,lastNums=0,0

    re_MessagesList=[]
    re_AnswersList=[]

    driver.get(URL)

    time.sleep(3)
    div_list=driver.find_elements_by_xpath('//*[@id="dataCollectionContainer"]/div[@class="takeQuestionDiv "]')

    for div in div_list:
        message = div.find_element_by_xpath('./div/ol/li/div/fieldset/legend/div').text
        answers = div.find_elements_by_xpath('./div/ol/li/div/fieldset/table/tbody/tr')
        an_list=[]

        for an in answers:
            t=an.find_element_by_xpath('./td[3]/div/label').text
            an_list.append(str(t))
        if len(an_list)==0:
            answers = div.find_elements_by_xpath('./div/ol/li/div/fieldset/p')
            for an in answers:
                t=an.find_element_by_xpath('./label').text
                an_list.append(str(t))

        answer_str=an_list

        re_MessagesList.append(message)
        re_AnswersList.append(answer_str)

    return re_MessagesList,re_AnswersList


URL_data='file:///F:/Desktop/All/language/VSCODEWORKSPACE/Python/%E7%88%AC%E8%99%AB/smallProject/%E6%AF%9B%E6%A6%82/Test/Source/question.html'
re_MessagesList,re_AnswersList=getQuestion(URL_data,1000)

URL_data='file:///F:/Desktop/All/language/VSCODEWORKSPACE/Python/%E7%88%AC%E8%99%AB/smallProject/%E6%AF%9B%E6%A6%82/Test/Source/answer.html'
getAnswer(URL_data,1000,re_MessagesList,re_AnswersList)

# input()