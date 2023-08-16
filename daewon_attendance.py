from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def go_attendance(id, pw, driver: WebDriver):
    succeed = False
    
    driver.get("https://www.daewonshop.com")
    print("- 대원샵 메인 진입 -")
    msg_for_return = "- 대원샵 메인 진입 -\n"
    time.sleep(2)

    main_popup = driver.find_element(By.ID, "main-layer-popup")

    if "active" in main_popup.get_attribute("class"):
        main_popup.find_elements(By.CSS_SELECTOR, "a.close")[0].click()
        print("대원샵 팝업 닫음")
        msg_for_return += "대원샵 팝업 닫음\n"

    time.sleep(1)

    try:
        login_btn = driver.find_element(By.CSS_SELECTOR, "ul.member-wrap #btn-login")
    except NoSuchElementException:
        login_btn = None

    if login_btn is not None:
        login_btn.click()
        print("대원샵 로그인창 오픈")
        msg_for_return += "대원샵 로그인창 오픈\n"
        time.sleep(1)
        
        root_handle = driver.current_window_handle
        
        for handle in driver.window_handles:
            if handle != root_handle:
                driver.switch_to.window(handle)
                break

        driver.find_element(By.CSS_SELECTOR, "input.id").send_keys(id)
        driver.find_element(By.CSS_SELECTOR, "input.pw").send_keys(pw)
        driver.find_element(By.ID, "m-login").click()
        print("대원샵 로그인 완료")
        msg_for_return += "대원샵 로그인 완료\n"
        
        driver.switch_to.window(root_handle)

    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, "a.attendcheck").click()
    print("대원샵 출석체크 페이지 진입")
    msg_for_return += "대원샵 출석체크 페이지 진입\n"
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, "button.attendance-check-btn").click()
    time.sleep(2)
    
    result_content = driver.find_element(By.CSS_SELECTOR, "section.dpromotion-modal-content")
    
    try:
        result_msg = result_content.find_element(By.CSS_SELECTOR, ".dpromotion-alert__message").text
    except NoSuchElementException:
        result_msg = result_content.text
    
    print("대원샵 출석체크 결과 :", result_msg)
    msg_for_return += "대원샵 출석체크 결과 : " + result_msg + "\n"
    time.sleep(2)
    
    driver.find_element(By.CSS_SELECTOR, "button.dpromotion-modal-close").click()
    print("- 대원샵 완료 -")
    msg_for_return += "- 대원샵 완료 -\n"
    succeed = True
    
    return {"succeed": succeed, "msg_for_return": msg_for_return}