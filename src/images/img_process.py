
from urllib.parse import urlparse

def get_img_url(url, pars = True):
    '''The function `get_img_url` takes a URL as input and returns a modified version of the URL by
    removing any parameters and extracting the image path.
    
    Parameters
    ----------
    url
        The `url` parameter is the URL of the image you want to get the URL for.
    pars, optional
        The `pars` parameter is a boolean value that determines whether or not to parse the URL path. If
    `pars` is `True`, the function will remove any parameters from the URL path by splitting it at the
    '-' character and keeping only the first part. If `pars` is `False`,
    
    Returns
    -------
        The function `get_img_url` returns a modified URL string.
    
    '''
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
