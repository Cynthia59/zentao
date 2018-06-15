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
import settings

class Bug(object):
    '''统计bug模块'''
    def __init__(self, productId, productName, moduleName):
        self.driver = webdriver.Ie()
        self.driver.maximize_window()
        self.productId = productId
        self.productName = productName
        self.moduleName = moduleName

    #截图
    def insert_img(self, file_name):
        file_path = './image/%s.png' % file_name
        self.driver.get_screenshot_as_file(file_path)

    #登录及选择产品
    def login(self):
        url = 'http://192.168.2.203/zentao/www/index.php?m=bug&f=browse&productID=' + self.productId
        self.driver.get(url)
        try:
            self.driver.find_element_by_xpath('//*[@id="account"]').send_keys('禅道通知')
            self.driver.find_element_by_xpath('//*[@id="login-form"]/form/table/tbody/tr[2]/td/input').send_keys('tester2018')
            self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        except Exception as e:
            print(e)
        finally:
            time.sleep(1)
            #点击搜索按钮
            self.driver.find_element_by_xpath('//*[@id="bysearchTab"]/a').click()
            time.sleep(1)

    #每天新增bug数
    def openedBugsPerDay(self):
        # 搜索
        #所属模块
        s1 = Select(self.driver.find_element_by_id('field1'))
        s1.select_by_visible_text('所属模块')
        s2 = Select(self.driver.find_element_by_id('value1'))
        s2.select_by_visible_text('/'+moduleName)
        #第二个搜索框置空，防止跑下一个项目时，第二项为未关闭bug
        s1 = Select(self.driver.find_element_by_id('field3'))
        s1.select_by_visible_text('Bug标题')
        #点击搜索
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        #点击报表
        self.driver.find_element_by_xpath('//*[@id="featurebar"]/div[1]/div[1]/div[2]/a').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="chartsopenedBugsPerDay"]').click()
        # time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)
        self.insert_img(self.productName+'_每日新增bug数')
        # 点击返回
        self.driver.find_element_by_xpath('//*[@id="titlebar"]/div[2]/a').click()
        time.sleep(1)

    #每天每人提交bug数
    def bugsPerUserToday(self, searchItem):
        #根据搜索条件定义控件
        if searchItem == '创建日期':
            selectItem = 'chartsopenedBugsPerUser'
            imageName = '每人提交bug数'
        elif searchItem == '解决日期':
            selectItem = 'chartsresolvedBugsPerUser'
            imageName = '每人解决bug数'
        elif searchItem == '关闭日期':
            selectItem = 'chartsclosedBugsPerUser'
            imageName = '每人关闭bug数'

        # "今日"控件不固定，获取控件列表
        def today(i):
            return '/html/body/div[' + i + ']/div[3]/table/tfoot/tr/th'
        todays = []
        for i in range(5, 10):
            todays.append(today(str(i)))

        #搜索
        # driver.find_element_by_xpath('//*[@id="bysearchTab"]/a').click()
        s1 = Select(self.driver.find_element_by_id('field3'))
        s1.select_by_visible_text(searchItem)
        s2 = Select(self.driver.find_element_by_id('operator3'))
        s2.select_by_visible_text('=')
        self.driver.find_element_by_xpath('//*[@id="value3"]').click()
        # autoit.mouse_click('main', 1190, 466) #autoit需要屏幕常亮，不适用jenkins
        for today in todays:
            try:
                self.driver.find_element_by_xpath(today).click()
            except Exception as e:
                pass
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        # 点击报表
        self.driver.find_element_by_xpath('//*[@id="featurebar"]/div[1]/div[1]/div[2]/a').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="'+selectItem+'"]').click()
        # time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)
        self.insert_img(self.productName+'_'+imageName)
        # 点返回
        self.driver.find_element_by_xpath('//*[@id="titlebar"]/div[2]/a').click()
        time.sleep(1)

    #指派给bug数
    def bugsPerAssignedTo(self):
        # 搜索
        s1 = Select(self.driver.find_element_by_id('field3'))
        s1.select_by_visible_text('Bug状态')
        s2 = Select(self.driver.find_element_by_id('operator3'))
        s2.select_by_visible_text('!=')
        s3 = Select(self.driver.find_element_by_id('value3'))
        s3.select_by_visible_text('已关闭')
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()   #搜索
        time.sleep(1)

        # 点击报表
        self.driver.find_element_by_xpath('//*[@id="featurebar"]/div[1]/div[1]/div[2]/a').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="chartsbugsPerAssignedTo"]').click()
        # time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)
        self.insert_img(self.productName+'_指派给bug数')

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    for i in settings.products:
        print(time.ctime(), i)
        productName = i[0]
        productId = i[1]
        moduleName = i[2]
        #执行脚本
        bug = Bug(productId, productName, moduleName)
        bug.login()
        bug.openedBugsPerDay()
        bug.bugsPerUserToday('创建日期')
        bug.bugsPerUserToday('解决日期')
        bug.bugsPerUserToday('关闭日期')
        bug.bugsPerAssignedTo()
        bug.quit()

    # path = 'E:/软件和工具/禅道自动统计bug截图'
    # if os.path.exists(path):
    #     shutil.rmtree(path)
    # shutil.copytree('./image/', path)
