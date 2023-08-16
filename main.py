from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import daewon_attendance
import sofrano_attendance
import util
import dotenv
import os

try:
    print("- - 시작 - -")
    msg_for_slack = "- - 시작 - -\n"

    dotenv.load_dotenv()
    
    id = os.getenv("ID")
    pw = os.getenv("PW")
    
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    # options.add_experimental_option("detach", True)
    # options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    
    daewon_res_dict = daewon_attendance.go_attendance(id, pw, driver)
    msg_for_slack += daewon_res_dict["msg_for_return"]
    
    sofrano_res_dict = sofrano_attendance.go_attendance(id, pw, driver)
    msg_for_slack += sofrano_res_dict["msg_for_return"]
    
    driver.quit()
    print("- - 완료 - -")
    msg_for_slack += "- - 완료 - -"
    
    print(daewon_res_dict["succeed"], sofrano_res_dict["succeed"])
    
    util.send_slack_msg(msg_for_slack)
except Exception as e:
    print("예외 발생", e)
    util.send_slack_msg(str(e))
