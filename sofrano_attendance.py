from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from PIL import Image
import time
import pytesseract
import io
import util

def try_captcha(driver: WebDriver):
    msg = ""
    succeed = False
    
    for i in range(10):
        print(str(i+1) + "번째 시도..")
        msg += str(i+1) + "번째 시도..\n"
        
        time.sleep(2)
        
        try:
            btn = driver.find_element(By.CSS_SELECTOR, "#attendWriteForm span.gRight a")
        except NoSuchElementException:
            btn = None
        
        if btn is None:
            print("소프라노몰 이미 출석체크를 해서 버튼이 없음")
            msg += "소프라노몰 이미 출석체크를 해서 버튼이 없음\n"
            succeed = True
            return {"succeed": succeed, "msg": msg}
        
        btn.click()
        
        print("Captcha 모달 오픈")
        msg += "Captcha 모달 오픈\n"
        
        captcha_img = driver.find_element(By.CSS_SELECTOR, ".attendSecurityLayer p.form img")
        secure_input = driver.find_element(By.CSS_SELECTOR, ".attendSecurityLayer #secure_text")
        
        img_byte = captcha_img.screenshot_as_png
        
        original_img = Image.open(io.BytesIO(img_byte))
        time.sleep(1)
        print("오리지널 이미지 get")
        msg += "오리지널 이미지 get\n"
        
        new_img = util.convert_image(original_img)
        print("추출이 쉬운 이미지로 가공 완료")
        msg += "추출이 쉬운 이미지로 가공 완료\n"
        
        pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
        captcha_str = pytesseract.image_to_string(new_img)
        print("문자열 추출 :", captcha_str)
        msg += "문자열 추출 : " + captcha_str + "\n"
        
        secure_input.send_keys(captcha_str)
        
        try:
            driver.find_element(By.CSS_SELECTOR, ".attendSecurityLayer .btnArea a")[0].click()
        except Exception:
            print("왜 UnexpectedAlert이 뜨는지 모르겠지만 예외로 빠짐")
            print("출석체크 버튼 클릭")
            msg += "출석체크 버튼 클릭\n"
            
            try:
                driver.switch_to.alert.accept()
            except Exception:
                print("마찬가지로 왜 NoSuchAlert이 뜨는지 모르겠지만 예외로 빠짐")
            
            time.sleep(2)
            
            try:
                after_btn = driver.find_element(By.CSS_SELECTOR, "#attendWriteForm span.gRight a")
            except NoSuchElementException:
                after_btn = None
            
            if after_btn is None:
                succeed = True
                break
    
    return {"succeed": succeed, "msg": msg}

def go_attendance(id, pw, driver: WebDriver):
    driver.get("https://sofrano.com/attend/stamp.html")
    print("- 소프라노몰 출석체크 페이지 진입 -")
    msg_for_return = "- 소프라노몰 출석체크 페이지 진입 -\n"
    time.sleep(1)
    
    driver.switch_to.alert.accept()
    time.sleep(2)

    driver.find_element(By.ID, "member_id").send_keys(id)
    driver.find_element(By.ID, "member_passwd").send_keys(pw)
    driver.find_element(By.CSS_SELECTOR, "a.loginBtn").click()
    print("소프라노몰 로그인 완료")
    msg_for_return += "소프라노몰 로그인 완료\n"
    time.sleep(2)
    
    res_dict = try_captcha(driver)
    msg_for_return += res_dict["msg"]
    
    return {"succeed": res_dict["succeed"], "msg_for_return": msg_for_return}