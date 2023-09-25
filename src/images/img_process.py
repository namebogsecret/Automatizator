#/src/images/img_process.py
from urllib.parse import urlparse

def get_img_url(url, pars = True):
    parsed_url = urlparse(url)
    path = parsed_url.path
    # Удаление параметров из URL-адреса, если они есть
    #print (path)
    if '-' in path and pars:
        path = path.split('-')[0]
        #print(path)
    if path.startswith('//'):
        path = path[2:]
        #print(path)
        #print (parsed_url.netloc)
    file_url = f"https://{parsed_url.netloc}{path}"
    return file_url


def __main__():
    """print (get_img_url(url1))
    print (get_img_url(url2))
    print (get_img_url(url3))"""
    

if __name__ == "__main__":
    __main__()
