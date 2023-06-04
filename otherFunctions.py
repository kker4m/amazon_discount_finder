from requiredLibraries  import *
global seperator
from sys import platform

if platform == 'linux':
    seperator = str(os.path.sep)
else:
    seperator = str(os.path.sep) + str(os.path.sep)

_E = False
_D = 'VARIABLES'
_C = 'utf-8-sig'
_B = 'data.ini'
_A = True


def waitElement(driver,xpath,sec=10):
    try:
        WebDriverWait(driver, sec).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except Exception as e:
        return False


def getParentFolder():
    from sys import platform
    if platform == 'win32':
        A = '\\'
        import sys, pathlib
        if getattr(sys, 'frozen', _E):
            current_direct = str(pathlib.Path(sys.executable).parent.resolve()) + A;parantez = str(current_direct)[:-1][
                                                                                               ::-1].find(
                A);parentFolder = str(current_direct)[:-1][::-1][parantez:][::-1]
        elif __file__:
            current_direct = str(pathlib.Path(__file__).parent.resolve()) + A;parantez = str(current_direct)[:-1][
                                                                                         ::-1].find(
                A);parentFolder = str(current_direct)[:-1][::-1][parantez:][::-1]
        return parentFolder
    elif platform == 'linux':
        from pathlib import Path
        parentFolder = Path(Path.cwd()).parent
        parentFolder = str(parentFolder) + '/'
        return str(parentFolder)


global parentFolder
parentFolder = getParentFolder()

def uyu():
    from random import randint
    delay = str(randint(1, 6)) + '.' + str(randint(1, 1000))
    time.sleep(float(delay))


def scroll_down_page(driver, speed=15):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script(
            'window.scrollTo(0, {});'.format(current_scroll_position))
        new_height = driver.execute_script('return document.body.scrollHeight')


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end='')
        time.sleep(1)
        t -= 1


def scrollDown(driver, pixels): currentScroll = driver.execute_script(
    'return  window.pageYOffset'); driver.execute_script('window.scrollTo(0, {})'.format(currentScroll + pixels))

def openNewTab(driver): driver.execute_script(
    "window.open('');"); mainTab = driver.window_handles[0]; newTab = driver.window_handles[-1]; return mainTab, newTab


if __name__ == '__main__':
    pass
