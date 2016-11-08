#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url_main = 'http://myscore.ru'
url_match = 'http://www.myscore.ru/match/{0}/#match-summary'

game_result = u'{0} {1} {2} {3} : {4} {5}'

def parse_head_2_head_page(driver):
	game_rows = driver.find_elements_by_xpath('//tr[@class="odd highlight"] | //tr[@class="even highlight"]')
	for game_row in game_rows:
		date = game_row.find_element_by_class_name("date").text
		competition = game_row.find_element_by_class_name("flag_td").get_attribute("title")
		team_cells = game_row.find_elements_by_xpath('td[@class="name"] | td[@class="name highTeam"]')
		home_team = team_cells[0].find_element_by_xpath('span').text
		guest_team = team_cells[1].find_element_by_xpath('span').text
		score = game_row.find_element_by_xpath('td/span[@class="score"]/strong').text
		scores = score.split(':')
		home_score = 0
		guest_score = 0
		if len(scores) == 2:
			home_score = scores[0]
			guest_score = scores[1]
		else:
			print(u'Can\'t split score string {0}'.format(score))
		print(game_result.format(date, competition, home_team, home_score, guest_score, guest_team))

driver = webdriver.PhantomJS()
driver.set_window_size(1280, 1024)
driver.get('http://myscore.ru')
driver.save_screenshot('myscore.png')
elements = driver.find_elements_by_xpath('//div[@class="fs-table"]/div[@class="table-main"]/table/tbody/tr[@class="tr-first stage-scheduled" | @class=" stage-scheduled" | @class="even stage-scheduled"]')
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
	parse_head_2_head_page(driver)
	# scores = filter((lambda score: score), map((lambda el: el.text), driver.find_elements_by_xpath('//span[@class="score"]/strong')))
	driver.save_screenshot('{0}.png'.format(id))
	# print(driver.title)
	# print(scores)
driver.close()
