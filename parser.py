#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url_main = 'http://myscore.ru'
url_match = 'http://www.myscore.ru/match/{0}/#match-summary'

game_result = u'{0} {1} {2} {3} : {4} {5}'

def encode(unicode):
	return unicode.encode('utf-16')

def parse_game_row(row):
	date = row.find_element_by_class_name("date").text
	competition = row.find_element_by_class_name("flag_td").get_attribute("title")
	team_cells = row.find_elements_by_xpath('td[@class="name"] | td[@class="name highTeam"]')
	home_team = guest_team = 'Unknown'
	if len(team_cells) == 2:
		home_team = team_cells[0].find_element_by_xpath('span').text
		guest_team = team_cells[1].find_element_by_xpath('span').text
	score = row.find_element_by_xpath('td/span[@class="score"]/strong').text
	scores = score.split(':')
	home_score = 0
	guest_score = 0
	if len(scores) == 2:
		home_score = scores[0]
		guest_score = scores[1]
	else:
		print(u'Can\'t split score string {0}'.format(score))
	# print(game_result.format(date, competition, home_team, home_score, guest_score, guest_team))
	return {'date': date, 
			'competition': competition, 
			'home_team': home_team, 
			'guest_team': guest_team, 
			'home_score': home_score, 
			'guest_score': guest_score}

def parse_head_2_head_page(driver):
	stats = {'home team stats': [], 'guest team stats': [], 'mutual games stats': []}
	team_names = map((lambda el: el.text), driver.find_elements_by_xpath('//span[class="tname"]/a'))
	if len(team_names) == 2:
		stats['home team name'] = team_names[0]
		stats['guest team name'] = team_names[1]
	home_game_rows = driver.find_elements_by_xpath('//table[@class="head_to_head h2h_home"]/tbody/tr[@class="odd highlight" | @class="even highlight"]')
	guest_game_rows = driver.find_elements_by_xpath('//table[@class="head_to_head h2h_away"]/tbody/tr[@class="odd highlight" | @class="even highlight"]')
	mutual_game_rows = driver.find_elements_by_xpath('//table[@class="head_to_head h2h_mutual"]/tbody/tr[@class="odd highlight" | @class="even highlight"]')
	for game_row in home_game_rows[0:5]:
		stats['home team stats'].append(parse_game_row(game_row))
	for game_row in guest_game_rows[0:5]:
		stats['guest team stats'].append(parse_game_row(game_row))
	for game_row in mutual_game_rows[0:5]:
		stats['mutual games stats'].append(parse_game_row(game_row))
	return stats

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
for id in ids[0:5]:
	driver.get(url_match.format(id))
	element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@id="a-match-head-2-head"]')))
	element.click()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Итого"]')))
	stats = parse_head_2_head_page(driver)
	print(repr(stats).decode('unicode-escape'))
	# scores = filter((lambda score: score), map((lambda el: el.text), driver.find_elements_by_xpath('//span[@class="score"]/strong')))
	# driver.save_screenshot('{0}.png'.format(id))
	# print(driver.title)
	# print(scores)
driver.close()
