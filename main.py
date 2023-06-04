from callDrivers import *

class Scraper:
    def __init__(self):
        self.prepare_driver()
        if os.path.exists('urls.txt') != True:
            print("urls.txt not found, creating..")
            with open('urls.txt', 'w', encoding='utf-8') as f:
                f.close()
        if os.path.exists('mail.conf') != True:
            print("mail.conf not found, creating...")
            with open("mail.conf",'w',encoding='utf-8') as f:
                f.write("sender_mail=examplesendermail@gmail.com\nsender_mail_password=examplepasswordforsendermail\nreceiver_mail=examplereceivermail")
                f.close()
        self.db = mysql.connect('checked_urls.db')
        self.cursor = self.db.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS `products` (
          `ID` INTEGER,
          `url` varchar(400) NOT NULL,
          `price` int DEFAULT NULL,
          `erase_count` int DEFAULT 0,
          `timer` int DEFAULT 0,
          PRIMARY KEY (`ID`)
        )""")

    def get_current_products(self):
        with open('urls.txt', 'r', encoding='utf-8') as f:
            prods = f.read().splitlines()
        return prods
    def get_send_mail_info(self):
        with open('mail.conf','r',encoding='utf-8') as f:
            lines = f.read().splitlines()
        return lines[0].split('=',1)[1],lines[1].split('=',1)[1],lines[2].split('=',1)[1]

    def save_send_mail_info(self,sender_mail,sender_mail_passwd,reciever_mail):
        with open('mail.conf','w',encoding='utf-8') as f:
            f.write(f"sender_mail={sender_mail}\nsender_mail_password={sender_mail_passwd}\nreciever_mail={reciever_mail}")
        return True
    def prepare_driver(self):
        self.driver = callUcDriver(headless=True,useData=False,pageLoadStrategy="eager")
        return True

    def close_driver(self):
        self.driver.quit()
        return True

    def remove_non_ascii(self,text):
        return re.sub(r'[^\x00-\x7F]', ' ', text)

    def send_mail(self,product_price,product_title,product_url):
        mail,passwd,mail_to_send = self.get_send_mail_info()
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        msg = f"Subject: A discount has been detected on the product you are following!\n\nThe price of the product you follow on Amazon with the title {product_title.strip()} has dropped to {product_price.strip()} price! Here is the link to the product: {product_url}"

        try:
            s.login(mail,passwd)
            s.sendmail(
                from_addr=mail,
                to_addrs=mail_to_send,
                msg=msg
            )
            s.quit()
            return True
        except smtplib.SMTPAuthenticationError:
            print("Please check your e-mail and password, use the application password and make sure that 2-factor authentication is turned on.")
            return False

    def get_price(self):
        if waitElement(self.driver,'//span[@class="a-price-whole"]',20):
            return self.driver.find_element(By.XPATH,'//span[@class="a-price-whole"]').text
        return False

    def get_title(self):
        if waitElement(self.driver,'//span[@id="productTitle"]',20):
            return self.driver.find_element(By.XPATH,'//span[@id="productTitle"]').get_attribute('innerHTML')
        return False

    def save_to_database(self,product_url,product_price = None):
        if self.get_current_products().__contains__(product_url) != True:
            if product_price == None:
                print("Price scraping from the target url..")
                self.driver.get(product_url)
                product_price = self.get_price()
            title = self.get_title()
            values = (product_url),(product_price),(0),(0)
            sql = "INSERT INTO products(url,price,erase_count,timer) VALUES(?,?,?,?)"
            self.cursor.execute(sql,values)
            self.db.commit()
            print(f"Target url with the title {title.strip()} is saved in the database.")
            return True
        return False

    def scrape_avaibles_from_db(self):
        sql = "SELECT url,price FROM products WHERE timer = 0;"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        sql = """
        UPDATE products
        SET timer = CASE
            WHEN timer < 5 THEN timer + 1
            ELSE 0
            END
        ;
        """
        self.cursor.execute(sql)
        self.db.commit()
        return result

    def erase_not_avaible_urls(self):
        with open('urls.txt','r',encoding='utf-8') as f:
            base_urls = f.read().splitlines()
        for url in base_urls:
            url = url.strip()
            self.cursor.execute("SELECT * FROM products WHERE url = ?", (url,))
            result = self.cursor.fetchone()

            if result is None:
                erase_count = result[3]
                if erase_count == 3:
                    self.cursor.execute("DELETE FROM products WHERE url = ?", (url,))
                    self.db.commit()
                else:
                    self.cursor.execute("UPDATE products SET erase_count = erase_count + 1 WHERE url = ?", (url,))
                    self.db.commit()

    def find_discount_from_urls(self):
        prod_urls = self.scrape_avaibles_from_db()
        for prod in prod_urls:
            url = prod[0]
            old_price = prod[1]
            self.driver.get(url)
            price = self.get_price()
            if price != False:
                title = self.get_title()
                print(f"Checking product with title {title.strip()}.")
                if float(old_price) > float(price):
                    print("Discount founded, trying to send an email.")
                    mail_res = self.send_mail(price,title,url)
                    if mail_res:
                        print("Mail sended.")
            else:
                print("There was an error scraping the price, please contact the developer after making sure you have an internet connection.")
        self.erase_not_avaible_urls()

if __name__ == '__main__':
    scraper = Scraper()
    while True:
        print("""
1- Add a URL to scraper
2- Start scraper
3- Sending mail settings
4- Quit
        """)
        choice = input('Please make a choice:')
        if int(choice) == 1:
            while True:
                url = input("Please enter your amazon url:")
                if url.__contains__('www.amazon'):
                    save_res = scraper.save_to_database(url)
                    if save_res:
                        with open('urls.txt','r',encoding='utf-8') as f:
                            lines = f.read().splitlines()
                        lines.append(url)
                        with open('urls.txt','w',encoding='utf-8') as f:
                            f.write('\n'.join(str(line) for line in lines))
                    else:
                        print("The url you want to add to the database has already been added.")
                    break
                else:
                    print("Make sure the url you entered is correct and from amazon, contact the developer if the problem persists.")
        elif int(choice) == 2:
            while True:
                scraper.find_discount_from_urls()
                print("After waiting 5 minutes, the urls will be checked again.")
                time.sleep(300)
        elif int(choice) == 3:
            sender_mail,sender_mail_passwd,receiver_mail = scraper.get_send_mail_info()

            print(f"\nIf you don't know how to make an app key, follow this tutorial: https://www.youtube.com/watch?v=hXiPshHn9Pw\nCurrent informations;\nsender_mail={sender_mail}\nsender_mail_passwd={sender_mail_passwd}\nreciever_mail={receiver_mail}")
            while True:
                print("""
1- Sender mail
2- Sender mail password ( app key )
3- Receiver mail
4- Save settings and quit
                """)
                mail_choice = input("Please make a choice:")
                if int(mail_choice) == 1:
                    sender_mail = input("Please enter your sender mail:")
                elif int(mail_choice) == 2:
                    sender_mail_passwd = input("Please enter your sender mail's password which is an app key:")
                elif int(mail_choice) == 3:
                    receiver_mail = input("Which mail will recieve the sended mail ?:")
                elif int(mail_choice) == 4:
                    print("Your settings are being saved..")
                    scraper.save_send_mail_info(sender_mail,sender_mail_passwd,receiver_mail)
                    break
        elif int(choice) == 4:
            print("Thanks for using my app, fiverr/linuxkerem")
            scraper.close_driver()
            break
        else:
            print("Please make a choice.")