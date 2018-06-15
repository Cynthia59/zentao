#encoding: utf-8
"""
@project = zentao
@file = bug_selenium
@function = bug统计(模拟操作)
@author = Cindy
@create_time = 2018/5/17 17:20
@python_version = 3.x
PIL不支持3.x,用Pillow代替
"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time,shutil,os
import myimage
import settings
import autoit

driver = webdriver.Ie()
driver.maximize_window()

imagepath = './image'

def screenshot(name):
    imagefile = imagepath + '/%s.png' % name
    # driver.get_screenshot_as_file(imagefile)
    myimage.screenshot_by_size(imagefile, 358, 300, 1568, 756)

def openedBugsPerDay(productName, productId, moduleName):
    '''每天新增bug数'''
    #login
    url = 'http://192.168.2.203/zentao/www/index.php?m=bug&f=browse&productID='+productId
    driver.get(url)
    #记住账号密码，不需要每次登录
    # if driver.find_element_by_xpath('//*[@id="account"]').is_displayed():
    #     driver.find_element_by_xpath('//*[@id="account"]').send_keys('禅道通知')
    #     driver.find_element_by_xpath('//*[@id="login-form"]/form/table/tbody/tr[2]/td/input').send_keys('tester2018')
    #     driver.find_element_by_xpath('//*[@id="submit"]').click()
    time.sleep(2)

    # 搜索
    #所属模块
    driver.find_element_by_xpath('//*[@id="bysearchTab"]/a').click()
    time.sleep(1)
    s1 = Select(driver.find_element_by_id('field1'))
    s1.select_by_visible_text('所属模块')
    s2 = Select(driver.find_element_by_id('value1'))
    s2.select_by_visible_text('/'+moduleName)
    #第二个搜索框置空，防止跑下一个项目时，第二项为未关闭bug
    s1 = Select(driver.find_element_by_id('field3'))
    s1.select_by_visible_text('Bug标题')
    #点击搜索
    driver.find_element_by_xpath('//*[@id="submit"]').click()
    time.sleep(1)

    #点击报表
    driver.find_element_by_xpath('//*[@id="featurebar"]/div[1]/div[1]/div[2]/a').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="chartsopenedBugsPerDay"]').click()
    # time.sleep(1)
    driver.find_element_by_xpath('//*[@id="submit"]').click()
    time.sleep(1)
    screenshot(productName+'_每日新增bug数')

def bugsPerUserToday(productName, productId, searchItem):
    '''每人提交bug数'''
    #点返回
    driver.find_element_by_xpath('//*[@id="titlebar"]/div[2]/a').click()
    time.sleep(1)

    #根据搜索条目定义控件
    # def today(i):
    #     return '/html/body/div['+i+']/div[3]/table/tfoot/tr/th'
    # todays = []
    # for i in [5,7,9,6,8,10]:
    #     todays.append(today(str(i)))
    # print(todays)

    if searchItem == '创建日期':
        selectItem = 'chartsopenedBugsPerUser'
        imageName = '每人提交bug数'
    elif searchItem == '解决日期':
        selectItem = 'chartsresolvedBugsPerUser'
        imageName = '每人解决bug数'
    elif searchItem == '关闭日期':
        selectItem = 'chartsclosedBugsPerUser'
        imageName = '每人关闭bug数'

    #搜索
    # driver.find_element_by_xpath('//*[@id="bysearchTab"]/a').click()
    s1 = Select(driver.find_element_by_id('field3'))
    s1.select_by_visible_text(searchItem)
    s2 = Select(driver.find_element_by_id('operator3'))
    s2.select_by_visible_text('=')
    driver.find_element_by_xpath('//*[@id="value3"]').click()
    autoit.mouse_click('main', 1190, 466) #autoit需要屏幕常亮，不使用jenkins
    # for today in todays:
    #     if driver.find_element_by_xpath(today).is_displayed():
    #         print(today)
    #         driver.find_element_by_xpath(today).click()
    driver.find_element_by_xpath('//*[@id="submit"]').click()
    time.sleep(1)

    # 点击报表
    driver.find_element_by_xpath('//*[@id="featurebar"]/div[1]/div[1]/div[2]/a').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="'+selectItem+'"]').click()
    # time.sleep(1)
    driver.find_element_by_xpath('//*[@id="submit"]').click()
    time.sleep(1)
    screenshot(productName+'_'+imageName)

def bugsPerAssignedTo(productName, productId, moduleName):
    '''指派给'''
    #点返回
    driver.find_element_by_xpath('//*[@id="titlebar"]/div[2]/a').click()
    time.sleep(1)

    # 搜索
    # driver.find_element_by_xpath('//*[@id="bysearchTab"]/a').click()
    s1 = Select(driver.find_element_by_id('field3'))
    s1.select_by_visible_text('Bug状态')
    s2 = Select(driver.find_element_by_id('operator3'))
    s2.select_by_visible_text('!=')
    s3 = Select(driver.find_element_by_id('value3'))
    s3.select_by_visible_text('已关闭')
    driver.find_element_by_xpath('//*[@id="submit"]').click()   #搜索
    time.sleep(1)

    # 点击报表
    driver.find_element_by_xpath('//*[@id="featurebar"]/div[1]/div[1]/div[2]/a').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="chartsbugsPerAssignedTo"]').click()
    # time.sleep(1)
    driver.find_element_by_xpath('//*[@id="submit"]').click()
    time.sleep(1)
    screenshot(productName+'_指派给bug数')

# 运行脚本

for i in settings.products:
    print(time.ctime(), i)
    productName = i[0]
    productId = i[1]
    moduleName = i[2]

    openedBugsPerDay(productName, productId, moduleName)
    bugsPerUserToday(productName, productId,'创建日期')
    bugsPerUserToday(productName, productId,'解决日期')
    bugsPerUserToday(productName, productId,'关闭日期')
    bugsPerAssignedTo(productName, productId, moduleName)

driver.quit()


path = 'E:/软件和工具/禅道自动统计bug截图'
if os.path.exists(path):
    shutil.rmtree(path)
shutil.copytree('./image/', path)
