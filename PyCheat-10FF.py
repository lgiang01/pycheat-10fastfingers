from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import json, time

# Simulating keyDown and keyUp events for Space. Thanks, StackOverflow!

def dispatchKeyEvent(driver, name, options = {}):
    options["type"] = name
    body = json.dumps({'cmd': 'Input.dispatchKeyEvent', 'params': options})
    resource = "/session/%s/chromium/send_command" % driver.session_id
    url = driver.command_executor._url + resource
    driver.command_executor._request('POST', url, body)

def holdKeySpace(driver, duration):
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

#Starting Chromium and navigate to page

browser = Chrome()
browser.get('https://10fastfingers.com/typing-test/english')

#Locate the input field

type_form_loc = "inputfield"
type_form = browser.find_element_by_id(type_form_loc) 

# Get value of the "words" array, which, surprisingly, contains all the words needed

lst_words = browser.execute_script("return words;")

# Sleep for a few seconds. This is to prevent freezes when ads loads

time.sleep(10)

# Run for 65 seconds (Longer than duration of a test to make sure it doesn't stop too soon) then stop

starttime = time.time()
for _ in range(len(lst_words)):
    type_form.send_keys(lst_words[_])
    holdKeySpace(browser, 0.05)
    if time.time() - starttime >= 65:
      break
    pass
