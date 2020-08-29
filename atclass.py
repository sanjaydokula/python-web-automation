from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
from time import localtime,strftime
from datetime import date as dt
import os
import pyautogui

user = os.environ['GUSER'] 
passw = os.environ['GPASS'] 
print(user,passw)
gitamDriver = webdriver.Chrome(ChromeDriverManager().install())
gitamDriver.maximize_window()
gitamDriver.get("https://login.gitam.edu/Login.aspx")
gitamDriver.find_element_by_name('txtusername').send_keys(user)
gitamDriver.find_element_by_name('password').send_keys(passw)
loginb = gitamDriver.find_element_by_xpath('//*[@id="form1"]/div[3]/div[1]/div[2]/div[3]/div[1]')
loginb.click()
gitamDriver.find_element_by_xpath('//*[@id="form1"]/div[4]/ul/li[1]/a/h5').click()
links = len(gitamDriver.find_elements_by_xpath('//*[@id="ContentPlaceHolder1_GridViewonline"]/tbody/tr'))
today = dt.today()
tdate = str(today)
tdate = tdate[8:]
cth,ctm,cds = strftime("%I %M %p", localtime()).split()
# cth,ctm,cds = 2,0,"PM"
ct = (int(cth)*60)+int(ctm)
sesl = []
for i in range(1,links+1):
    sestimepath = '//*[@id="ContentPlaceHolder1_GridViewonline"]/tbody/tr[{}]/td/a/div/h6'.format(i)
    link = gitamDriver.find_element_by_xpath(sestimepath)
    des = link.text
    desl = list(des.split())
    date = int(desl[2].split('-')[0])
    if(date == int(tdate)):
        sth,stm,scds = int(desl[4].split(':')[1]),int(desl[4].split(':')[2][0:2]),(desl[4].split(':')[2][-2::])
        st = (sth*60)+stm
        sesl.append(st)
        if(cds == scds):
            tdiff = abs(st-ct)
            if(tdiff <= 10 and tdiff>=0):
                print("can join")
                gitamDriver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_GridViewonline"]/tbody/tr[{}]/td/a/div'.format(i)).click()
                # print(gitamDriver.current_window_handle)
                gitamDriver.switch_to.window(gitamDriver.window_handles[1])
                time.sleep(3)
                pyautogui.click(x=745,y=219,clicks=1)
                # gitamDriver.execute_script("window.confirm = function() {return true;};")     
                break
            else:
                print("have a session at {0}:{1}0 today".format(min(sesl)//60,min(sesl)%60))
else:
    print("no session found")
time.sleep(3)
gitamDriver.quit()