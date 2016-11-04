#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url_main = 'http://myscore.ru'
url_match = 'http://www.myscore.ru/match/{0}/#match-summary'

driver = webdriver.PhantomJS()
driver.set_window_size(1280, 1024)
driver.get('http://myscore.ru')
driver.save_screenshot('myscore.png')
elements = driver.find_elements_by_xpath('//tr[@class="tr-first stage-scheduled"]')
# print(elements)
ids = []
for el in elements:
	id_text = el.get_attribute('id')
	ids.append(id_text.split('_')[2])
print(ids)
for id in ids:
	driver.get(url_match.format(id))
	element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@id="a-match-head-2-head"]')))
	element.click()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Итого"]')))
	scores = filter((lambda score: score), map((lambda el: el.text), driver.find_elements_by_xpath('//span[@class="score"]/strong')))
	driver.save_screenshot('{0}.png'.format(id))
	print(driver.title)
	print(scores)
driver.close()