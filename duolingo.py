from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from cfg import Base


class Duolingo(Base):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 关闭log
    options.page_load_strategy = 'eager' # 修改页面加载策略
    d = webdriver.Chrome(options=options)  
    d.implicitly_wait(15)
    wait = WebDriverWait(d, 12)

    # 已有账户btn
    already_have_an_account_locator = (By.XPATH, '//button[@data-test="have-account"]')
    username_locator = (By.XPATH, '//input[@data-test="email-input"]')
    passwd_locator = (By.XPATH, '//input[@data-test="password-input"]')
    login_btn_locator = (By.XPATH, '//button[@data-test="register-button"]')
    invalid_email_locator = (By.XPATH, '//*[@data-test="invalid-form-field"]')
    # 练习基地
    exercise_base_locator = (By.XPATH, '//*[@data-test="practice-hub-nav"]')
    # 小故事
    story_btn_locator = (By.XPATH, '//*[@id="root"]//div[2]/div/button[2]')
    # 所有的小故事 
    all_stories_locator = (By.XPATH, '//img/../../div[2]/div[2]/div/div')
    story_title_relative_locator = (By.XPATH, './/*[contains(@data-test, "title")]')
    # 更多
    more_btn_locator = (By.XPATH, '//*[@data-test="more-nav"]')
    sub_div_xpath = '//*[@id="root"]//div[last()]//span/div/div'
    # 学校按钮 
    school_btn_locator = (By.XPATH, '//*[@id="root"]//div[last()]//span/div/div/div[1]') 
    # Schools顶部tab 菜单
    top_tab_xpath = '//*[@id="right-panel"]/../div[2]'
    assign_task_xpath = top_tab_xpath + '//a[2]/p'
    # 布置作业tab
    assign_task_lactor = (By.XPATH, assign_task_xpath)
    # 筛选条件按钮
    filter_btn_locator = (By.XPATH, '//*[@data-test="assign-v2-static-filter-bar"]//button[1]')
    # 学习内容类型
    learning_content_type_locator =  (By.XPATH, '//*[@data-test="lessons-unit-filter-option"]/..')
    # 学习单元
    learning_unit_checbox_locator = (By.XPATH, './label[1]/div')    
    # 小故事checkbox
    short_story_checkbox = (By.XPATH, './label[2]/div')
    # 显示结果
    sure_btn_locator = (By.XPATH, '//*[@data-test="show-results-unit-filters-modal-button"]')
    section_xpath = '//*[@id="root"]/div[1]/div/div[3]/div/div[2]/section'
    section_locator = (By.XPATH, section_xpath)
    # 第几部分
    section_no_locator = (By.XPATH, './/h1')
    section_name_locator = (By.XPATH, './/h3')
    # CEFR level
    cefr_level_locator = (By.XPATH, section_xpath + '/header/div[1]/div[1]/div[1]//span')
    # 单词数量
    words_locator = (By.XPATH, './header/div[1]/div/div[2]/div/span')
    num_of_stories_locator = (By.XPATH, './header/div[1]/div/div[3]/div/span')
    # 学习单元
    learning_unit_locator = (By.XPATH, './div')
    # 单元类型
    learning_unit_type_locator = (By.XPATH, './div[3]/span')
    # 显示更多
    show_more_btn_locator = (By.XPATH, './div[2]/button')
    # 新单词
    new_words_locator = (By.XPATH, './div/div/div/div/p')
    # 小故事
    short_story_div_list_locator = (By.XPATH, './div')
    # 序号
    story_id_locator = (By.XPATH,  './div[1]/div[1]/span')
    story_title_locator = (By.XPATH, './div[1]/div/div/h5')
    story_desc_locator = (By.XPATH, './div[1]/div/div/p')


    def scroll_ele_into_view(self, webelement):
        """使元素处于正中"""
        self.d.execute_script("arguments[0].scrollIntoView({block:'center',inline:'center'})", webelement)


    def get_site(self):  
        """访问网址"""  
        self.d.get(self.url)

    
    def click_already_have_an_account_btn(self):
        """点击已有帐户按钮"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.already_have_an_account_locator)).click()
        except:
            return False
        

    def type_account(self):
        """输入账号"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.username_locator)).send_keys(self.account)
        except:
            return False
        
    def type_passwd(self):
        """输入密码"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.passwd_locator)).send_keys(self.passwd)
        except:
            return False
        
    
    def click_login_btn(self):
        """点击login按钮"""
        try:
            login_btn = self.wait.until(EC.element_to_be_clickable(self.login_btn_locator))
            login_btn.click()
            # 如果出现邮箱未注册，则再点击一次login按钮
            if self.wait.until(EC.visibility_of_element_located(self.invalid_email_locator)):
                login_btn.click()
        except:
            return False
        

    def click_exercise_base(self):
        """点击练习基地按钮"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.exercise_base_locator)).click()
        except:
            return False
        
        
    def click_short_story(self):
        """点击小故事按钮"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.story_btn_locator)).click()
        except:
            return False


    def write_all_story_titles_to_a_file(self):
        """将所有的小故事标题写入文件"""
        try:
            story_list = self.wait.until(EC.presence_of_all_elements_located(self.all_stories_locator))
            story_titles = []
            for _, ele in enumerate(story_list):
                story_title = ele.find_element(*self.story_title_relative_locator).text.strip()
                story_titles.append(story_title)
            with open('all_stories_titles.txt', "w", encoding='utf8') as f:
                f.write("\n".join(story_titles))
        except:
            return False

    
    def move_to_ele(self, target_webEle):
        """移动鼠标到目标元素"""
        ActionChains(self.d).move_to_element(target_webEle).perform()


    def switch_to_window(self, keyword):
        """切换到指定窗口"""
        for handle in self.d.window_handles:
            self.d.switch_to.window(handle)
            if keyword in self.d.current_url:
                break


    def move_to_more_btn(self):
        """移动到更多按钮"""
        try:
            more_btn = self.wait.until(EC.presence_of_element_located(self.more_btn_locator))
            self.move_to_ele(more_btn)
        except:
            return False


    def click_school_btn(self):
        """点击schools"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.school_btn_locator)).click()
        except:
            return False
        

    def click_assign_task_btn(self):
        """点击布置作业"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.assign_task_lactor)).click()
        except:
            return False


    def click_filter_btn(self):
        """点击筛选条件"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.filter_btn_locator)).click()
        except:
            return False

    
    def tick_content(self, content_type="学习单元"):
        """勾选学习内容类型"""
        try:
            learning_content_type_div = self.wait.until(EC.presence_of_element_located(self.learning_content_type_locator))
            if content_type=="学习单元":    
                learning_content_type_div.find_element(*self.learning_unit_checbox_locator).click()
                return
            elif content_type=="小故事":
                learning_content_type_div.find_element(*self.short_story_checkbox).click()
        
        except:
            return False
        
    
    def click_sure(self):
        """点击显示结果"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.sure_btn_locator)).click()
        except:
            return False
        

    def calc_all_section_words(self):
        """计算所有部分的单词总数"""       
        total_words = 0 
        lines = []  # 保存所有的行
        try:
            section_ele_list = self.wait.until(EC.presence_of_all_elements_located(self.section_locator))            
            for i, ele in enumerate(section_ele_list):
                try:
                    wordsinfo = ele.find_element(*self.words_locator).text.strip()
                    total_words += int(wordsinfo.split('个')[0])
                    lines.append(f"{i+1}: {wordsinfo}")  # 添加这一行到lines列表中
                except:
                    continue
            with open('words.txt', "w", encoding='utf8') as f:
                f.write('\n'.join(lines))
            return total_words
        except:
            return total_words  
        
    
    def get_all_new_words(self):
        """拿到所有基础单元里面的的新单词"""       
        all_new_words_list = []
        try:
            section_ele_list = self.wait.until(EC.presence_of_all_elements_located(self.section_locator))
        
            for i, section_ele in enumerate(section_ele_list):
                try:
                    self.scroll_ele_into_view(section_ele)
                    learning_unit_eles = section_ele.find_elements(*self.learning_unit_locator)
                    for i in learning_unit_eles:
                        unit_type_ele = i.find_element(*self.learning_unit_type_locator).text.strip()
                        show_more_btn = i.find_element(*self.show_more_btn_locator)
                    
                        if unit_type_ele=="基础":
                            self.scroll_ele_into_view(show_more_btn)
                            show_more_btn.click()
                            new_words_list = i.find_elements(*self.new_words_locator)
                            for i in new_words_list:
                                listed_words = i.text.strip()  # 'like, english, chinese, I, you'
                                each_words_list = listed_words.split(', ')
                                all_new_words_list += each_words_list    
                except:
                    return False
            return all_new_words_list 
        except:
            return False
        

    def de_duplication_for_list(self, original_list):
        """对列表中的元素去重"""
        new_list = sorted(set(original_list), key=original_list.index)

        return new_list
    

    def write_to_file(self, words_list, file_name):
        """将列表中的元素，按行写入文件"""
        with open(file_name, "w", encoding='utf8') as f:
            f.write('\n'.join(words_list))


    def get_execution_time(self, start_time):
        """获取函数执行的时间"""
        end_time = time.time()
        total_time = end_time - start_time
        minutes, seconds = divmod(total_time, 60)
        print(f"代码运行时间：{int(minutes)}分{seconds:.2f}秒")


    def login_by_an_account(self):
        """通过已有帐号密码登录"""
        self.get_site()
        self.click_already_have_an_account_btn()
        self.type_account()
        self.type_passwd()
        self.click_login_btn()


    def get_all_story_titles(self):
        """将所有的小故事标题写入文件"""
        start_time = time.time()
        self.click_exercise_base()
        self.click_short_story()
        self.write_all_story_titles_to_a_file()
        self.get_execution_time(start_time)


    def my_func(self):
        self.move_to_more_btn()
        self.click_school_btn()
        self.switch_to_window('schools')
        self.click_assign_task_btn()
        self.click_filter_btn()
        self.tick_content()
        self.click_sure()


    def print_all_words(self):
        """计算所有的单词数量"""
        # 获取开始时间
        start_time = time.time()
        self.my_func()
        total_words = duo.calc_all_section_words()
        print(f"共有{total_words}个单词")
        self.get_execution_time(start_time)


    def write_all_words_to_file(self):
        """将未去重的所有单词写入文件"""
        start_time = time.time()
        all_new_words_list = duo.get_all_new_words()
        self.write_to_file(all_new_words_list,'未去重的所有单词.txt')
        self.get_execution_time(start_time)


    def dedepulicate_words_to_file(self, input_file, output_file):
        """从输入文件中读取单词，去重，然后写入到输出文件中"""
        start_time = time.time()
        seen = set()  # 检查是否已经见过这个单词
        words = []  # 保存所有单词的顺序
        with open(input_file, 'r', encoding='utf8') as f:
            for line in f:
                word = line.strip()  
                if word not in seen:  # 如果是一个新单词
                    seen.add(word)  # 记录已经见过这个单词
                    words.append(word)  

        with open(output_file, 'w', encoding='utf8') as f:
            f.write('\n'.join(words))  

        self.get_execution_time(start_time)



duo = Duolingo()
# 登录
duo.login_by_an_account()
# 将所有的小故事标题写入文件
duo.get_all_story_titles()
## 计算所有的单词数量
duo.print_all_words()
## 将未去重的所有单词写入文件
duo.write_all_words_to_file()
# ## 将去重后的所有单词写入文件
duo.dedepulicate_words_to_file('未去重的所有单词.txt', '去重后的所有单词.txt')