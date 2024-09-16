import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy

class TestTelegramBot(unittest.TestCase):

    def setUp(self):
        # Setup UiAutomator2 options for Appium on Android 11
        options = UiAutomator2Options()
        options.platformName = 'Android'
        options.platformVersion = '11'  # Targeting Android 11
        options.deviceName = 'emulator-5554'
        options.appPackage = 'org.telegram.messenger'
        options.appActivity = 'org.telegram.ui.LaunchActivity'
        options.noReset = True  # Keep the app logged in after each test
        options.autoGrantPermissions = True

        # Initialize Appium driver with the options
        self.driver = webdriver.Remote('http://localhost:4723', options=options)
        self.driver.implicitly_wait(2)  # Implicit wait for elements


    def tearDown(self):
        # Quit the driver after the test is done
        self.driver.quit()

    def find_chat(self, name, telegramat):
        element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Telegram")')
        element.click()

        search_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Search")')
        search_button.click()


        search_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Search")')
        search_button.send_keys(telegramat)


        chat_result = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("android.view.ViewGroup").textContains("{name}")')
        chat_result.click()

        try:
            start_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,   'new UiSelector().text("START")')
            if start_button.is_displayed():
                start_button.click()
        except Exception:
            # Continue if the button is not found
            pass


    def send_message(self, message):
        input_field = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Message")')
        input_field.send_keys(message)
        send_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Send")')
        send_button.click()

    def send_image(self, image_name):
        # Open the attachment menu and send an image

        attach_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Attach media")')
        attach_button.click()


        element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("File")')
        element.click()

        element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Internal Storage")')
        element.click()

        element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{image_name}")')
        element.click()



    def get_last_message(self):
        message_elements = self.driver.find_element(AppiumBy.XPATH, "//androidx.recyclerview.widget.RecyclerView")
        childs = message_elements.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")
        return childs[-1].text if message_elements else None

    def test_01_send_text_instead_of_image(self):
        self.find_chat("DuckImageAnalyser", "duckimageanalyserbot")
        self.send_message("This is a test text")

        last_message = self.get_last_message()
        self.assertIn("error", last_message.lower())

    def test_02_send_png(self):
        # self.find_chat("boti")
        self.send_image("duck.png")

        last_message = self.get_last_message()
        self.assertIn("error", last_message.lower())

    def test_03_send_fugazi_jpg(self):
        # self.find_chat("boti", "botitheimagebot")
        self.send_image("fugaziduck.jpg")

        last_message = self.get_last_message()
        self.assertIn("error", last_message.lower())

    def test_04_send_jpg(self):
        # self.find_chat("boti")
        self.send_image("duck.jpg")

        last_message = self.get_last_message()
        self.assertIn("hash", last_message.lower())




if __name__ == '__main__':
    unittest.main()
