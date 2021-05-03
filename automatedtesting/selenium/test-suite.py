#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

URL_LOGIN = 'https://www.saucedemo.com/'
URL_INVENTORY = 'https://www.saucedemo.com/inventory.html'
URL_CART = 'https://www.saucedemo.com/cart.html'


def login(driver, user, password):
    """Login to the website"""
    print('Navigating to the demo page to login.')
    driver.get(URL_LOGIN)
    driver.find_element_by_id("user-name").send_keys(user)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("login-button").click()
    assert URL_INVENTORY in driver.current_url
    print(f"Login with username {user} and password {password} successful")


def add_items(driver):
    """Add items to the cart"""
    cart = []
    print('Add all items to the cart')
    items = driver.find_elements_by_class_name('inventory_item')
    for item in items:
        item_name = item.find_element_by_class_name('inventory_item_name').text
        cart.append(item_name)
        item.find_element_by_class_name('btn_inventory').click()
        print(f'\tAdded {item_name}')
    cart_item = driver.find_element_by_class_name('shopping_cart_badge')
    assert int(cart_item.text) == len(items)

    driver.find_element_by_class_name('shopping_cart_link').click()
    assert URL_CART in driver.current_url

    for item in driver.find_elements_by_class_name('inventory_item_name'):
        assert item.text in cart
    print('Finished testing adding items to the cart')


def remove_items(driver):
    """Remove items from the cart"""
    driver.find_element_by_class_name('shopping_cart_link').click()
    assert URL_CART in driver.current_url

    cart_items = len(driver.find_elements_by_class_name('cart_item'))

    print(f"Number of items in the cart = {cart_items}")
    for item in driver.find_elements_by_class_name('cart_item'):
        item_name = item.find_element_by_class_name('inventory_item_name').text
        item.find_element_by_class_name('cart_button').click()
        print(f'\tRemoved {item_name}')

    cart_items = len(driver.find_elements_by_class_name('cart_item'))
    assert cart_items == 0
    print('Finshed testing removing items from the cart')


def run_tests():
    """Run the test"""
    print("Starting the browser...")
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    print('Browser started successfully.')
    print('Login')
    login(driver, "standard_user", "secret_sauce")
    print('Add items')
    add_items(driver)
    print('Remove items')
    remove_items(driver)
    print("Tests Completed")


if __name__ == "__main__":
    run_tests()
