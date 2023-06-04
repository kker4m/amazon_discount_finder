from otherFunctions import *

class ChromeWithPrefs(webdriver.Chrome):
    def __init__(self, *args, options=None,useData=True,**kwargs):
        if options:
            self.handle_prefs(options,useData)

        super().__init__(*args, options=options, **kwargs)

        # remove the user_data_dir when quitting
        if useData:
            self.keep_user_data_dir = True
        else:
            self.keep_user_data_dir = False
    @staticmethod
    def handle_prefs(options,useData = True):
        if prefs := options.experimental_options.get("prefs"):
            # turn a (dotted key, value) into a proper nested dict
            def undot_key(key, value):
                if "." in key:
                    key, rest = key.split(".", 1)
                    value = undot_key(rest, value)
                return {key: value}

            # undot prefs dict keys
            undot_prefs = reduce(lambda d1, d2: {**d1, **d2},  # merge dicts
                (undot_key(key, value) for key, value in prefs.items()), )

            if useData:
                # create an user_data_dir and add its path to the options
                user_data_dir = "chromeLog"
                options.add_argument(f"--user-data-dir={user_data_dir}")

                # create the preferences json file in its default directory
                default_dir = os.path.join(user_data_dir, "Default")
                # os.mkdir(default_dir)

                prefs_file = os.path.join(default_dir, "Preferences")
                with open(prefs_file, encoding="latin1", mode="w") as f:
                    json.dump(undot_prefs, f)

                # pylint: disable=protected-access
                # remove the experimental_options to avoid an error
                del options._experimental_options["prefs"]


class wireChromeWithPrefs(seleniumWireWebdriver.Chrome):
    def __init__(self, *args, options=None,useData=True,**kwargs):
        if options:
            ChromeWithPrefs.handle_prefs(options,useData)

        super().__init__(*args, options=options,useData=useData, **kwargs)

        if useData:
            self.keep_user_data_dir = True
        else:
            self.keep_user_data_dir = False

def callUcDriver(proxy=None, headless=False, useData=True,pageLoadStrategy='eager'):
    prefs = {'intl.accept_languages': 'en,en_US'}
    caps = DesiredCapabilities().CHROME
    if proxy != None:
        if type(proxy) != list:
            proxy = proxy.split(':')

        if len(proxy) > 2:
            IP = proxy[0]
            port = proxy[1]
            username = proxy[2]
            password = proxy[3]
            useAuth = True
        else:
            IP = proxy[0]
            port = proxy[1]
            useAuth = False

        if useAuth:
            wireOptions = {'proxy': {'http': 'http://' + username + ':' + password + '@' + IP + ':' + port,
                'https': 'https://' + username + ':' + password + '@' + IP + ':' + port,
                'no_proxy': 'localhost,127.0.0.1'}}
        else:
            wireOptions = {'proxy': {'http': 'http://@' + IP + ':' + port,
                'https': 'https://@' + IP + ':' + port,
                'no_proxy': 'localhost,127.0.0.1'}}

    caps["pageLoadStrategy"] = pageLoadStrategy
    op = webdriver.ChromeOptions()
    if headless:
        op.add_argument("--headless=new")

    op.add_argument('--ignore-certificate-errors')
    op.add_experimental_option("prefs", prefs)
    op.add_argument("--no-sandbox")
    op.add_argument("--dns-prefetch-disable")
    op.add_argument("--disable-gpu")
    op.add_argument("--disable-user-media-security=true")
    op.add_argument("--disable-popup-blocking")

    if proxy != None:
        driver = wireChromeWithPrefs(options=op,driver_executable_path="chromedriver",desired_capabilities=caps, seleniumwire_options=wireOptions,useData=useData)
    else:
        driver = ChromeWithPrefs(options=op,driver_executable_path="chromedriver",desired_capabilities=caps,useData=useData)

    return driver

if __name__ == "__main__":
    pass