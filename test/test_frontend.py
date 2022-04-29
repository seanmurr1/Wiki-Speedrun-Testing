from curses import KEY_UP
from doctest import UnexpectedException
from tkinter import W
from unittest.result import failfast

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException  
from selenium.common.exceptions import UnexpectedAlertPresentException  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys      

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Update path with retrieving from online instead?
# PATH = "/Users/sean-murray/Desktop/wikipedia-speedruns/env/lib/python3.8/site-packages/seleniumbase/drivers/chromedriver"

# Game does not allow you to play prompt of the day if you are not logged in
def test_prompt_of_day_no_login():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    WebDriverWait(driver, 10)
    # open page
    driver.get("https://wikispeedruns.com/")
    driver.maximize_window()
    driver.implicitly_wait(20)   

    #start run
    play_button = driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div[1]/div/div[1]/table/tbody/tr/td[1]/a")
    play_button.click()
    driver.implicitly_wait(20)

    # assert that prompt of day doesnt allow you to play if youre not logged in
    alert = driver.switch_to.alert
    assert "You must be logged in to play this rated prompt" in alert.text
    alert.accept()
    driver.implicitly_wait(20)

    # check if reroutes you back to home page
    assert driver.current_url == 'https://wikispeedruns.com/'
    driver.quit()

# testing login capability
def test_login():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    WebDriverWait(driver, 10)
    driver.get("https://wikispeedruns.com/")
    driver.maximize_window()
    driver.implicitly_wait(20)

    # click login button to go to login page
    login = driver.find_element(By.LINK_TEXT, "Login")
    login.click()
    driver.implicitly_wait(20)

    # ensure on the right page
    assert driver.current_url == 'https://wikispeedruns.com/login'
    usrnm = driver.find_element(By.ID, "login")
    pswd = driver.find_element(By.ID, "password")
    usrnm.send_keys('testcase')
    pswd.send_keys('password')

    # login
    driver.find_element(By.XPATH, "/html/body/div/div/div/form/button").click()
    driver.implicitly_wait(20)
    WebDriverWait(driver, 5).until(
        lambda driver: driver.current_url == "https://wikispeedruns.com/")
    # check to see back on homepage
    assert driver.current_url == 'https://wikispeedruns.com/'
    # check to see if logged in
    assert driver.find_element(By.XPATH, "/html/body/nav/div/div/ul/li[1]/a").text == 'testcase'
    driver.quit()

# once logged in, should be able to play prompt of the day
def test_play_after_login():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #login
    WebDriverWait(driver, 10)
    driver.get("https://wikispeedruns.com/")
    driver.maximize_window()
    driver.implicitly_wait(20)
    login = driver.find_element(By.LINK_TEXT, "Login")
    login.click()
    driver.implicitly_wait(20)
    assert driver.current_url == 'https://wikispeedruns.com/login'
    usrnm = driver.find_element(By.ID, "login")
    pswd = driver.find_element(By.ID, "password")
    usrnm.send_keys('testcase')
    pswd.send_keys('password')
    driver.find_element(By.XPATH, "/html/body/div/div/div/form/button").click()
    driver.implicitly_wait(20)
    WebDriverWait(driver, 5).until(
        lambda driver: driver.current_url == "https://wikispeedruns.com/")
    driver.implicitly_wait(40)    
    #play
    play_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[3]/div[1]/div/div[1]/table/tbody/tr/td[1]/a")))
    play_button.click()
    driver.implicitly_wait(20)
    driver.find_element(By.ID, "start-btn").click()
    driver.implicitly_wait(30)
    WebDriverWait(driver, 30)
    # checking if able to play by seeing if the game is in rated mode or in practice mode, either is valid
    try:
        WebDriverWait(driver, 30)
        mode = driver.find_element(By.CLASS_NAME, "text-danger")
        assert mode.text == 'Rated'
    except NoSuchElementException:
        driver.implicitly_wait(30)
        WebDriverWait(driver, 30)
        mode = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/b")))
        #assert mode.text == "Practice"
    driver.quit()

# command find shows warning but does not reset progress
def test_cmmd_f():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    WebDriverWait(driver, 10)
    driver.get("https://wikispeedruns.com/play/76")
    driver.maximize_window()
    driver.implicitly_wait(40)
    driver.find_element(By.ID, "start-btn").click()
    driver.implicitly_wait(20)
    WebDriverWait(driver, 10)
    # ensure we are on wiki page so pressing command find will trigger alert
    assert driver.find_element(By.XPATH, "/html/body/div/div/div/div[4]/div[1]/div[1]/h1/i").text == 'Chickering'
    # press command find
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('F').key_up(Keys.COMMAND).perform()
    driver.implicitly_wait(20)
    # check if alert popped up and content
    alert = driver.switch_to.alert
    assert "WARNING: Attempt to Find in page. This will be recorded." in alert.text
    alert.accept()
    driver.implicitly_wait(20)
    # ensure we stay on same page, should not reset run
    assert driver.current_url == 'https://wikispeedruns.com/play/76'
    driver.quit()

# pressing back will reset run
def test_back_ends_run():
    opt = webdriver.ChromeOptions().add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)
    # open a game
    driver.get("https://wikispeedruns.com/play/76")
    driver.maximize_window()
    driver.implicitly_wait(40)
    driver.find_element(By.ID, "start-btn").click()
    driver.implicitly_wait(20)
    # check to make sure game has been started
    assert driver.find_element(By.XPATH, "/html/body/div/div/div/div[4]/div[1]/div[1]/h1/i").text == 'Chickering'
    # test a couple of links so we can later test back button isnt going just back one page
    driver.find_element(By.LINK_TEXT, "Chickering, Suffolk").click()
    driver.implicitly_wait(20)
    driver.find_element(By.LINK_TEXT, "United Kingdom").click()
    driver.implicitly_wait(40)
    # go back
    try:
        driver.back()
    except UnexpectedAlertPresentException:
        # sometimes chrome gives "are you sure you want to leave this page, changes wont be saved" alert
        # trying to accept that alert and move on
        driver.switch_to_window()
        WebDriverWait(driver, 15).until(ActionChains(driver).send_keys(Keys.RETURN).perform())
        # assert back button ends run
        WebDriverWait(driver, 30).until(
            lambda driver: driver.current_url == "https://wikispeedruns.com/")
        assert driver.current_url == 'https://wikispeedruns.com/'
    driver.quit()

# refreshing page keeps logged in
def test_refresh_holds_state():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #login
    driver.get("https://wikispeedruns.com/")
    driver.maximize_window()
    driver.implicitly_wait(20)
    login = driver.find_element(By.LINK_TEXT, "Login")
    login.click()
    driver.implicitly_wait(20)
    assert driver.current_url == 'https://wikispeedruns.com/login'
    usrnm = driver.find_element(By.ID, "login")
    pswd = driver.find_element(By.ID, "password")
    usrnm.send_keys('testcase')
    pswd.send_keys('password')
    driver.find_element(By.XPATH, "/html/body/div/div/div/form/button").click()
    driver.implicitly_wait(20)
    WebDriverWait(driver, 5).until(
        lambda driver: driver.current_url == "https://wikispeedruns.com/")
    driver.implicitly_wait(40)
    # refresh page
    driver.refresh()
    driver.implicitly_wait(20)
    # check if still logged in
    assert driver.find_element(By.XPATH, "/html/body/nav/div/div/ul/li[1]/a").text == 'testcase'
    driver.quit()

# hitting start now button starts game immediately
def test_start_now():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://wikispeedruns.com/play/76")
    driver.maximize_window()
    driver.implicitly_wait(40)
    driver.find_element(By.ID, "start-btn").click()
    driver.implicitly_wait(20)
    assert driver.find_element(By.XPATH, "/html/body/div/div/div/div[4]/div[1]/div[1]/h1/i").text == 'Chickering'
    driver.quit()

# waiting for countdown starts game
def test_wait_start():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://wikispeedruns.com/play/76")
    driver.maximize_window()
    WebDriverWait(driver, 10)    
    driver.implicitly_wait(20)
    assert driver.find_element(By.XPATH, "/html/body/div/div/div/div[4]/div[1]/div[1]/h1/i").text == 'Chickering'
    driver.quit()

# testing a successful run from start to finish
def test_successful_run():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://wikispeedruns.com/play/76")
    driver.maximize_window()
    driver.implicitly_wait(40)
    driver.find_element(By.ID, "start-btn").click()
    driver.implicitly_wait(20)
    assert driver.find_element(By.XPATH, "/html/body/div/div/div/div[4]/div[1]/div[1]/h1/i").text == 'Chickering'
    driver.find_element(By.LINK_TEXT, "Chickering, Suffolk").click()
    driver.implicitly_wait(20)
    driver.find_element(By.LINK_TEXT, "United Kingdom").click()
    driver.implicitly_wait(40)
    driver.execute_script("arguments[0].click();", driver.find_element(By.LINK_TEXT, "Europe"))
    driver.implicitly_wait(20)
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "/html/body/div/div/div/div[4]/div[1]/div[2]/table[3]/tbody/tr[42]/td[3]/a"))    
    driver.implicitly_wait(20)
    assert 'You found it!' in driver.page_source
    driver.quit()

# hovering over a link gives little excerpt on it
def test_hover_article():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://wikispeedruns.com/play/76")
    driver.maximize_window()
    driver.implicitly_wait(40)
    driver.find_element(By.ID, "start-btn").click()
    driver.implicitly_wait(20)
    txt = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Arthur M. Chickering")))
    ActionChains(driver).move_to_element(txt).perform()
    popup = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "tooltip-container")))
    assert popup.text == "Arthur Merton Chickering was a U.S. arachnologist."
    driver.quit()