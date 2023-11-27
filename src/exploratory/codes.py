import os
import requests
from bs4 import BeautifulSoup
from git import Repo

head_url = "https://fortran-lang.org/packages/"
target_url = "https://github.com/"


def scrape_code_urls():
    """
    Get url to all repos mentioned on fortran-lang.org/packages
    """
    
    # Initialize list of urls and 
    urls = []
    seen = set()
    
    # Iterate over all <a> tags on fortran-lang.org/packages
    req = requests.get(head_url)
    soup = BeautifulSoup(req.text, 'html.parser')
    for link in soup.find_all('a'):
        
        # Scrape url and ensure it points to desired page
        url = link.get('href')
        if url is None: continue
        cls = link.get('class')
        if cls is None or len(cls) != 2: continue
        if cls[0] != "reference" or cls[1] != "internal": continue
        sub_url = head_url + url
        
        # Iterate over all <a> tags on desired page
        req = requests.get(sub_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        for link in soup.find_all('a'):
            
            # Scrape url and ensure it points to github.com
            url = link.get('href')
            if url is None: continue
            if not url.startswith(target_url): continue
            cls = link.get('class')
            if cls is None or len(cls) != 2: continue
            if cls[0] != "reference" or cls[1] != "external": continue

            # Add url to list if it has not been seen before
            url = url[len(target_url) :]
            if url in seen: continue
            urls.append(url)
            seen.add(url)
            
    return urls
        
        
def init_codes(rootdir : str):
    """
    Clone all repos mentioned on fortran-lang.org/packages to file
    """
    
    # Iterate over all distinct github.com urls from fortran-lang.org/packages
    urls = scrape_code_urls()
    print("{} urls found".format(len(urls)))
    for url in urls:
        print(url)
        
        # Absolute url and relative directory path
        repo_url = target_url + url
        repo_dir = rootdir + '/' + url

        # Clone repo if it does not exist on file
        if os.path.exists(repo_dir): continue
        os.makedirs(repo_dir)
        Repo.clone_from(repo_url, repo_dir)            


if __name__ == "__main__":
    
    # Initialize codes
    rootdir = "codes"
    init_codes(rootdir)