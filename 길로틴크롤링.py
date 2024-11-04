import time
import winreg
from winreg import *

from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import os
import datetime
import shutil
import traceback



findRange = range(0,1000)
oneDelay = 0.7

ID = ""
PASSWORD = ""


days = [(datetime.datetime.today() - datetime.timedelta(minutes=10)).strftime("%y%m%d"),(datetime.datetime.today() - datetime.timedelta(days=1) - datetime.timedelta(minutes=10)).strftime("%y%m%d"),(datetime.datetime.today() - datetime.timedelta(days=2) - datetime.timedelta(minutes=10)).strftime("%y%m%d")]
winup_path = r"SOFTWARE\Jamsu"
reg_handle = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
keyval=OpenKey(reg_handle,winup_path, 0, KEY_READ)

lastNumber = QueryValueEx(keyval, "Number")[0]


dayIndex = 0


keyval.Close()
reg_handle.Close()

if lastNumber < int(days[0] + "00000000"):
    lastNumber = int(days[0] + "00000000")
    reg_handle = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    keyval = OpenKey(reg_handle, winup_path, 0, KEY_WRITE)
    SetValueEx(keyval, "Number", 0, winreg.REG_QWORD, lastNumber)
    keyval.Close()
    reg_handle.Close()

print(lastNumber)

for day in days:
    tempPath = "guillotine/" + day
    if os.path.exists(tempPath) == False:
        os.makedirs(tempPath)

tempPath = "guillotine/" + (datetime.datetime.today() - datetime.timedelta(days=3)).strftime("%y%m%d")
if os.path.exists(tempPath):
    while True:
        try:
            shutil.rmtree(tempPath)
            break
        except:
            time.sleep(0.1)








while True:

    try:
        server = Server('browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat')
        server.start()
        print("서버스타트")
        proxy = server.create_proxy(params={'trustAllServers':'true'}) # Some time you need to add this parameter , Otherwise, the page may not open


        print("크롬 옵션 시작")
        # # # # todo chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless") # No interface mode
        # chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='chromedriver.exe')
        proxy.new_har("", options={'captureContent': True, 'captureHeaders': False, 'captureBinaryContent': True})
        print("크롬 옵션 완료")








        driver.get("https://nxlogin.nexon.com/common/login.aspx?redirect=https://barracks.sa.nexon.com/guillotine")
        time.sleep(1)
        driver.find_element(by=By.ID,value='txtNexonID').send_keys(ID)
        driver.find_element(by=By.ID,value='txtPWD').send_keys(PASSWORD)
        driver.find_element(by=By.CLASS_NAME,value='button01').click()


        time.sleep(3)

        if(driver.current_url.find("login.apsx?") >= 0):
            print("error occured!!")
            raise Exception('ID or Password is wrong!!', 'login.aspx? Error!!')



        elements = driver.find_elements(by = By.TAG_NAME, value = 'a')
        for e in elements:
            if e.text.find('[배심원] 사건 처리') >= 0:
                e.click()
                break


        time.sleep(3)
        print("배심원까지 왔다!")


        while True:
            today = (datetime.datetime.today() - datetime.timedelta(minutes=10)).strftime("%y%m%d")
            if (days[0] != today):
                tempPath = "guillotine/" + days[2]
                while True:
                    try:
                        shutil.rmtree(tempPath)
                        break
                    except:
                        time.sleep(0.1)
                days[2] = days[1]
                days[1] = days[0]
                days[0] = today
                os.makedirs("guillotine/"+today)
                lastNumber = int(today + "00000000")
                keyval = OpenKey(reg_handle, winup_path, 0, KEY_WRITE)
                SetValueEx(keyval, "Number", 0, winreg.REG_QWORD, lastNumber)
                keyval.Close()
                reg_handle.Close()

            #for i in findRange:
            for i in range(lastNumber % 100000000 + 1, lastNumber % 100000000 + 300):
                while True:
                    proxy.new_har("", options={'captureContent': True, 'captureHeaders': False, 'captureBinaryContent': True})
                    number = today + str(i).zfill(8)
                    driver.execute_script("client = new XMLHttpRequest(); client.open('POST','https://barracks.sa.nexon.com/api/Guillotine/GetDetailRead/" + number + "',true) ;client.send();")
                    proxy.wait_for_traffic_to_stop(1, 60)
                    time.sleep(oneDelay)

                    try:
                        proxyHar = str(proxy.har)

                        user_sn = proxyHar.split('user_nexon_sn":',1)[1].split(",",1)[0]
                        if user_sn == "0":
                            print(number + "없음")
                            break
                        else:

                            if int(number) > lastNumber:
                                lastNumber = int(number)
                                reg_handle = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
                                keyval = OpenKey(reg_handle, winup_path, 0, KEY_WRITE)
                                SetValueEx(keyval,"Number", 0, winreg.REG_QWORD, lastNumber)
                                keyval.Close()
                                reg_handle.Close()




                            tempPath = "guillotine/" + today + "/" + user_sn








                            if os.path.exists(tempPath) == False:
                                user_nick = proxyHar.split('user_nick":"', 1)[1].split('"', 1)[0]
                                kill_death = proxyHar.split('"kill_death_per":"', 1)[1].split('"', 1)[0] + "%"
                                win_per = proxyHar.split('"win_per":"', 1)[1].split('"', 1)[0]
                                ranking = proxyHar.split('"ranking":"', 1)[1].split('"', 1)[0]
                                user_img = proxyHar.split('"user_img":"', 1)[1].split('"', 1)[0]

                                total_matches = []
                                matches = proxyHar.split('"match_list":[', 1)[1].split('}],', 1)[0].split(
                                    '"match_key":"')
                                for j in range(1, len(matches)):
                                    match_plimit = matches[j].split('"plimit":', 1)[1].split(',', 1)[0]

                                    match_save_data = "!" + matches[j].split('"map_name":"', 1)[1].split('"', 1)[
                                        0] + "!@" + matches[j].split('"match_name":"', 1)[1].split('"', 1)[
                                                          0] + " " + match_plimit + " vs " + match_plimit + "!@" + \
                                                      matches[j].split('"kill_cnt":', 1)[1].split(',', 1)[0] + "!@" + \
                                                      matches[j].split('"death_cnt":', 1)[1].split(',', 1)[0] + "!@" + \
                                                      matches[j].split('"head_cnt":', 1)[1].split(',', 1)[0] + "!@" + \
                                                      matches[j].split('"damage_cnt":', 1)[1].split(',', 1)[0] + "!@" + \
                                                      matches[j].split('"assist_cnt":', 1)[1].split(',', 1)[0] + "!@" + \
                                                      matches[j].split('"save_cnt":', 1)[1].split(',', 1)[0] + "!@"

                                    if matches[j].split('"screenshot_flag":', 1)[1].split(',', 1)[0] == "true":
                                        while True:

                                            proxy.new_har("", options={'captureContent': True, 'captureHeaders': False,
                                                                       'captureBinaryContent': True})
                                            driver.execute_script(
                                                "client = new XMLHttpRequest(); client.open('POST','https://barracks.sa.nexon.com/api/Guillotine/GetScreenShotRead/" + user_sn + "/" +
                                                matches[j].split('"', 1)[0] + "/0',true) ;client.send();")

                                            proxy.wait_for_traffic_to_stop(1, 60)
                                            time.sleep(2.5)
                                            proxyHar2 = str(proxy.har)
                                            if proxyHar2.split("'status': ", 1)[1].split(',', 1)[0] == "200":
                                                screenshots = proxyHar2.split('"img_url":"')
                                                if len(screenshots) == 1:
                                                    match_save_data = match_save_data + "bypass"
                                                else:
                                                    for k in range(1, len(screenshots)):
                                                        match_save_data = match_save_data + \
                                                                          screenshots[k].split('",', 1)[0] + "!@"

                                                break
                                    total_matches.append(match_save_data)


                                total_comments = []
                                comments = proxyHar.split('"comment_info":{', 1)[1].split("}]}", 1)[0].split('"user_nick":"')
                                for j in range(1, len(comments)):
                                    comment_user_sn = comments[j].split('"user_nexon_sn":', 1)[1].split(',', 1)[0]
                                    comment_user_nick = comments[j].split('"', 1)[0]
                                    comment_content = \
                                    comments[j].split('"comment_content":"', 1)[1].split('","comment_no"', 1)[0]

                                    total_comments.append("#"+comment_user_sn + "!@" + comment_user_nick + " : " + comment_content)





                                f = open(tempPath,'w')
                                f.writelines(number + "\n")    # 사건번호
                                f.writelines(user_nick+ "\n")
                                f.writelines(kill_death+ "\n")
                                f.writelines(win_per+ "\n")
                                f.writelines(ranking+ "\n")
                                f.writelines(user_img+ "\n")
                                for j in total_matches:
                                    f.writelines(j+ "\n")
                                for j in total_comments:
                                    f.writelines(j+ "\n")

                                f.close()
                            print(number + "있다요!! ")
                            break
                    except IndexError as e:
                        print(number + "," + str(traceback.format_exc()))
                        print(proxyHar)

            dayIndex = (dayIndex + 1 ) % 3
            tempPath = "guillotine/" + days[dayIndex]
            file_Lst = os.listdir(tempPath)
            print("고쳐보자!!!")
            for file in file_Lst:
                filePath = tempPath +'/' + file
                while True:
                    try:
                        f = open(filePath, 'r')
                        break
                    except:
                        time.sleep(0.1)
                lines = f.readlines()
                f.close()
                while True:
                    try:
                        proxy.new_har("", options={'captureContent': True, 'captureHeaders': False,'captureBinaryContent': True})
                        number = lines[0][:-1]
                        driver.execute_script(
                            "client = new XMLHttpRequest(); client.open('POST','https://barracks.sa.nexon.com/api/Guillotine/GetDetailRead/" + number + "',true) ;client.send();")
                        proxy.wait_for_traffic_to_stop(1, 60)
                        time.sleep(oneDelay)
                        proxyHar = str(proxy.har)
                        user_sn = proxyHar.split('user_nexon_sn":', 1)[1].split(",", 1)[0]
                        if user_sn == "0":
                            print(number + " 종결 !! 삭제!")
                            while True:
                                try:
                                    os.remove(filePath)
                                    break
                                except:
                                    time.sleep(0.1)
                            break
                        else:
                            tempTotalCount = len(lines)
                            tempCount = 6
                            for i in range(6,tempTotalCount):
                                if lines[i][:1] != "!":
                                    break
                                else:
                                    tempCount = tempCount + 1
                            saveCount = tempCount
                            tempCount = tempTotalCount - tempCount

                            comments = proxyHar.split('"comment_info":{', 1)[1].split("}]}", 1)[0].split('"user_nick":"')
                            if (len(comments) -1) == tempCount:
                                print(filePath + "는 똑같음!")
                            else:
                                while True:
                                    try:
                                        f = open(filePath,'w')
                                        break
                                    except:
                                        time.sleep(0.1)



                                for j in range(0, saveCount):
                                    f.writelines(lines[j])


                                for j in range(1, len(comments)):
                                    comment_user_sn = comments[j].split('"user_nexon_sn":', 1)[1].split(',', 1)[0]
                                    comment_user_nick = comments[j].split('"', 1)[0]
                                    comment_content = \
                                    comments[j].split('"comment_content":"', 1)[1].split('","comment_no"', 1)[0]

                                    f.writelines("#"+comment_user_sn + "!@" + comment_user_nick + " : " + comment_content+'\n')
                                print(filePath+" 댓글 수정됌!" )



                                f.close()




                            break



                    except IndexError:
                        print("Index Error Occured!!\n"+str(traceback.format_exc())+"\n사건번호 : "+number + ", 파일명 :" + filePath+ "\n 프록시 값 : " + proxyHar)








    except:
        try:
            server.stop()
        except:
            pass
        try:
            driver.quit()
        except:
            pass
        print( str(traceback.format_exc()))
        time.sleep(120)