# Getting Started

Before running the Script, you will need to download a chrome web driver. Follow the steps below to setup the project:

1. Use the link [What Version of Chrome Do I Have?](https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have) to find your Chrome version. My version is 102.
2. Select the Chrome Driver from [Download a Chrome Driver for Windows, Linux, or Mac](https://chromedriver.chromium.org/downloads) that matches your version. And download either the windows, linux, or mac zip.
3. Extract the chrome driver from the zip and place the driver into the ```drivers folder```
4. Rename the driver to ```chromedriverwindows``` if you're on windows.
5. Add the data csv into the ```input folder``` and rename the file to ```data.csv```
6. Run the script.
7. The output data csv will be found in the output folder.

# Running the Script
To run the app use the following command:
```python main.py```

# If the program is unable to find the chrome driver
1. Make sure the chrome driver is named correctly. Example => ```chromedriverwindows.exe``` for windows.
2. In the service/seleniumServices.py file, make sure you use the ```absolute path``` when referencing the chrome driver in the INIT method.
3. The FRAX website may be down. 
4. If all else fails, contact Alex.


# If Selenium fails
If the selenium driver fails at any point and is unable to properly close, the selenium driver will keep running in the background taking up all your RAM.

To remove these tasks from running in the background, do the following
1. Open up a ```command prompt``` and type ```tasklist```
2. In the command prompt, all tasks currently running on your computer will be shown. 
3. Verify that some tasks are named ```chrome.exe``` or ```chromedriver.exe```
3. In the ```command prompt``` type ```taskkill /F /IM chrome.exe``` or  ```taskkill /F /IM chromedriver.exe```
4. Verify that the tasks are not running anymore by typing ```tasklist``` again.
5. Close the ```command prompt```