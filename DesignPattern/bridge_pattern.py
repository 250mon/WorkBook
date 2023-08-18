"""
Bridget Pattern

In the software realm, device drivers are often cited as
an example of the bridge pattern, when the developers of
an OS defines the interface for device vendors to implement it.

Let's assume we are building an application where the user is
going to manage and deliver content after fetching it from
diverse sources, which could be:

- web page (based on its URL)
- resource accessed on an FTP server
- file on the local file system
- database server

So, here is the idea: instead of implementing several content
classes, each holding the methods responsible for getting the
content pieces, assembling them, and showing them inside the
application, we can define an abstraction for the Resource
Content and a separate interface for the objects that are
responsible for fetching the content
"""
import abc
from urllib import request


class ResourceContent:
    """
    Define teh abstraction's interface
    Maintain a reference to an object which represents the Implementor
    """

    def __init__(self, imp):
        self._imp = imp

    def show_content(self, path):
        self._imp.fetch(path)


"""
we define the equivalent of an interface in Python using two features
of the language,
1. the metaclass feature (which helps define the type of a type), 
2. abstract base classes (ABC):
"""


class ResourceContentFetcher(metaclass=abc.ABCMeta):
    """
    Define the interface for implementation classes that fetch content
    """

    @abc.abstractmethod
    def fetch(self, path):
        pass


"""
Now, we can add an implementation class to fetch content from a web page
or resource:
"""

class URLFetcher(ResourceContentFetcher):
    # Implementation 1
    """
    Implement the Implementor interface and define its concrete
    implementation.
    """

    def fetch(self, path):
        # path is an URL
        req = request.Request(path)
        with request.urlopen(req) as response:
            if response.code == 200:
                the_page = response.read()
                print(the_page)


class LocalFileFetcher(ResourceContentFetcher):
    """
    Implement the Implementor interface and define its concrete
    implementation.
    """

    def fetch(self, path):
        # path is teh filepath to a text file
        with open(path) as f:
            print(r.read())


def main():
    url_fetcher = URLFetcher()
    iface = ResourceContent(url_fetcher)
    iface.show_content('http://pytho.org')

    print('========================')

    localfs_fetcher = LocalFileFetcher()
    iface = ResourceContent(localfs_fetcher)
    iface.show_content('file.text')