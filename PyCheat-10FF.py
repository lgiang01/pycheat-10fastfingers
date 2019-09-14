from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import json, time

def dispatchKeyEvent(driver, name, options = {}):
    options["type"] = name
    body = json.dumps({'cmd': 'Input.dispatchKeyEvent', 'params': options})
    resource = "/session/%s/chromium/send_command" % driver.session_id
    url = driver.command_executor._url + resource
    driver.command_executor._request('POST', url, body)

def holdKeyW(driver, duration):
    endtime = time.time() + duration
    options = { \
      "code": "Space",
      "key": " ",
      "text": " ",
      "unmodifiedText": " ",
      "nativeVirtualKeyCode": ord(" "),
      "windowsVirtualKeyCode": ord(" ")
    }

    while True:
        dispatchKeyEvent(driver, "rawKeyDown", options)
        dispatchKeyEvent(driver, "char", options)

        if time.time() > endtime:
          dispatchKeyEvent(driver, "keyUp", options)
          break

        options["autoRepeat"] = True
        time.sleep(0.01)

browser = Chrome()
browser.get('https://10fastfingers.com/typing-test/thai')
words_list_loc = "words"

type_form_loc = "inputfield"
type_form = browser.find_element_by_id(type_form_loc) 

lst_words = browser.execute_script("return words;")

time.sleep(15)
starttime = time.time()
for _ in range(len(lst_words)):
    type_form.send_keys(lst_words[_])
    holdKeyW(browser, 0.05)
    if time.time() - starttime >= 65:
      break
    pass
