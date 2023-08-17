#!/Users/bsho88_office/project/no_java_project/py_test/auto_login/.venv/bin/python

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
    
    id = os.getenv("DAEWON_ID")
    pw = os.getenv("DAEWON_PW")
    
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    # options.add_experimental_option("detach", True)
    # options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    
    daewon_res_dict = daewon_attendance.go_attendance(id, pw, driver)
    msg_for_slack += daewon_res_dict["msg_for_return"]
    
    id = os.getenv("SOFRANO_ID")
    pw = os.getenv("SOFRANO_PW")
    
    sofrano_res_dict = sofrano_attendance.go_attendance(id, pw, driver)
    msg_for_slack += sofrano_res_dict["msg_for_return"]
    
    driver.quit()
    print("- - 완료 - -")
    msg_for_slack += "- - 완료 - -\n"
    
    msg_for_slack += "결과 : "
    print(daewon_res_dict["succeed"], sofrano_res_dict["succeed"])
    
    if daewon_res_dict["succeed"]:
        msg_for_slack += "대원 성공, "
    else:
        msg_for_slack += "대원 실패, "
    
    if sofrano_res_dict["succeed"]:
        msg_for_slack += "소프라노 성공\n"
    else:
        msg_for_slack += "소프라노 실패\n"
    
    util.send_slack_msg(msg_for_slack)
except Exception as e:
    print("예외 발생", e)
    util.send_slack_msg(str(e))
