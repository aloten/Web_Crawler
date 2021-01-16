""" Aidan Loten, 11/11/2020, Web Scraping Code
"""

import re

EXTS = ["jpg", "jpeg", "svg", "png", "pdf",
        "gif", "bmp", "mp3", "dvi"]

# '<a' + _not >_ + 'href=' + _quote_ + 'http://' + _nonquote_ + _quote_
URL_REGEX = '''<a[^>]+href\s*=\s*["'](https://\S+{}\.{}[^"']+?)["']'''

def filter_urls(text, domain='bowdoin.edu'):
    """
    returns a list of urls found in the string 'text'
    """
    def extension_is_valid(url):
        """ Checks if the potential URL is valid.
        Media files, for example, are not.
        """
        EXTS = ["jpg", "jpeg", "svg", "png", "pdf",
                "gif", "bmp", "mp3", "dvi"]
        for e in EXTS:
            if url.lower().endswith(e):
                return False
        return True

    domain, tld = domain.split(".")
    regex = re.compile(URL_REGEX.format(domain, tld))

    urls = re.findall(regex, text)
    return [url for url in urls if extension_is_valid(url)]


def filter_emails(text):
    """
    returns a list of emails found in the string 'text'
    """
    emails = re.findall(r'\w+@\w+\.\w+', text)
    return emails
    

def filter_phones(text):
    """
    returns a list of uniformly formatted phone numbers extracted from
    the string 'text'
    """
    
    phones = re.findall(r'[(]?\d{3}[\s]?[)-.][\s]?[2-9]\d{2}[\s]?[-.][\s]?\d{4}\b', text)
    phones_new = []
    for phone in phones:
        phone = phone.replace('.', '-').replace('(', '').replace(')', '-').replace(' ', '')
        phones_new.append(phone)
    return phones_new
