from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import json
import time
import collections
import re

driver = Chrome('./chromedriver_win32/chromedriver.exe')
driver.maximize_window()


# 截取Cookie数据
def GetCookie(URL):
    driver.get(URL)
    input('If you success login, print Yes:')
    # 获取cookie列表
    cookie_list = driver.get_cookies()
    jsonCookies = json.dumps(cookie_list) 
    with open('./Cookie/bb_mg.json', 'w') as fileObject:
        fileObject.write(jsonCookies) 

def clickAndSleep(driver,str):
    time.sleep(0.8)
    driver.find_element_by_xpath(str).click()
    time.sleep(0.3)


def getQuestion(URL,counts,driver):
    titleSets=set()
    set_counts=0
    patient,lastNums=0,0

    re_MessagesList=[]
    re_AnswersList=[]

    time.sleep(1.5)
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


def GetDatas(URL,counts):
    time_start=time.time()
    titleSets=set()
    set_counts=0

    patient,lastNums=0,0
    # 默认字典，作为分类用
    classify_dict=collections.defaultdict(list)


    with open('./res/topicMessage.txt',mode='w',encoding='utf-8') as f_result:
        driver.get(URL)
        with open('./Cookie/bb_mg.json', encoding='UTF-8') as f:
            bbJson = json.load(f)
            for j in bbJson:
                driver.add_cookie(j)

        driver.get(URL)

        for iterator in range(counts):
            MessagesListReal=[]
            AnswersListReal=[]

            driver.get(URL)
            time.sleep(1)
            # clickAndSleep(driver,'//*[@id="bottom_submitButtonRow"]/input[2]')
            # //*[@id="bottom_submitButtonRow"]/input[2]
            # 处理第二次爬取的问题
            clickAndSleep(driver,'//*[@id="containerdiv"]/div[2]/a[3]')
            # # //*[@id="containerdiv"]/div[2]/a[3] 开始新的提交

            re_MessagesList,re_AnswersList=getQuestion(URL,1000,driver)


            clickAndSleep(driver,'//*[@id="bottom_submitButtonRow"]/input[2]')

            dialog_box = driver.switch_to_alert()
            dialog_box.accept()   #接受弹窗

            clickAndSleep(driver,'//*[@id="containerdiv"]/p[2]/a')

            time.sleep(1)
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
            
            # 【第十章】
            
            # if message not in titleSets:
            for mes,ans in zip(re_MessagesList,re_AnswersList):
                if mes not in titleSets:
                    titleSets.add(mes)
                    ans='\n'.join(ans)

                    chapter=re.match('【.*】',mes)
                    chapter=chapter.group(0)

                    one_page_strs=''

                    one_page_strs+=mes+'\n'
                    one_page_strs+=ans+'\n\n'
                    one_page_strs+='~'*50+'\n\n'
                    # f_result.write(mes)
                    # f_result.write('\n')
                    # f_result.write(ans)
                    # f_result.write('\n\n')
                    # f_result.write('~'*50)
                    # f_result.write('\n\n')

                    classify_dict[chapter].append(one_page_strs)

            set_counts=len(titleSets)
            print(f'第{iterator+1}次爬取获得题目{set_counts}个')
            time_end=time.time()
            print(f'总用时{time_end-time_start}s')

            if set_counts-lastNums==0:
                patient+=1
                if patient>=30:
                    break
            else:
                patient=0
            
            lastNums=set_counts
        for k,values in classify_dict.items():
            f_result.write('\n'+'#'*50+'\n')
            f_result.write(k+'\n')
            f_result.write('#'*50+'\n'+'\n')
            for v in values:
                f_result.write(v)




URL='https://wlkc.ouc.edu.cn/webapps/assessment/take/launch.jsp?course_assessment_id=_30547_1&course_id=_13492_1&content_id=_641342_1&step=null'
# GetCookie(URL)
GetDatas(URL,1000)


# input()