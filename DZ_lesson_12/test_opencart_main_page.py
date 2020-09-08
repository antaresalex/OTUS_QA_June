from functools import reduce
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import math
import operator


# Тестируем Главную /


# Тестируем сайт, что он связан с OpenCart
def test_example(browser, url, wait):
    # открываем главную
    browser.get(url)
    # перематываем страницу вниз до конца
    browser.find_element_by_css_selector('footer p a').send_keys(Keys.END)
    # browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="http://www.opencart.com"]')))
    assert element.text == 'OpenCart'


# Тест 1 открытия Privacy Policy
def test_click_privacy_policy(browser, url):
    # открываем главную
    browser.get(url)
    # перематываем страницу вниз до конца
    browser.find_element_by_css_selector('body footer div div div:nth-child(1) ul li:nth-child(3) a').send_keys(
        Keys.END)
    element = browser.find_element_by_css_selector('body footer div div div:nth-child(1) ul li:nth-child(3) a')
    element.click()
    new_pade_element = browser.find_element_by_css_selector('#content h1')
    assert new_pade_element.text == 'Privacy Policy'


# Тест 2 Featured Macbook открытия карточки с товаром по клику на картинку
def test_click_featured_picture(browser, url):
    # открываем главную
    browser.get(url)
    element = browser.find_element_by_css_selector('.product-layout .img-responsive')
    actions = ActionChains(browser)
    # перематываем страницу до элемента
    actions.move_to_element(element)
    # получаем название товара на Main Page из Featured
    name_element = browser.find_element_by_css_selector('.product-layout .caption a').text
    actions.perform()
    # кликаем на картинку Featured продукта
    element.click()
    # получаем название товара на странице из заголовка Product Page
    new_pade_element = browser.find_element_by_css_selector('#content .col-sm-4 h1')
    assert new_pade_element.text == name_element


# Тест 3 Featured Macbook открытия карточки с товаром по клику на название
def test_click_featured_name(browser, url, wait):
    # открываем главную
    browser.get(url)
    element = browser.find_elements_by_css_selector('.product-layout .product-thumb')[0]
    actions = ActionChains(browser)
    # перематываем страницу до элемента
    actions.move_to_element(element)
    # получаем название товара на Main Page из Featured
    name_element = browser.find_element_by_css_selector('.product-layout .caption a').text
    actions.perform()
    # клик на название Featured продукта (надо исправить css селектор в element)
    element.click()
    # получаем название товара на странице из заголовка Product Page
    product_name = browser.find_element_by_css_selector('#content .col-sm-4 h1')
    assert product_name.text == name_element


# Тест 4 Featured по стоимости
@pytest.mark.parametrize("product_index", [0, 1, 2, 3])
def test_featured_price(browser, url, product_index):
    # открываем главную
    browser.get(url)
    element = browser.find_elements_by_css_selector('.product-layout')[product_index]
    # перематываем страницу до элемента
    element.location_once_scrolled_into_view
    # получаем стоимость Featured продукта на Main Page
    price_element = str(element.find_element_by_css_selector('.product-layout .price').text)
    price_element = price_element.split('\n')[0]
    price_element = price_element.split(' ')[0]
    # клик на название Featured продукта
    element_name = element.find_element_by_css_selector('.product-layout .caption a')
    element_name.click()
    # получаем стоимость продукта на Product Page
    new_pade_element = browser.find_element_by_css_selector('#content .row .col-sm-4 h2')
    assert new_pade_element.text == price_element


# Тест 5 Переключение картинок в первом слайдбаре
def test_show_next_slide(browser, url, wait):
    # открываем главную
    browser.get(url)
    # перематываем первый слайд бар вперед
    swiper = browser.find_element_by_css_selector('#content .swiper-button-next')
    swiper.click()
    # делаем скриншот
    picture_slide_first = browser.find_element_by_css_selector(
            '.swiper-viewport #slideshow0')
    picture_slide_first.screenshot('picture_slide_first.png')
    # перематываем первый слайд бар вперед
    swiper.click()
    # делаем скриншот
    picture_slide_second = browser.find_element_by_css_selector(
            '.swiper-viewport #slideshow0')
    picture_slide_second.screenshot('picture_slide_second.png')
    # сравниваем скриншоты
    # image_one = Image.open('picture_slide_first.png').convert('RGB')
    # image_two = Image.open('picture_slide_second.png').convert('RGB')
    # diff = ImageChops.difference(image_one, image_two)
    h1 = Image.open('picture_slide_first.png').histogram()
    h2 = Image.open('picture_slide_second.png').histogram()
    rms = math.sqrt(reduce(operator.add,
                           map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))
    print(rms)
    if rms <= 90:
        diff = "Identical"
    else:
        diff = "Different"
    assert diff == "Different"
