class Navigation:

    
    def getNext(self, start, numRows, numFound, urlBase):
        url   = None
        title = None

        if None == start:
            return url, title

        if (start+1)*numRows < numFound:
            title = 'Next results'
            url = '%s%d' % (urlBase, start+1)
    
        return url, title        

    
    def getPrev(self, start, numRows, numFound, urlBase):
        url   = None
        title = None

        if None == start:
            return url, title

        if 0 != start:
            title = 'Prev results'
            url = '%s%d' % (urlBase, start-1)
    
        return url, title        

    
    def initWithBaseUrl(cls, start, numRows, numFound, urlBase):
        (nextLink, nextTitle) = cls.getNext(start, numRows, numFound, urlBase)
        (prevLink, prevTitle) = cls.getPrev(start, numRows, numFound, urlBase)
        return cls(nextLink, nextTitle, prevLink, prevTitle)
    

    def __init__(self, nextLink, nextTitle, prevLink, prevTitle):
        self.nextLink  = nextLink
        self.nextTitle = nextTitle
        self.prevLink  = prevLink
        self.prevTitle  = prevTitle


if __name__ == '__main__':
    import doctest
    doctest.testmod()
