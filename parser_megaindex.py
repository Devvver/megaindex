from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import csv

# Устанавливаем заголовок User-Agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

# Создаем экземпляр ChromeOptions
chrome_options = webdriver.ChromeOptions()

# Устанавливаем User-Agent в ChromeOptions
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument(f"user-agent={user_agent}")

# Запускаем браузер с заданными опциями
driver = webdriver.Chrome(options=chrome_options)

driver.maximize_window()



def parsing_site(driver, site):
    try:
        driver.get('https://ru.megaindex.com/backlinks/' + site)
        sleep(20)

        # Находим элементы
        link_element = driver.find_element(By.ID, 'total_self_domains')
        total_self_uniq_links = driver.find_element(By.ID, 'total_self_uniq_links')
        trust_dr_rank = driver.find_elements(By.CLASS_NAME, 'drchart-text')
        chart_element = driver.find_element(By.ID, 'chart_yaca')
        text_elements = chart_element.find_elements(By.TAG_NAME, 'text')

        # Печатаем значения, чтобы убедиться, что элементы присутствуют
        print(f"Домены: {link_element.text}")
        print(f"Ссылки: {total_self_uniq_links.text}")

        # Проверяем, что trust_dr_rank не пуст и содержит хотя бы один элемент
        if trust_dr_rank:
            trust_rank_value = trust_dr_rank[0].text
            print(f"Trust rank: {trust_rank_value}")
        else:
            print("Trust rank не найден")

        if trust_dr_rank:
            dr_rank_values = trust_dr_rank[1].text
            print(f"DR rank: {dr_rank_values}")
        else:
            print("DR rank не найден")

        # Проверяем, что text_elements не пуст и содержит хотя бы один элемент
        if text_elements:
            themes = ' '.join([text_element.text for text_element in text_elements if text_element.text.strip()])


            print(f"Тематика: {themes}")
        else:
            print("DR rank и Тематика не найдены")

        # Создаем словарь
        my_dict = {
            'Домен': site,
            'Домены': link_element.text ,
            'Ссылки': total_self_uniq_links.text,
            'Trust Rank': trust_rank_value,
            'DR Rank': dr_rank_values,
            'Тематика': themes
        }

        # Выводим словарь
        print(my_dict)
        return my_dict

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        my_dict=None


# Создаем пустой список
site_data_list = []
all_site_data = []
# Открываем файл и читаем его построчно
with open('site.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # Добавляем строку в список
        site_data_list.append(line.strip())

# Выводим полученный список
print(site_data_list)




driver.get("https://ru.megaindex.com/auth/register")
sleep(20)
for mysite in site_data_list:
    site_data = parsing_site(driver, mysite)
    if site_data:
        all_site_data.append(site_data)

# Записываем данные в CSV после завершения цикла
with open('Сайты.csv', 'w', encoding='utf-8', newline='') as csvfile:
    # Задаем заголовки CSV
    fieldnames = ['Домен','Домены', 'Ссылки', 'Trust Rank', 'DR Rank', 'Тематика']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Записываем заголовки
    writer.writeheader()

    # Записываем данные из списка в CSV
    writer.writerows(all_site_data)




driver.quit()
