# from selenium import webdriver
# import unittest

# class GoogleTestCase(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.addCleanup(self.browser.quit)

#     def testPageTitle(self):
#         self.browser.get('http://localhost:22362/')
#         self.assertIn('Google', self.browser.title)

# if __name__ == '__main__':
#     unittest.main(verbosity=2)

from time import sleep

import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Chrome()
action_chains = ActionChains(browser)

url = 'http://psiturk-hamiltonian:22362/ad?assignmentId=debugI4SGTK&hitId=debugF0878N&workerId=debugFWECF5&mode=debug'


def check_if_id_exists(id):
    return len(browser.find_elements_by_id(id)) > 0


def wait_for_text_and_next(text, timeout=10):
    WebDriverWait(browser, timeout).until(
        EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/p"),
                                         text))
    browser.find_element_by_id('next').click()


def test_1(full_test=False):
    browser.get(url)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn")))
    assert 'Psychology Experiment' in browser.title
    browser.find_element_by_class_name('btn').click()

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
    browser.switch_to.window(browser.window_handles[-1])
    browser.find_element_by_class_name('btn-primary').click()

    # consentaccept
    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/h1"), 'You may download'))
    browser.find_element_by_class_name('btn-primary').click()

    # instructions
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "next")))
    browser.find_element_by_id('next').click()

    wait_for_text_and_next('While you are looking at the stream of images')

    wait_for_text_and_next('If your overall accuracy')

    wait_for_text_and_next('After the 35-minute phase of the experiment')

    # quiz 1
    do_quiz_1(browser)

    # start_part_2
    browser.execute_script("PRETASK_TIME = 1;")

    wait_for_text_and_next("You're almost ready to begin!")
    do_pretest(browser)

    # start_online
    if full_test:
        browser.execute_script("DISPLAY_TIME = 800;")        
    else:
        browser.execute_script("DISPLAY_TIME = 1;")
        browser.execute_script("N_WRONG_MAX = 50000;")
    wait_for_text_and_next("The 35-minute stream will begin now.")

    if full_test:
        n = detect_rotation(browser)
        print(n)

    # Post 1
    wait_for_text_and_next("Congratulations! You've finished the longest phase of the experiment.", timeout=60)
    wait_for_text_and_next("Just as before, if your overall accuracy")

    # Quiz 2
    do_quiz_2(browser)

    if full_test:
        browser.execute_script("DISPLAY_TIME = 800;")
    else:
        browser.execute_script("DISPLAY_TIME = 1;")
        browser.execute_script("N_WRONG_MAX = 50000;")
    wait_for_text_and_next("Ready? We'll get started on the next phase")

    if full_test:
        n = detect_rotation(browser)
        print(n)

    # wait_for_text_and_next("You're almost done")

    WebDriverWait(browser, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/p"),
                                         "You're almost done"))
    browser.find_element_by_id('observations').send_keys("selenium test");
    browser.find_element_by_id('next').click()
    # browser.find_element_by_id('next').click()

    # observation_path = "/html/body/div[@id='container-questionnaire']/div[@class='instructions-well']


    # browser.implicitly_wait(1)
    # do_offline_test()

    # questionnaire_path = "/html/body/div[@id='container-questionnaire']/h1"
    # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, questionnaire_path)))
    # browser.find_element_by_id('next').click()


def test_failure(full_test=False):
    browser.get(url)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn")))
    assert 'Psychology Experiment' in browser.title
    browser.find_element_by_class_name('btn').click()

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
    browser.switch_to.window(browser.window_handles[-1])
    browser.find_element_by_class_name('btn-primary').click()

    # consentaccept
    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, "/html/body/div/div/h1"), 'You may download'))
    browser.find_element_by_class_name('btn-primary').click()

    # instructions
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "next")))
    browser.find_element_by_id('next').click()

    wait_for_text_and_next('While you are looking at the stream of images')

    wait_for_text_and_next('The amount of time')

    wait_for_text_and_next('After the first phase of the experiment')

    # quiz 1
    do_quiz_1(browser)

    # start_part_2
    browser.execute_script("PRETASK_TIME = 1;")

    wait_for_text_and_next("You're almost ready to begin!")
    do_pretest(browser)

    # start_online
    browser.execute_script("DISPLAY_TIME = 1;")
    wait_for_text_and_next("The 35-minute stream will begin now.")

    # Make sure failure text exists
    instructions_path = "/html/body/div[@id='container-instructions']/div/p"
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, instructions_path)))
    browser.find_element_by_xpath(instructions_path).text == 'You missed ten consecutive dots.'
    wait_for_text_and_next('You missed ten consecutive dots.')

    questionnaire_path = "/html/body/div[@id='container-questionnaire']/h1"
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, questionnaire_path)))
    browser.find_element_by_id('next').click()


def test_cancel_quits():
    browser = webdriver.Firefox()

    browser.get(url)
    browser.find_element_by_class_name('btn').click()
    new_window = browser.window_handles[-1]
    browser.switch_to.window(new_window)
    browser.find_element_by_class_name('btn-danger').click()

    assert new_window not in browser.window_handles

    browser.quit()


def quiz_helper(ans):
    if ans in browser.find_element_by_id("answer1").text:
        browser.switch_to.active_element.send_keys(1)
    elif ans in browser.find_element_by_id("answer2").text:
        browser.switch_to.active_element.send_keys(2)
    elif ans in browser.find_element_by_id("answer3").text:
        browser.switch_to.active_element.send_keys(3)


def do_quiz_1(browser):
    print('Executing Quiz 1')
    N_QUESTIONS = 8
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "question")))
    for i in range(N_QUESTIONS):
        browser.implicitly_wait(0.01)
        q = browser.find_element_by_id("question").text
        if "What happens if your response is incorrect?" in q:
            quiz_helper("You'll hear a HIGH tone.")
        elif "What will be flashed on the screen while you participate in this experiment?" in q:
            quiz_helper('Unfamiliar objects')
        elif "What happens if you don't make your response in time?" in q:
            quiz_helper("You'll hear a LOW tone.")
        elif "How long do you have to make your response?" in q:
            quiz_helper("Until the next image in the stream appears on the screen")
        elif "What happens if your overall accuracy on the rotation task is greater than 90% correct?" in q:
            quiz_helper("You get a monetary bonus of $1 at the end of the experiment.")
        elif "Other than looking at the screen, what additional task should you perform?" in q:
            quiz_helper("Hit [2] when an image is rotated and [1] when it is NOT rotated.")
        elif "How long will the stream of images go on for?" in q:
            quiz_helper("About 35 minutes")
        elif "What happens if you respond incorrectly to more than 10 of the rotated images in a row?" in q:
            quiz_helper("The experiment terminates automatically.")


def do_pretest(browser):
    print('Executing Pretest')
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "heading")))
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "testcategoryshown")))
    has_heading = True
    while has_heading:
        heading = browser.find_element_by_id('heading').text
        if "Which image is rotated?" in heading:            
            im0 = browser.find_elements_by_class_name("testcategoryshown")[0]
            im1 = browser.find_elements_by_class_name("testcategoryshown")[1]
            if 'rotated' in im0.get_attribute('src'):
                browser.switch_to.active_element.send_keys(1)
            elif 'rotated' in im1.get_attribute('src'):
                browser.switch_to.active_element.send_keys(2)
        browser.implicitly_wait(0.1)
        has_heading = len(browser.find_elements_by_id('heading')) > 0


def detect_rotation(browser):
    print('Executing Rotation Detection')

    images = []

    def get_shown_status():
        is_shown = [len(i.get_attribute('class')) == 11 for i in images]
        return np.array(is_shown)

    def check_heading():
        heading = browser.find_elements(By.XPATH, "/html/body/div/div/h1")
        return len(heading) > 0 and "Carefully watch the sequence!" in heading[0].text

    def press_next_key(shown):
        # print(np.where(shown)[0][0])
        if np.where(shown)[0][0] < 24:
            print('1')
            browser.switch_to.active_element.send_keys(1)
        else:
            print('2')
            browser.switch_to.active_element.send_keys(2)

    for i in range(48):
        WebDriverWait(browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div[@id='fractal']/img[@id='image%d']" % (i))))
        images.append(browser.find_elements(By.XPATH,
                                            "/html/body/div/div/div[@id='fractal']/img[@id='image%d']" % (i))[0])

    shown = get_shown_status()
    while(sum(shown) < 1):
        shown = get_shown_status()
    shown_next = shown

    n = 0
    # has_heading = True

    while True:
        try:
            n += 1
            press_next_key(shown)
            while np.sum(np.abs(shown_next - shown)) != 2 or (sum(shown_next) != 1):
                shown_next = get_shown_status()
            shown = shown_next
        except StaleElementReferenceException:
            break
        # has_heading = check_heading()
    return n


# def do_offline_test():
#     browser.implicitly_wait(2)
#     for i in range(27):
#         # browser.implicitly_wait(0.1)
#         action_chains.send_keys((i % 3) + 1)
#     action_chains.perform()

# test_1()
