import asyncio
import time
import random
from tkinter import BROWSE
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
error=""
async def start(id,password): 
  options = webdriver.ChromeOptions()
  options.add_experimental_option("excludeSwitches", ["enable-logging"])
  #options.add_argument("--auto-open-devtools-for-tabs");
  browser = webdriver.Chrome("C:/driver/chromedriver.exe",options=options)
  browser.get("https://www.benedu.co.kr/")
  browser.find_element(By.ID,"loginID").send_keys(id)
  browser.find_element(By.ID,"loginPW").send_keys(password)
  browser.find_element(By.XPATH,"/html/body/section/div[2]/div[2]/form/div/div[5]/button[1]").click()
  await asyncio.sleep(2)
  #sidebar = browser.find_element(By.XPATH,r'//*[@id="menu-toggler"]')
  #sidebar.click()
  try:
    browser.find_element(By.XPATH,r"//*[@id='sidebar']/div[1]/div[1]/div/ul/li[4]").click()
  except Exception as error:
    return "아이디 혹은 비밀번호가 잘못됐습니다."
  await asyncio.sleep(1)
  browser.find_element(By.LINK_TEXT,"학습과제").click()
  개수=len(browser.find_element(By.XPATH,r'//*[@id="TaskList-table"]/tbody').find_elements(By.TAG_NAME,"tr"))
  if 개수==0:
    return "학습과제가 없습니다."
  for i in range(1,개수+1):
    if i != 1:
      browser.find_element(By.LINK_TEXT,"학습과제").click()
    browser.find_element(By.XPATH,rf'//*[@id="TaskList-table"]/tbody/tr[{i}]').click()
    await asyncio.sleep(1)
    try:
      browser.find_element(By.XPATH,r'//*[@id="TestDetail-table"]/tbody/tr/td[3]/div').click()
    except:
      browser.find_element(By.XPATH,r'//*[@id="TestDetail-table"]/tbody/tr/td[4]/div').click()
    await asyncio.sleep(3)
    ans=browser.execute_async_script(
      """(async () => {
    const m = location.search.match(/id=(.*)&value=(.*)&type=(.*)/).map(v => decodeURI(v));

    const gettime= document.getElementsByClassName('badge pull-right')[0].innerText.split(' ')[3].split(':');
    const timeout= Number(gettime[0])*60000+Number(gettime[1]*1000);

    const fd = new FormData();
    fd.append('values[0][value]', m[1]);
    fd.append('values[0][detailvalue]', m[2]);
    fd.append('type', m[3]);

    const res = await fetch(location.origin + "/Utils/TestDetailPrint", {method: "POST", body: fd})
    const data = await res.text();
    const d = JSON.parse(data);

    const answers = d.Table01.map(v => v.QST_CORRECT); // (string | null)[]
    const badges = document.querySelectorAll("#Answer .badge");
    let inputs = 0;
    let a=0;
    for (let j = 0, questionNum = 0; questionNum < 5; questionNum++) {  
        if (badges[j].attributes["num"].value === 'X') {
            document.querySelectorAll("#Answer input")[inputs].value = answers[questionNum];
            inputs++;
            j++;
        } else {
            badges[j + Number(answers[questionNum]) - 1].click()
            console.log(badges[j+Number(answers[questionNum])-1].value)
            j += 6;
        }
    }
    
})();""")
    print(ans)
    #r= random.randint(180,240)
    #time.sleep(r)
    #browser.find_element(By.XPATH,r'//*[@id="main-container"]/div[2]/div/div[2]/div/div/div[4]/div[2]/div[2]/div[2]/div[2]/a').click()

#        setTimeout(()=> {document.getElementsByClassName('btn btn-primary btn-block')[0].click()}, timeout);
