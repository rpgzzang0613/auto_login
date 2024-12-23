#!/Users/bsho88_office/project/no_java_project/py_test/auto_login/.venv/bin/python

from SeleniumAttendance import SeleniumAttendance
import util
import dotenv
import os
import traceback

try:
    print("- - 시작 - -", flush=True)
    msg_for_slack = "- - 시작 - -\n"

    dotenv.load_dotenv()
    
    sa = SeleniumAttendance()
    
    daewon_res_dict = sa.go_daewon(os.getenv("DAEWON_ID"), os.getenv("DAEWON_PW"))
    msg_for_slack += daewon_res_dict["msg_for_return"]
    
    sofrano_res_dict = sa.go_sofrano(os.getenv("SOFRANO_ID"), os.getenv("SOFRANO_PW"))
    msg_for_slack += sofrano_res_dict["msg_for_return"]
    
    sa.quit_driver()
    
    print("- - 완료 - -", flush=True)
    msg_for_slack += "- - 완료 - -\n"
    
    msg_for_slack += "결과 : "
    print(daewon_res_dict["succeed"], sofrano_res_dict["succeed"], flush=True)
    
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
    print("예외 발생:", str(e), flush=True)
    trace_str = traceback.format_exc()
    
    # 로그에 예외 정보 및 작업 진행 상황 출력
    log_msg = f"예외 발생: {str(e)}\n"
    log_msg += f"진행 상황:\n{msg_for_slack}\n"
    log_msg += f"Traceback:\n{trace_str}"
    print(log_msg, flush=True)
    
    # Slack에 예외 정보 및 작업 진행 상황 전송
    util.send_slack_msg(log_msg)