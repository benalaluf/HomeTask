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

        # Initialize Appium driver with the options
        self.driver = webdriver.Remote('http://localhost:4723', options=options)
        self.driver.implicitly_wait(10)  # Implicit wait for elements


    def tearDown(self):
        # Quit the driver after the test is done
        self.driver.quit()

    def find_chat(self, chat_name):
        # Find the bot by searching for it in Telegram
        element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Telegram")')
        element.click()  # To click the Telegram icon

        search_button = self.driver.find_element(AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Search"]/android.widget.ImageView')
        search_button.click()

        search_input = self.driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[@text="Search"]')
        search_input.send_keys(chat_name)
        sleep(1)

        # Select the bot from search results
        chat_result = self.driver.find_element(AppiumBy.XPATH, f'//android.view.ViewGroup[@text="{chat_name}, bot"]')
        chat_result.click()



    def send_message(self, message):
        # Send a text message to the bot

        sleep(1)
        input_field = self.driver.find_element(AppiumBy.XPATH,'//android.widget.FrameLayout[@content-desc="Web tabs "]')
        input_field.click()
        sleep(1)
        input_field = self.driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[@text="Message"]')
        input_field.send_keys(message)
        sleep(2)

        send_button = self.driver.find_element(AppiumBy.XPATH, '//android.view.View[@content-desc="Send"]')
        send_button.click()

    def send_image(self, image_path):
        # Open the attachment menu and send an image

        attach_button = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Attach")
        attach_button.click()

        gallery_button = self.driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Gallery']")
        gallery_button.click()

        # Select image from gallery
        self.driver.find_element(AppiumBy.XPATH, f"//android.widget.ImageView[contains(@content-desc, '{image_path}')]").click()
        sleep(2)

        # Send the image
        send_button = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Send")
        send_button.click()

    def get_last_message(self):
        # Get the last message in the chat
        message_elements = self.driver.find_element(AppiumBy.XPATH, "//androidx.recyclerview.widget.RecyclerView")
        childs = message_elements.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")
        return childs[-1].text if message_elements else None

    def test_01_send_text_instead_of_image(self):
        self.find_chat("boti")
        self.send_message("This is a test text")
        sleep(2)

        last_message = self.get_last_message()
        self.assertIn("error", last_message.lower())

    # def test_send_jpg_image(self):
    #     self.find_chat("boti")
    #     self.send_image("test_image.jpg")  # Adjust with the correct image path/identifier
    #     sleep(3)
    #
    #     last_message = self.get_last_message()
    #     self.assertNotIn("error", last_message.lower())
    #
    # def test_send_non_jpg_file(self):
    #     self.find_chat("boti")
    #     self.send_image("test_image.png")  # Use a non-JPG file
    #     sleep(3)
    #
    #     last_message = self.get_last_message()
    #     self.assertIn("error", last_message.lower())

if __name__ == '__main__':
    unittest.main()
