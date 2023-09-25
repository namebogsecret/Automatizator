#/src/webdriver/scroll.py
from random import randint
from time import sleep
from logging import getLogger
from log_scripts.set_logger import set_logger

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def scroll_down(driver, times = 1, height = 4000000):
    logger.info('Started scrolling %s times', times)
    for i in range(1, times):
        driver.execute_script(f"window.scrollTo(0, {height});")
        sleep(1)
        logger.debug('Scrolled down %s times', i)
    logger.info('Scrolled down %s times', times)
    


"""import requests

cookies = {
    'auth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTAxMDE0NiIsInVzZXJfdHlwZSI6InByZXAiLCJhdXRoX3VzZXJfaWQiOiI0MTQ1MTYyMSIsImp0aSI6ImVjODc5ZDk2ZDgzYzY4OTg5ZGZmZDRkNjZhNjc1MzZiIiwiZXhwIjoxNjkxMTQ1OTcxLCJhdWQiOlsiYmFja29mZmljZSIsIndhcnAiXX0.OOYFpJBkTDlF7YQKztkKv_sGkgux53dbyZjSazI200Q',
    'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoX3VzZXJfaWQiOiI0MTQ1MTYyMSIsImV4cCI6MTY5MzczNDM3MSwianRpIjoiZWM4NzlkOTZkODNjNjg5ODlkZmZkNGQ2NmE2NzUzNmIiLCJhdWQiOlsiYmFja29mZmljZSIsIndhcnAiXX0.obQ-AHd1Aan09Go7i0J-yAtC4dxBATpwLARaun549ac',
    'board_search_id': '5ca8c928-0347-a078-b952-ed636122261e',
    'board_search_dt': '1691143404',
    'board_with_filters': '1',
    'sc_mktc': '%5B%22%5C%2F%22%2C%22%22%2C1691116478%5D',
    'uid': '99BABAB9BE63CC6489A17F0102C69009',
    '_ga': 'GA1.2.541354441.1691116482',
    '_gid': 'GA1.2.1589376560.1691116482',
    '_ym_uid': '1691116482955925195',
    '_ym_d': '1691116482',
    'ml_mrm': '1',
    '_ym_isad': '2',
    'prfr_egback_sent': '1',
    '_gcl_au': '1.1.1771437061.1691116540',
    'intercom-id-bx6ssdy0': '2cc78e89-f3d2-49bb-a7f5-8c39fddcdec5',
    'intercom-session-bx6ssdy0': '',
    'intercom-device-id-bx6ssdy0': '6ec9ca54-dda8-4b97-b163-de4a85589406',
    '_ym_visorc': 'w',
    'egback': 'PodlevskihVN',
    'npsBanner_PodlevskihVN': '4',
    'prfr_bo_tkn': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiZnVsbCIsInZlcnNpb24iOjEsImlkIjoiN2QwNmM2Y2UtOTFkYy00ZDViLWFiZWMtNGE4NGU5MWQxNGU3Iiwic3RhdHVzIjoidG91Y2hlZCIsInNlc3Npb25JZCI6IjkyZjYxMzc2LTVjNWYtNDdmMy1hYWExLTRlMjJlMDgyZGMxMCIsImFjY291bnRJZCI6ODYwMDU2NSwicm9sZXMiOnsiY3VzdG9tZXIiOm51bGwsImltcGxlbWVudGVyIjoiUG9kbGV2c2tpaFZOIiwiaW1wbGVtZW50ZXJQaWQiOiIxMDEwMTQ2In0sImlhdCI6MTY5MTE0Mjk4OSwiZXhwIjoxNjkxMTQzNTg5LCJqdGkiOiI3ZDA2YzZjZS05MWRjLTRkNWItYWJlYy00YTg0ZTkxZDE0ZTcifQ.IHFwTJt7X1_yc-UO4bvhUgrhlhnmxBmua76XTIItmS0',
    'VRID': '4-1',
    'sid': 'ubq6mGTMzOBluNGwCVb3Ag==',
    'sc_crf': 'https%3A%2F%2Frepetitors.info%2F',
    'sc_ltime': '1691143399.908',
    '_ga_3WXCQPX0FF': 'GS1.2.1691142260.2.1.1691143400.0.0.0',
    'pbo_save_ts': '1691143402',
    '_ga_QZ48JJKG5W': 'GS1.2.1691142264.2.1.1691143404.60.0.0',
}

headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryd8Bu6wTK56pdHirA',
    'Origin': 'https://repetitors.info',
    'Referer': 'https://repetitors.info/backoffice/n.php',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'x-app-id': 'BO',
    'x-new-auth-compatible': '1',
}

data = {
  '$------WebKitFormBoundaryd8Bu6wTK56pdHirA\\r\\nContent-Disposition: form-data; name': '"request"\\r\\n\\r\\n{"meta":{"ui_type":"WEB","ui_app":"MOBWEBBO","ui_ver":"1","ui_os":"0.0","method":"findOrders"},"data":{"searchId":"644101","allVerticals":true,"searchQuery":"","useSavedFilter":true,"nextCursor":"WzcwLDE2OTA5ODI2NTAsNTQ5NDE3MTJd","pageSize":10}}\\r\\n------WebKitFormBoundaryd8Bu6wTK56pdHirA--\\r\\n'
}

response = requests.post('https://repetitors.info/backoffice/api/', headers=headers, cookies=cookies, data=data)
crhjkbyu pfrfpj
"""