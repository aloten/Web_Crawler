""" Aidan Loten, 11/11/2020, Web Scraping Code
"""

import sys
from filters import filter_urls, filter_emails, filter_phones
import requests


class WebPage:

    def __init__(self, url):
        """
        Initializes a WebPage's state with the url, and populates:
        - the set of urls in the WebPages's source
        - the set of emails in the WebPages's source
        - the set of phone numbers in the WebPages's source
        Args:
            url (str): the url to search
        """
        self.url = url
        self.urls = set()
        self.emails = set()
        self.phones = set()
        self.populate()

    def __hash__(self):
        """Return the hash of the URL"""
        return hash(self.url())

    def __eq__(self, page):
        """
        return True if and only if the url of this page equals the url
        of page.
        Args:
            page (WebPage): a WebPage object to compare
        """
        return self.url() == page.url()

    def populate(self):
        """
        fetch this WebPage object's webpage text and populate its content
        """
        r = requests.get(self.url)
        if r.status_code == requests.codes.ok:
            self.urls = set(filter_urls(r.text))
            self.emails = set(filter_emails(r.text))
            self.phones = set(filter_phones(r.text))            
            

    def url(self):
        """return the url asssociated with the WebPage"""
        return self.url

    def phones_set(self):
        """return the phone numbers associated with the WebPage"""
        return self.phones

    def emails_set(self):
        """return the email addresses associated with the WebPage"""
        return self.emails

    def urls_set(self):
        """return the URLs associated with the WebPage"""
        return self.urls

class WebCrawler:
    def __init__(self, base_url, max_links=50):
        """
        Initialize the data structures required to crawl the web.
        Args:
           base_url (str): the starting point of our crawl
           max_links (int): after traversing this many links, stop the crawl
        """
        self.base_url = base_url
        self.max_links = max_links
        self._all_emails = set()
        self._all_urls = set()
        self._all_phones = set()
        self.visited_pages = []
        self.crawl()

    def crawl(self):
        """
        starting from self._base_url and until stopping conditions are met,
        creates WebPage objects and recursively explores their links.
        """
        counter = 0
        to_visit = [self.base_url]
        while counter != self.max_links:
            if to_visit[0] in self.visited_pages:
                to_visit.pop(0)
                
            else:
                w = WebPage(to_visit[0])
                for item in list(w.urls_set()):
                    to_visit.append(item)
                self._all_urls = self._all_urls.union(w.urls_set()) 
                self._all_emails = self._all_emails.union(w.emails_set()) 
                self._all_phones = self._all_phones.union(w.phones_set()) 
                self.visited_pages.append(to_visit[0])
                to_visit.pop(0)
                counter += 1

    def all_emails(self):
        """
        returns the set of all email addresses harvested during a
        successful crawl
        """
        return self._all_emails

    def all_phones(self):
        """
        returns the set of all phone numbers harvested during a
        successful crawl
        """
        return self._all_phones

    def all_urls(self):
        """
        returns the set of all urls traversed during a crawl
        """
        return self._all_urls

    def output_results(self, filename):
        """
        In an easy-to-read format, writes the report of a successful crawl
        to the file specified by 'filename'.
        This includes the starting url, the set of urls traversed,
        all emails encountered, and the set of phone numbers (recorded in
        a standardized format of NPA-NXX-XXXX).
        """
        file = open(filename, 'w')
        file.write("Base URL: " + self.base_url + "\n\n")
        file.write("URLs: \n")
        for url in self._all_urls:
            file.write(url + "\n")
        file.write("\nEmails: \n")
        for email in self._all_emails:
            file.write(email + "\n")
        file.write("\nPhones: \n")
        for phone in self._all_phones:
            file.write(phone + "\n")
        file.close()
        

def usage():
    print("python3 crawl.py <base_url> <report_file>")
    print("\tbase_url: the initial url to crawl")
    print("\treport_file: file where all results are written")

if __name__ == '__main__':

    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    base_url = sys.argv[1]
    report_path = sys.argv[2]

    crawl = WebCrawler(base_url, 15) # until you are confident use small max_links
    crawl.crawl()
    crawl.output_results(report_path)



w = WebCrawler("https://bowdoin.edu")
w.output_results("data.txt")