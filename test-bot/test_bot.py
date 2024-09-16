import sys
import unittest
from time import sleep

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

BOT_NAME = 'DuckImageAnalyser'
TELEGRAM_AT = 'duckimageanalyserbot'

class TestTelegramBot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.device_name = sys.argv[1] if len(sys.argv) > 1 else 'emulator-5554'

    def setUp(self):
        options = UiAutomator2Options()
        options.platformName = 'Android'
        options.deviceName = self.device_name  # Use the provided device name
        options.appPackage = 'org.telegram.messenger'
        options.appActivity = 'org.telegram.ui.LaunchActivity'
        options.noReset = True
        options.autoGrantPermissions = True

        self.driver = webdriver.Remote('http://localhost:4723', options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def run(self, result=None):
        super().run(result)
        if result.wasSuccessful():
            print(f'Test {self._testMethodName} PASSED')
        else:
            print(f'Test {self._testMethodName} FAILED')

    def open_telegram_reliable(self):
        self.driver.press_keycode(3)  # Go to home screen
        sleep(0.8)
        size = self.driver.get_window_size()
        start_x = size['width'] / 2
        start_y = size['height'] * 0.9
        end_y = size['height'] * 0.1
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)
        sleep(0.8)
        element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Telegram")')
        element.click()

    def find_chat(self, name, telegramat):
        self.open_telegram_reliable()

        search_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Search")')
        search_button.click()

        search_input = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Search")')
        search_input.send_keys(telegramat)

        chat_result = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                               f'new UiSelector().className("android.view.ViewGroup").textContains("{name}")')
        chat_result.click()

        try:
            start_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("START")')
            if start_button.is_displayed():
                start_button.click()
        except Exception:
            pass

    def send_message(self, message):
        input_field = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Message")')
        input_field.send_keys(message)
        send_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Send")')
        send_button.click()

    def send_image(self, image_name):
        attach_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                                 'new UiSelector().description("Attach media")')
        attach_button.click()

        element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("File")')
        element.click()

        element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Internal Storage")')
        element.click()

        element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{image_name}")')
        element.click()

    def get_last_message(self):
        message_elements = self.driver.find_element(AppiumBy.XPATH, "//androidx.recyclerview.widget.RecyclerView")
        # fix weird bug when dockerized
        while True:
            childs = message_elements.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")
            if "Seen" not in childs[-1].text:
                return childs[-1].text
            sleep(0.5)

    def test_01_send_text_instead_of_image(self):
        self.find_chat(BOT_NAME, TELEGRAM_AT)
        self.send_message("DUCK")
        last_message = self.get_last_message()
        self.assertIn("error", last_message.lower())

    def test_02_send_png(self):
        self.send_image("duck.png")
        last_message = self.get_last_message()
        self.assertIn("error", last_message.lower())

    def test_03_send_fugazi_jpg(self):
        self.send_image("fugaziduck.jpg")
        last_message = self.get_last_message()
        self.assertIn("error", last_message.lower())

    def test_04_send_jpg(self):
        self.send_image("duck.jpg")
        last_message = self.get_last_message()
        self.assertIn("hash", last_message.lower())


if __name__ == '__main__':
    unittest.main()
