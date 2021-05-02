# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import datetime

# Function to log text with a timestamp
def print_log(text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("{0} - {1}".format(timestamp, text))

# Setup the driver and navigate to the demo website
def driver_setup(website):
    print_log("Starting the chrome browser")
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    print_log("Browser started successfully.")
    driver.get(website)
    return driver

# Start the browser and login with standard_user
def login(driver, user, password):
    print_log("Logging in")
    driver.find_element_by_id("user-name").send_keys(user)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("login-button").click()
    product_label = driver.find_element_by_css_selector(
        "div[class='product_label']").text
    assert "Products" in product_label
    print_log(
        "Login with username {0} and password {1} successfully".format(user, password))


def add_cart(driver, n_items):
    for i in range(n_items):
        # Get the URL of the product
        element = "a[id='item_" + str(i) + "_title_link']"
        driver.find_element_by_css_selector(element).click()  # Click the URL
        driver.find_element_by_css_selector(
            "button.btn_primary.btn_inventory").click()  # Add the product to the cart
        product = driver.find_element_by_css_selector(
            "div[class='inventory_details_name']").text  # Get the name of the product from the page
        # Display message saying which product was added
        print_log("{0} added to shopping cart.".format(product))
        driver.find_element_by_css_selector(
            "button.inventory_details_back_button").click()  # Click the Back button
    print_log(
        "{0} items are all added to shopping cart successfully".format(n_items))


def remove_cart(driver, n_items):
    for i in range(n_items):
        element = "a[id='item_" + str(i) + "_title_link']"
        driver.find_element_by_css_selector(element).click()
        driver.find_element_by_css_selector(
            "button.btn_secondary.btn_inventory").click()
        product = driver.find_element_by_css_selector(
            "div[class='inventory_details_name']").text
        # Display message saying which product was added
        print_log("{0} removed from shopping cart.".format(product))
        driver.find_element_by_css_selector(
            "button.inventory_details_back_button").click()

    print_log(
        "{0} items are all removed from shopping cart successfully".format(n_items))

if __name__ == "__main__":
    items = 6
    driver = driver_setup("https://www.saucedemo.com/")
    login(driver, "standard_user", "secret_sauce")
    add_cart(driver, items)
    remove_cart(driver, items)
    print_log("Tests Completed")
