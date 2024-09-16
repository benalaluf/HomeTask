# Telegram Bot Testing Project

This project automates the testing of a Telegram bot designed to calculate the hash of `.jpg` and `.jpeg` images. If the bot encounters other file types or text, it will return an error. Testing is seamlessly executed through the Telegram interface using a Python script with Appium.

## Requirements

Before you start, make sure you have the following:

- **ADB Environment**: Ensure that `adb` (Android Debug Bridge) is installed and correctly configured on your machine.
- **Telegram**: The Android device must have Telegram installed and logged into the test account.
- **Image Files**: Ensure that your test images (`.jpg`/`.jpeg`) are pushed to the device before starting the tests.

## Setup

1. Setup your Android device via `adb` and ensure Telegram is logged in.
2. Push the test images to the connected device using the following script:
    ```bash
    ./push_images.sh
    ```
3. RUN

## Running the Project

You’ve got two ways to run the tests:

### 1. Running with `tmux_run.sh` (The Cool Way 😎)

This is the recommended option for those who enjoy seeing things happen in real-time. Using `tmux`, this script splits your terminal into multiple panes, letting you observe device logs and test results side by side.

- **Requirements**: 
  - You need `tmux` installed to enjoy this cool feature.

- **How to Run**:
    ```bash
    sudo chmod +x tmux_run.sh
    sudo ./tmux_run.sh
    ```

This will automatically pick the live `adb` device, fire up `tmux`, and start the tests in an awesome split-screen view!

### 2. Running with `run.sh` (The Simple Way)

If you’re looking for a no-fuss, straightforward execution, you can run the tests with `run.sh`. No `tmux` required, just plain output.

- **How to Run**:
    ```bash
    ./run.sh
    ```

The test will run as usual, printing everything to your terminal.

## Automatic ADB Device Selection

Both `run.sh` and `tmux_run.sh` scripts are smart enough to automatically detect and connect to the live `adb` device.

## Additional Notes


- The project is designed to be user-friendly and straightforward, with a lot of work spent learning Docker to streamline the process. 🐳
- If you run into issues, manually running the Docker container is recommended. It may give you more control over debugging any environment problems that pop up.
- I run my test with Pixel_8_API_35, although the code should work with every device

## BTW works on my mechine
![](assets/works_on_my_mechine.gif)