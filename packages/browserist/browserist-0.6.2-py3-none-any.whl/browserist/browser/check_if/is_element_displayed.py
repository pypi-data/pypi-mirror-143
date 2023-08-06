from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def check_if_is_element_displayed(driver: object, xpath: str) -> bool:
    try:
        element = driver.find_element(By.XPATH, xpath)  # type: ignore
        return element.is_displayed()  # type: ignore
    except (NoSuchElementException, Exception):
        return False
