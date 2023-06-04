### Let This Program Keep Track of Your Products for You💲
Python code written with selenium and undetected-chromedriver that keeps track of your newly added products every five minutes, deletes any url from the database after a certain period of time if you delete it from the txt file with a database and control system, and allows you to send an e-mail to yourself if any discount is caught.

**Why Selenium  ❓**

The Request repository is really the heart of very fast scraping. But one of the biggest drawbacks is that it gets caught by anti-bots. I don't know if Amazon has any sanctions on this, but I don't want to get a connection refused error after using the program for 1 day and I wanted to use this library to secure the basics. I tried to minimize bot detection as much as possible by using undetected-chromedriver with Selenium, there is a disadvantage in scraping the first products in terms of speed, but I did not see any loss of speed in subsequent products. It works really efficiently.

**Why do you keep the data in a txt file instead of just in a database❓**

As a developer who likes to surf Github, there were times when I couldn't get out of the database structure when I wanted to use a library I liked. I would also love for anyone who doesn't understand software to be able to use my program, and if anyone can use it, then it passes the accessibility test for me. That's why I wanted to add a .txt file, you can add urls from the terminal but if you want to delete them you can go into the txt file and delete any data, so after 3 cycles if the url is not rewritten in the txt file it will be deleted from the database. I know it's a bit crude and old school :9

**Side Note📝**

Don't forget to install chromedriver.exe according to your Chrome version. You can find it in Help > About Google Chrome. The current version of chromedriver.exe is 113.0.5672.

**Technologies used**

```
selenium
selenium-wire
undetected-chromedriver
sqlite3
```
You can install all used modules with install.bat or find them in requirements.txt.
All remaining libraries will be installed on your device with Python 3.10.

