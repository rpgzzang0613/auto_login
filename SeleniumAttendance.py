from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from PIL import Image
import pytesseract
import io
import platform
import util

class SeleniumAttendance:
    
    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--headless=new")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_experimental_option("detach", True)
        # options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(options=options)
        
        self.driver.implicitly_wait(10)
        
    def go_daewon(self, id, pw):
        succeed = False
    
        driver_ = self.driver
    
        driver_.get("https://www.daewonshop.com")
        print("- 대원샵 메인 진입 -", flush=True)
        msg_for_return = "- 대원샵 메인 진입 -\n"

        main_popup = driver_.find_element(By.ID, "main-layer-popup")

        if "active" in main_popup.get_attribute("class"):
            main_popup.find_elements(By.CSS_SELECTOR, "a.close")[0].click()
            print("대원샵 팝업 닫음", flush=True)
            msg_for_return += "대원샵 팝업 닫음\n"

        try:
            login_btn = driver_.find_element(By.CSS_SELECTOR, "ul.member-wrap #btn-login")
        except NoSuchElementException:
            login_btn = None

        if login_btn is not None:
            login_btn.click()
            print("대원샵 로그인창 오픈", flush=True)
            msg_for_return += "대원샵 로그인창 오픈\n"
            
            root_handle = driver_.current_window_handle
            
            for handle in driver_.window_handles:
                if handle != root_handle:
                    driver_.switch_to.window(handle)
                    break

            driver_.find_element(By.CSS_SELECTOR, "input.id").send_keys(id)
            driver_.find_element(By.CSS_SELECTOR, "input.pw").send_keys(pw)
            driver_.find_element(By.ID, "m-login").click()
            print("대원샵 로그인 완료", flush=True)
            msg_for_return += "대원샵 로그인 완료\n"
            
            driver_.switch_to.window(root_handle)

        driver_.get("https://www.daewonshop.com/cs/attend")
        print("대원샵 출석체크 페이지 진입", flush=True)
        msg_for_return += "대원샵 출석체크 페이지 진입\n"

        try:
            dw_check_btn = WebDriverWait(driver_, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".attendance-check-btn")))
            dw_check_btn.click()
            print("대원샵 출석체크 버튼 찾아서 클릭", flush=True)
            msg_for_return += "대원샵 출석체크 버튼 찾아서 클릭\n"
        except NoSuchElementException:
            dw_check_btn = None
            print("대원샵 출석체크 버튼 찾기 실패 (NoSuchElementException)", flush=True)
            msg_for_return += "대원샵 출석체크 버튼 찾기 실패 (NoSuchElementException)\n"
        except TimeoutException:
            dw_check_btn = None
            print("대원샵 출석체크 버튼 찾기 실패 (TimeoutException)", flush=True)
            msg_for_return += "대원샵 출석체크 버튼 찾기 실패 (TimeoutException)\n"

            page_logs = driver_.get_log('browser')
            with open("page_console_log.txt", "w", encoding="utf-8") as log_file:
                for log in page_logs:
                    log_file.write(f"{log['level']} - {log['message']}\n")

            page_screenshot = driver_.save_screenshot("page_screenshot.png")
            
            page_html = driver_.page_source
            with open("page_source.html", "w", encoding="utf-8") as html_file:
                html_file.write(page_html)

        if dw_check_btn is None:
            succeed = False
            return {"succeed": succeed, "msg_for_return": msg_for_return}

        modal_content = WebDriverWait(driver_, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.dpromotion-modal-content")))

        try:
            modal_form = modal_content.find_element(By.CSS_SELECTOR, "form")
        except NoSuchElementException:
            modal_form = None
        except TimeoutException:
            modal_form = None

        if modal_form is not None:
            # form이 있으면 동의 체크 후 클릭하고 변경된 모달로 재할당
            modal_content = driver_.find_element(By.CSS_SELECTOR, "section.dpromotion-modal-content")
            modal_content.find_element(By.CSS_SELECTOR, ".dpromotion-agreement__item-title").click()
            modal_content.find_element(By.CSS_SELECTOR, ".dpromotion-modal__button.confirm").click()
            modal_content = driver_.find_element(By.CSS_SELECTOR, "section.dpromotion-modal-content")

        try:
            result_msg = modal_content.find_element(By.CSS_SELECTOR, ".dpromotion-alert__message").text
        except NoSuchElementException:
            result_msg = modal_content.text
        
        print("대원샵 출석체크 결과 :", result_msg, flush=True)
        msg_for_return += "대원샵 출석체크 결과 : " + result_msg + "\n"
        
        driver_.find_element(By.CSS_SELECTOR, "button.dpromotion-modal-close").click()
        print("- 대원샵 완료 -", flush=True)
        msg_for_return += "- 대원샵 완료 -\n"
        succeed = True
        
        return {"succeed": succeed, "msg_for_return": msg_for_return}
        
        
    def __try_captcha(self):
        driver_ = self.driver
        
        msg = ""
        succeed = False
        
        for i in range(15):
            print(str(i+1) + "번째 시도..", flush=True)
            msg += str(i+1) + "번째 시도..\n"
            
            try:
                btn = driver_.find_element(By.CSS_SELECTOR, "#attendWriteForm span.gRight a")
            except NoSuchElementException:
                btn = None
            
            if btn is None:
                print("소프라노몰 이미 출석체크를 해서 버튼이 없음", flush=True)
                msg += "소프라노몰 이미 출석체크를 해서 버튼이 없음\n"
                succeed = True
                return {"succeed": succeed, "msg": msg}
            
            btn.click()
            
            print("Captcha 모달 오픈", flush=True)
            msg += "Captcha 모달 오픈\n"
            
            captcha_img = driver_.find_element(By.CSS_SELECTOR, ".attendSecurityLayer p.form img")
            secure_input = driver_.find_element(By.CSS_SELECTOR, ".attendSecurityLayer #secure_text")
            
            img_byte = captcha_img.screenshot_as_png
            
            original_img = Image.open(io.BytesIO(img_byte))
            print("오리지널 이미지 get", flush=True)
            msg += "오리지널 이미지 get\n"
            
            new_img = util.convert_image(original_img)
            print("추출이 쉬운 이미지로 가공 완료", flush=True)
            msg += "추출이 쉬운 이미지로 가공 완료\n"
            
            if platform.system() == "Darwin":
                pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
            elif platform.system() == "Windows":
                pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"
            elif platform.system() == "Linux":
                pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
            
            # 개행문자 제거.. 왜 개행문자가 들어가는지 아직도 모름
            captcha_str = pytesseract.image_to_string(image=new_img, lang="eng").replace("\n", "")
            
            print("문자열 추출 :", captcha_str, flush=True)
            msg += "문자열 추출 : " + captcha_str + "\n"
            
            secure_input.send_keys(captcha_str)
            
            # 사실 개행문자 안뺀채로 클릭을 없애도 되긴 함
            driver_.find_elements(By.CSS_SELECTOR, ".attendSecurityLayer .btnArea a")[0].click()
            print("출석체크 버튼 클릭", flush=True)
            msg += "출석체크 버튼 클릭\n"

            try:
                alert_window = driver_.switch_to.alert
            except NoAlertPresentException:
                print("얼럿 창 못찾아서 두번째 시도..", flush=True)
                msg += "얼럿 창 못찾아서 두번째 시도..\n"
                try:
                    alert_window = WebDriverWait(driver_, 10).until(EC.alert_is_present())
                except NoAlertPresentException:
                    alert_window = None
                    print("얼럿 창 찾기 두번째 시도까지 실패", flush=True)
                    msg += "얼럿 창 찾기 두번째 시도까지 실패"
                except TimeoutException:
                    print("얼럿 창 찾기 두번째 시도 시간 초과", flush=True)
                    msg += "얼럿 창 찾기 두번째 시도 시간 초과"

            if alert_window is None:
                succeed = False
                return {"succeed": succeed, "msg": msg}

            print("소프라노몰 출석체크 결과 : ", alert_window.text, flush=True)
            msg += "소프라노몰 출석체크 결과 : " + alert_window.text + "\n"
            
            alert_window.accept()
            
            try:
                after_btn = driver_.find_element(By.CSS_SELECTOR, "#attendWriteForm span.gRight a")
            except NoSuchElementException:
                after_btn = None
                
            if after_btn is None:
                succeed = True
                break
        
        return {"succeed": succeed, "msg": msg}
    
    def go_sofrano(self, id, pw):
        driver_ = self.driver
        
        driver_.get("https://sofrano.com/attend/stamp.html")
        print("- 소프라노몰 출석체크 페이지 진입 -", flush=True)
        msg_for_return = "- 소프라노몰 출석체크 페이지 진입 -\n"
        
        driver_.switch_to.alert.accept()

        driver_.find_element(By.ID, "member_id").send_keys(id)
        driver_.find_element(By.ID, "member_passwd").send_keys(pw)
        driver_.find_element(By.CSS_SELECTOR, "a.loginBtn").click()
        print("소프라노몰 로그인 완료", flush=True)
        msg_for_return += "소프라노몰 로그인 완료\n"
        
        res_dict = self.__try_captcha()
        msg_for_return += res_dict["msg"]
        
        return {"succeed": res_dict["succeed"], "msg_for_return": msg_for_return}
    
    def quit_driver(self):
        self.driver.quit()