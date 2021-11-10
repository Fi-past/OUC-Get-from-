from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import json
import time


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
    driver.find_element_by_xpath(str).click()
    time.sleep(2)


def GetDatas(URL,counts):
    titleSets=set()
    set_counts=0

    patient,lastNums=0,0

    with open('./res/topicMessage.txt',mode='w',encoding='utf-8') as f_result:
        driver.get(URL)
        with open('./Cookie/bb_mg.json', encoding='UTF-8') as f:
            bbJson = json.load(f)
            for j in bbJson:
                driver.add_cookie(j)

        for i in range(counts):
            driver.get(URL)
            time.sleep(2)
            clickAndSleep(driver,'//*[@id="bottom_submitButtonRow"]/input[2]')
            clickAndSleep(driver,'//*[@id="containerdiv"]/div[2]/a[3]')
            clickAndSleep(driver,'//*[@id="bottom_submitButtonRow"]/input[2]')

            dialog_box = driver.switch_to_alert()
            dialog_box.accept()   #接受弹窗

            clickAndSleep(driver,'//*[@id="containerdiv"]/p[2]/a')

            time.sleep(3)
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

                answer_str=''
                for a in an_list:
                    answer_str+=a+'\n'
                message=str(message)+'\n'

                # print(message)
                # print(answer_str)
                # print('-'*30)
                if message not in titleSets:
                    titleSets.add(message)
                    f_result.write(message)
                    f_result.write(answer_str)
                    f_result.write('-'*30)
                    f_result.write('\n')
            set_counts=len(titleSets)
            print(f'第{i+1}次爬取获得题目{set_counts}个')

            if set_counts-lastNums==0:
                patient+=1
                if patient>=5:
                    break
            else:
                patient=0
            
            lastNums=set_counts




# URL_cookie='https://wlkc.ouc.edu.cn/webapps/assessment/take/launchAssessment.jsp?course_id=_13492_1&content_id=_626890_1&mode=view'
# GetCookie(URL_cookie)
URL_data='https://wlkc.ouc.edu.cn/webapps/assessment/take/launchAssessment.jsp?course_id=_13492_1&content_id=_626890_1&mode=view'
GetDatas(URL_data,1000)


# input()