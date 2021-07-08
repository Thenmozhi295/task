class Catalog:

  

    def __init__(self, title, urn, url, author, authoruri):
                
        self._entries    = []
        self._navigation = None
        self._title      = title
        self._urn        = urn
        self._url        = url
        self._author     = author
        self._authorUri  = authorUri
       
    
    def addentry(self, entry):
        self._entries.append(entry)
    
    def addNavigation(self, nav):
        self._navigation = nav


    def getEntries(self):
        return self._entries
