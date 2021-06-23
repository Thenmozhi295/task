from enum import Enum
from typing import  List
from datetime import datetime


from xml.dom import minidom


class Author:

   def __init__(self, name=None, uri=None):
        self.name = name
        self.uri = uri


class Prefix(Enum):
    DC = "dc"


class Issued:
    

    def __init__(self, prefix=None, text=None):
        self.prefix = prefix
        self.text = text


class Link:
   

    def __init__(self, rel=None, href=None, type=None, title=None):
        self.rel = rel
        self.href = href
        self.type = type
        self.title = title


class Entry:
    

    def __init__(self, title=None, id=None, updated=None, language=None, issued=None, link=None, author=None):
        self.title = title
        self.id = id
        self.updated = updated
        self.language = language
        self.issued = issued
        self.link = link
        self.author = author



class Feed:
    def __init__(self, id=None, link=None, title=None, updated=None, author=None, entry=None, xmlns=None, xmlns_dc=None, xmlns_opds=None):
        self.id = id
        self.link = link
        self.title = title
        self.updated = updated
        self.author = author
        self.entry = entry
        self.xmlns = xmlns
        self.xmlns_dc = xmlns_dc
        self.xmlns_opds = xmlns_opds    



   





  

