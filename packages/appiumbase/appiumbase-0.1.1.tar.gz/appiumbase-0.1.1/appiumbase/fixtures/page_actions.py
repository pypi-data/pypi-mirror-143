"""
This module contains a set of methods that can be used for page loads and
for waiting for elements to appear on a page.
These methods improve on and expand existing WebDriver commands.
Improvements include making WebDriver commands more robust and more reliable
by giving page elements enough time to load before taking action on them.
The default option for searching for elements is by Accessibility ID.
This can be changed by overriding the "MobileBy" parameter.
Options are:
MobileBy.CSS_SELECTOR
MobileBy.CLASS_NAME
MobileBy.ID
MobileBy.NAME
MobileBy.LINK_TEXT
MobileBy.XPATH
MobileBy.TAG_NAME
MobileBy.PARTIAL_LINK_TEXT
"""

import codecs
import os
import sys
import time
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import StaleElementReferenceException
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.action_chains import ActionChains
from appiumbase.config import settings
from appiumbase.fixtures import shared_utils as s_utils


def is_element_present(driver, selector, by=MobileBy.ACCESSIBILITY_ID):
    """
    Returns whether the specified element selector is present on the page.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    @Returns
    Boolean (is element present)
    """
    try:
        driver.find_element(by=by, value=selector)
        return True
    except Exception:
        return False


def is_element_visible(driver, selector, by=MobileBy.ACCESSIBILITY_ID):
    """
    Returns whether the specified element selector is visible on the page.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    @Returns
    Boolean (is element visible)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_displayed()
    except Exception:
        return False


def is_element_enabled(driver, selector, by=MobileBy.ACCESSIBILITY_ID):
    """
    Returns whether the specified element selector is enabled on the page.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    @Returns
    Boolean (is element enabled)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_enabled()
    except Exception:
        return False


def is_text_visible(driver, text, selector, by=MobileBy.ACCESSIBILITY_ID):
    """
    Returns whether the specified text is visible in the specified selector.
    @Params
    driver - the webdriver object (required)
    text - the text string to search for
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    @Returns
    Boolean (is text visible)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_displayed() and text in element.text
    except Exception:
        return False


def is_attribute_present(
        driver, selector, attribute, value=None, by=MobileBy.ACCESSIBILITY_ID
):
    """
    Returns whether the specified attribute is present in the given selector.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    attribute - the attribute that is expected for the element (required)
    value - the attribute value that is expected (Default: None)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    @Returns
    Boolean (is attribute present)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        found_value = element.get_attribute(attribute)
        if found_value is None:
            raise Exception()

        if value is not None:
            if found_value == value:
                return True
            else:
                raise Exception()
        else:
            return True
    except Exception:
        return False


def hover_on_element(driver, selector, by=MobileBy.ACCESSIBILITY_ID):
    """
    Fires the hover event for the specified element by the given selector.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    """
    element = driver.find_element(by=by, value=selector)
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()


def hover_element(driver, element):
    """
    Similar to hover_on_element(), but uses found element, not a selector.
    """
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()


def timeout_exception(exception, message):
    exception, message = s_utils.format_exc(exception, message)
    raise exception(message)


def hover_and_click(
        driver,
        hover_selector,
        click_selector,
        hover_by=MobileBy.ACCESSIBILITY_ID,
        click_by=MobileBy.ACCESSIBILITY_ID,
        timeout=settings.SMALL_TIMEOUT,
):
    """
    Fires the hover event for a specified element by a given selector, then
    clicks on another element specified. Useful for dropdown hover based menus.
    @Params
    driver - the webdriver object (required)
    hover_selector - the css selector to hover over (required)
    click_selector - the css selector to click on (required)
    hover_by - the hover selector type to search by (Default: MobileBy.CSS_SELECTOR)
    click_by - the click selector type to search by (Default: MobileBy.CSS_SELECTOR)
    timeout - number of seconds to wait for click element to appear after hover
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    element = driver.find_element(by=hover_by, value=hover_selector)
    hover = ActionChains(driver).move_to_element(element)
    for x in range(int(timeout * 10)):
        try:
            hover.perform()
            element = driver.find_element(by=click_by, value=click_selector)
            element.click()
            return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    message = "Element {%s} was not present after %s second%s!" % (
        click_selector,
        timeout,
        plural,
    )
    timeout_exception(NoSuchElementException, message)


def hover_element_and_click(
        driver,
        element,
        click_selector,
        click_by=MobileBy.ACCESSIBILITY_ID,
        timeout=settings.SMALL_TIMEOUT,
):
    """
    Similar to hover_and_click(), but assumes top element is already found.
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    hover = ActionChains(driver).move_to_element(element)
    for x in range(int(timeout * 10)):
        try:
            hover.perform()
            element = driver.find_element(by=click_by, value=click_selector)
            element.click()
            return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    message = "Element {%s} was not present after %s second%s!" % (
        click_selector,
        timeout,
        plural,
    )
    timeout_exception(NoSuchElementException, message)


def hover_element_and_double_click(
        driver,
        element,
        click_selector,
        click_by=MobileBy.ACCESSIBILITY_ID,
        timeout=settings.SMALL_TIMEOUT,
):
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    hover = ActionChains(driver).move_to_element(element)
    for x in range(int(timeout * 10)):
        try:
            hover.perform()
            element_2 = driver.find_element(by=click_by, value=click_selector)
            actions = ActionChains(driver)
            actions.move_to_element(element_2)
            actions.double_click(element_2)
            actions.perform()
            return element_2
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    message = "Element {%s} was not present after %s second%s!" % (
        click_selector,
        timeout,
        plural,
    )
    timeout_exception(NoSuchElementException, message)


def wait_for_element_present(driver, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=settings.LARGE_TIMEOUT):
    element = None
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        #s_utils.check_if_time_limit_exceeded()
        try:
            element = driver.find_element(by=by, value=selector)
            return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    if not element:
        message = "Element {%s} was not present after %s second%s!" % (
            selector,
            timeout,
            plural,
        )
        timeout_exception(NoSuchElementException, message)


def wait_for_element_visible(
        driver, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the element is present and visible on the page.
    Raises NoSuchElementException if the element does not exist
    within the specified timeout.
    Raises ElementNotVisibleException if the element exists,
    but is not visible (eg. opacity is "0") within the specified timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object
    """
    element = None
    is_present = False
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            is_present = True
            if element.is_displayed():
                return element
            else:
                element = None
                raise Exception()
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    if not element and by != MobileBy.LINK_TEXT:
        if not is_present:
            # The element does not exist in the HTML
            message = "Element {%s} was not present after %s second%s!" % (
                selector,
                timeout,
                plural,
            )
            timeout_exception(NoSuchElementException, message)
        # The element exists in the HTML, but is not visible
        message = "Element {%s} was not visible after %s second%s!" % (
            selector,
            timeout,
            plural,
        )
        timeout_exception(ElementNotVisibleException, message)
    if not element and by == MobileBy.LINK_TEXT:
        message = "Link text {%s} was not visible after %s second%s!" % (
            selector,
            timeout,
            plural,
        )
        timeout_exception(ElementNotVisibleException, message)


def wait_for_text_visible(
        driver, text, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the text is present in the element and visible
    on the page.
    Raises NoSuchElementException if the element does not exist in the HTML
    within the specified timeout.
    Raises ElementNotVisibleException if the element exists in the HTML,
    but the text is not visible within the specified timeout.
    @Params
    driver - the webdriver object (required)
    text - the text that is being searched for in the element (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object that contains the text searched for
    """
    element = None
    is_present = False
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        try:
            element = driver.find_element(by=by, value=selector)
            is_present = True
            if element.is_displayed() and text in element.text:
                return element
            else:
                element = None
                raise Exception()
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    if not element:
        if not is_present:
            # The element does not exist in the HTML
            message = "Element {%s} was not present after %s second%s!" % (
                selector,
                timeout,
                plural,
            )
            timeout_exception(NoSuchElementException, message)
        # The element exists in the HTML, but the text is not visible
        message = (
                "Expected text {%s} for {%s} was not visible after %s second%s!"
                % (text, selector, timeout, plural)
        )
        timeout_exception(ElementNotVisibleException, message)


def wait_for_exact_text_visible(
        driver, text, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the text matches exactly with the text in the element,
    and the text is visible.
    Raises NoSuchElementException if the element does not exist in the HTML
    within the specified timeout.
    Raises ElementNotVisibleException if the element exists in the HTML,
    but the exact text is not visible within the specified timeout.
    @Params
    driver - the webdriver object (required)
    text - the exact text that is expected for the element (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object that contains the text searched for
    """
    element = None
    is_present = False
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        try:
            element = driver.find_element(by=by, value=selector)
            is_present = True
            if element.is_displayed() and text.strip() == element.text.strip():
                return element
            else:
                element = None
                raise Exception()
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    if not element:
        if not is_present:
            # The element does not exist in the HTML
            message = "Element {%s} was not present after %s second%s!" % (
                selector,
                timeout,
                plural,
            )
            timeout_exception(NoSuchElementException, message)
        # The element exists in the HTML, but the exact text is not visible
        message = (
                "Expected exact text {%s} for {%s} was not visible "
                "after %s second%s!" % (text, selector, timeout, plural)
        )
        timeout_exception(ElementNotVisibleException, message)


def wait_for_attribute(
        driver,
        selector,
        attribute,
        value=None,
        by=MobileBy.ACCESSIBILITY_ID,
        timeout=settings.LARGE_TIMEOUT,
):
    """
    Searches for the specified element attribute by the given selector.
    Returns the element object if the expected attribute is present
    and the expected attribute value is present (if specified).
    Raises NoSuchElementException if the element does not exist in the HTML
    within the specified timeout.
    Raises NoSuchAttributeException if the element exists in the HTML,
    but the expected attribute/value is not present within the timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    attribute - the attribute that is expected for the element (required)
    value - the attribute value that is expected (Default: None)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    timeout - the time to wait for the element attribute in seconds
    @Returns
    A web element object that contains the expected attribute/value
    """
    element = None
    element_present = False
    attribute_present = False
    found_value = None
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        try:
            element = driver.find_element(by=by, value=selector)
            element_present = True
            attribute_present = False
            found_value = element.get_attribute(attribute)
            if found_value is not None:
                attribute_present = True
            else:
                element = None
                raise Exception()

            if value is not None:
                if found_value == value:
                    return element
                else:
                    element = None
                    raise Exception()
            else:
                return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    if not element:
        if not element_present:
            # The element does not exist in the HTML
            message = "Element {%s} was not present after %s second%s!" % (
                selector,
                timeout,
                plural,
            )
            timeout_exception(NoSuchElementException, message)
        if not attribute_present:
            # The element does not have the attribute
            message = (
                    "Expected attribute {%s} of element {%s} was not present "
                    "after %s second%s!" % (attribute, selector, timeout, plural)
            )
            timeout_exception(NoSuchAttributeException, message)
        # The element attribute exists, but the expected value does not match
        message = (
                "Expected value {%s} for attribute {%s} of element {%s} was not "
                "present after %s second%s! (The actual value was {%s})"
                % (value, attribute, selector, timeout, plural, found_value)
        )
        timeout_exception(NoSuchAttributeException, message)


def wait_for_element_absent(
        driver, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the specified element by the given selector.
    Raises an exception if the element is still present after the
    specified timeout.
    @Params
    driver - the webdriver object
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        try:
            driver.find_element(by=by, value=selector)
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
        except Exception:
            return True
    plural = "s"
    if timeout == 1:
        plural = ""
    message = "Element {%s} was still present after %s second%s!" % (
        selector,
        timeout,
        plural,
    )
    timeout_exception(Exception, message)


def wait_for_element_not_visible(
        driver, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the specified element by the given selector.
    Raises an exception if the element is still visible after the
    specified timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    timeout - the time to wait for the element in seconds
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        try:
            element = driver.find_element(by=by, value=selector)
            if element.is_displayed():
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
            else:
                return True
        except Exception:
            return True
    plural = "s"
    if timeout == 1:
        plural = ""
    message = "Element {%s} was still visible after %s second%s!" % (
        selector,
        timeout,
        plural,
    )
    timeout_exception(Exception, message)


def wait_for_text_not_visible(
        driver, text, selector, by=MobileBy.ACCESSIBILITY_ID, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the text in the element of the given selector on the page.
    Returns True if the text is not visible on the page within the timeout.
    Raises an exception if the text is still present after the timeout.
    @Params
    driver - the webdriver object (required)
    text - the text that is being searched for in the element (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object that contains the text searched for
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        if not is_text_visible(driver, text, selector, by=by):
            return True
        now_ms = time.time() * 1000.0
        if now_ms >= stop_ms:
            break
        time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    message = "Text {%s} in {%s} was still visible after %s second%s!" % (
        text,
        selector,
        timeout,
        plural,
    )
    timeout_exception(Exception, message)


def wait_for_attribute_not_present(
        driver,
        selector,
        attribute,
        value=None,
        by=MobileBy.ACCESSIBILITY_ID,
        timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the specified element attribute by the given selector.
    Returns True if the attribute isn't present on the page within the timeout.
    Also returns True if the element is not present within the timeout.
    Raises an exception if the attribute is still present after the timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    attribute - the element attribute (required)
    value - the attribute value (Default: None)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    timeout - the time to wait for the element attribute in seconds
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        if not is_attribute_present(
                driver, selector, attribute, value=value, by=by
        ):
            return True
        now_ms = time.time() * 1000.0
        if now_ms >= stop_ms:
            break
        time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    message = (
            "Attribute {%s} of element {%s} was still present after %s second%s!"
            "" % (attribute, selector, timeout, plural)
    )
    if value:
        message = (
                "Value {%s} for attribute {%s} of element {%s} was still present "
                "after %s second%s!"
                "" % (value, attribute, selector, timeout, plural)
        )
    timeout_exception(Exception, message)


def find_visible_elements(driver, selector, by=MobileBy.ACCESSIBILITY_ID):
    """
    Finds all WebElements that match a selector and are visible.
    Similar to webdriver.find_elements.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: MobileBy.CSS_SELECTOR)
    """
    elements = driver.find_elements(by=by, value=selector)
    try:
        v_elems = [element for element in elements if element.is_displayed()]
        return v_elems
    except (StaleElementReferenceException, ElementNotInteractableException):
        time.sleep(0.1)
        elements = driver.find_elements(by=by, value=selector)
        v_elems = []
        for element in elements:
            if element.is_displayed():
                v_elems.append(element)
        return v_elems


def save_screenshot(driver, name, folder=None):
    """
    Saves a screenshot to the current directory (or to a subfolder if provided)
    If the folder provided doesn't exist, it will get created.
    The screenshot will be in PNG format.
    """
    if not name.endswith(".png"):
        name = name + ".png"
    if folder:
        abs_path = os.path.abspath(".")
        file_path = abs_path + "/%s" % folder
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        screenshot_path = "%s/%s" % (file_path, name)
    else:
        screenshot_path = name
    try:
        element = driver.find_element(by=MobileBy.TAG_NAME, value="body")
        element_png = element.screenshot_as_png
        with open(screenshot_path, "wb") as file:
            file.write(element_png)
    except Exception:
        if driver:
            driver.get_screenshot_as_file(screenshot_path)
        else:
            pass


def wait_for_and_accept_alert(driver, timeout=settings.LARGE_TIMEOUT):
    """
    Wait for and accept an alert. Returns the text from the alert.
    @Params
    driver - the webdriver object (required)
    timeout - the time to wait for the alert in seconds
    """
    alert = wait_for_and_switch_to_alert(driver, timeout)
    alert_text = alert.text
    alert.accept()
    return alert_text


def wait_for_and_dismiss_alert(driver, timeout=settings.LARGE_TIMEOUT):
    """
    Wait for and dismiss an alert. Returns the text from the alert.
    @Params
    driver - the webdriver object (required)
    timeout - the time to wait for the alert in seconds
    """
    alert = wait_for_and_switch_to_alert(driver, timeout)
    alert_text = alert.text
    alert.dismiss()
    return alert_text


def wait_for_and_switch_to_alert(driver, timeout=settings.LARGE_TIMEOUT):
    """
    Wait for a browser alert to appear, and switch to it. This should be usable
    as a drop-in replacement for driver.switch_to.alert when the alert box
    may not exist yet.
    @Params
    driver - the webdriver object (required)
    timeout - the time to wait for the alert in seconds
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        try:
            alert = driver.switch_to.alert
            # Raises exception if no alert present
            dummy_variable = alert.text  # noqa
            return alert
        except NoAlertPresentException:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    message = "Alert was not present after %s seconds!" % timeout
    timeout_exception(Exception, message)
