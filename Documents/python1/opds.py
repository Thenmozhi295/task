from catalog import catalog
from entry import entry
from navigation import navigation
from link  import link

import lxml.etree as ET
import re

import sys
import feedparser 
import datetime
import string
import opensearch

class CatalogRenderer:

    def __init__(self):
        pass
        
    def toString(self):
        return ''
        
    def prettyPrintET(self, etNode):
        return ET.tostring(etNode, pretty_print=True)

class CatalogToAtom(CatalogRenderer):
    xmlns_atom    = 'http://www.w3.org/2005/Atom'
    xmlns_dcterms = 'http://purl.org/dc/terms/'
    xmlns_opds    = 'http://opds-spec.org/'
    
    atom          = "{%s}" % xmlns_atom
    dcterms       = "{%s}" % xmlns_dcterms
    opdsNS        = "{%s}" % xmlns_opds
    
    nsmap = {
        None     : xmlns_atom,
        'dcterms': xmlns_dcterms,
        'opds'   : xmlns_opds
    }
    
    fileExtMap = {
        'pdf'  : 'application/pdf',
        'epub' : 'application/epub+zip',
        'mobi' : 'application/x-mobipocket-ebook'
    }
    
    ebookTypes = ('application/pdf',
                  'application/epub+zip',
                  'application/x-mobipocket-ebook'
    )
   def createTextElement(self, parent, name, value):
        element = ET.SubElement(parent, name)
        element.text = value
        return element

   def createRelLink(self, parent, rel, urlroot, relurl, title=None, type='application/atom+xml'):
        absurl = urlroot + relurl
        element = ET.SubElement(parent, 'link')
        element.attrib['rel']  = rel
        element.attrib['type'] = type
        element.attrib['href'] = absurl;
        if title:
            element.attrib['title'] = title;

   def createOpdsRoot(self, c):
        
        opds = ET.Element(CatalogToAtom.atom + "feed", nsmap=CatalogToAtom.nsmap)                    
        
        self.createTextElement(opds, 'title',    c._title)

        self.createTextElement(opds, 'id',       c._urn)
    
        self.createTextElement(opds, 'updated',  c._datestr)
        
        self.createRelLink(opds, 'self', c._url, '')
        
        author = ET.SubElement(opds, 'author')
        self.createTextElement(author, 'name',  c._author)
        self.createTextElement(author, 'uri',   c._authorUri)
        
        if c._catalog:
            self.createRelLink(opds, 'http://opds-spec.org/2010/catalog', c._caralog, '', ' feed')
            
        return opds

    def createOpdsLink(self, entry, link):
        element = ET.SubElement(entry, 'link')
        element.attrib['href'] = link.get('url')
        element.attrib['type'] = link.get('type')
        if link.get('rel'):
            element.attrib['rel']  = link.get('rel')
  

        if link.get('formats'):
            for format in link.get('formats'):
                self.createTextElement(element, CatalogToAtom.dcterms+'hasFormat', format)
            
   
   def createOpdsEntry(self, opds, obj, links, ContentElement):
        entry = ET.SubElement(opds, 'entry')
        self.createTextElement(entry, 'title', obj['title'])
    
        self.createTextElement(entry, 'id',       obj['urn'])
    
        self.createTextElement(entry, 'updated',  obj['updated'])
    
        downloadLinks = []
        for link in links:
            self.createOpdsLink(entry, link)
            if link.get('type') in CatalogToAtom.ebookTypes:
                downloadLinks.append(link)
                    
        if 'date' in obj:
            element = self.createTextElement(entry, self.dcterms+'issued',  obj['date'][0:4])
    
        if 'authors' in obj:
            for author in obj['authors']:
                element = ET.SubElement(entry, 'author')
                self.createTextElement(element, 'name',  author)
                
        if 'publishers' in obj: 
            for publisher in obj['publishers']:
                element = self.createTextElement(entry, self.dcterms+'publisher', publisher)
    
        if 'languages' in obj:
            for language in obj['languages']: 
                element = self.createTextElement(entry, self.dcterms+'language', language);
        
        if 'content' in obj:
            self.createTextElement(entry, 'content',  obj['content'])
        elif fabricateContentElement:
           
            contentText=''
        
            if 'authors' in obj:
                if 1 == len(obj['authors']):
                    authorStr = '<b>Author: </b>'
                else:
                    authorStr = '<b>Authors: </b>'
                
                authorStr += ', '.join(obj['authors'])
                contentText += authorStr + '<br/>'
   
        
            if 'publishers' in obj:
                contentText += '<b>Publisher: </b>' + ', '.join(obj['publishers']) + '<br/>'
                
            if 'date' in obj:
                contentText += '<b>Year published: </b>' + obj['date'][0:4] + '<br/>'
        
            if 'contributors' in obj:
                contentText += '<b>Book contributor: </b>' + ', '.join(obj['contributors']) + '<br/>'
        
            if 'languages' in obj:
                contentText += '<b>Language: </b>' + ', '.join(obj['languages']) + '<br/>'
       

            if 'provider' in obj:
                contentText += '<b>Provider: </b>' + obj['provider'] + '<br/>'

            if len(downloadLinks):
                contentText += '<b>Download Ebook: </b>'
                for link in downloadLinks:
                    (start, sep, ext) = link.get('url').rpartition('.')
                    contentText += '(<a href="%s">%s</a>) '%(link.get('url'), ext.upper())

        
            element = self.createTextElement(entry, 'content',  contentText)
            element.attrib['type'] = 'html' 


     def createNavLinks(self, opds, nav):        
        if nav.prevLink:
            self.createRelLink(opds, 'prev', '', nav.prevLink, nav.prevTitle)

        if nav.nextLink:
            self.createRelLink(opds, 'next', '', nav.nextLink, nav.nextTitle)

   
     def __init__(self, c, ContentElement=False):
        CatalogRenderer.__init__(self)
        self.opds = self.createOpdsRoot(c)

        if c._opensearch:
            self.createOpenSearchDescription(self.opds, c._opensearch)

        if c._navigation:
            self.createNavLinks(self.opds, c._navigation)

        for e in c._entries:
            self.createOpdsEntry(self.opds, e._entry, e._links, ContentElement)

   def toString(self):
        return self.prettyPrintET(self.opds)


   def toElementTree(self):
        return self.opds



class CatalogToHtml(CatalogRenderer):
 
     entryDisplayKeys = [
        'authors',
        'date',
        'publishers',
        'formats',
        'contributors',
        'languages'
    ]
   
    entryDisplayTitles = {
        'authors': ('Author', 'Authors')
        'date': ('Published', 'Published'),
        'formats': ('Format', 'Formats'),
        'languages': ('Language', 'Languages'),
        'publishers': ( 'Publisher', 'Publishers'),
        'title': ('Title', 'Title')
    }
    
    entryLinkTitles = {
        'application/pdf': 'PDF',
        'application/epub': 'ePub',
        'application/epub+zip': 'ePub',
        'application/x-mobipocket-ebook': 'Mobi',
        'text/html': 'Website',
    }

   def __init__(self, catalog, device = None, query = None):
        CatalogRenderer.__init__(self)
        self.device = device
        self.query = query
        self.processCatalog(catalog)
        
    def processCatalog(self, catalog):
        html = self.createHtml(catalog)
        html.append(self.createHead(catalog))
        body = self.createBody(catalog)
        html.append(body)
        body.append(self.createHeader(catalog))
        body.append(self.createSearch(catalog._opensearch, query = self.query))
        body.append(self.createCatalogHeader(catalog))
        body.append(self.createNavigation(catalog._navigation))
        body.append(self.createEntryList(catalog._entries))
        body.append(self.createNavigation(catalog._navigation))
        body.append(self.createFooter(catalog))
        
        self.html = html
        return self
        
    def createHtml(self, catalog):
        return ET.Element('html')
        
    def createHead(self, catalog)
   
        head = ET.Element('head')
        titleElement = ET.SubElement(head, 'title')
        titleElement.text = catalog._title
        head.append(self.createStyleSheet('/static/catalog.css'))
        
        return head
                
     def createStyleSheet(self, url):
        
         return ET.Element('link', {
            'rel':'stylesheet',
            'type':'text/css', 
            'href':url
        })
        
    def createBody(self, catalog):
        return ET.Element('body')


       
    def createHeader(self, catalog):
        div = ET.Element( 'div', {'class':'opds-header'} )
        div.text = 'Catalog Header'
        return div

    def createNavigation(self, navigation):

        div = ET.Element( 'div', {'class':'opds-navigation'} )
        if not navigation:
            return div

         nextLink, nextTitle = navigation.nextLink, navigation.nextTitle
        prevLink, prevTitle = navigation.prevLink, navigation.prevTitle
        
        if (prevLink):
            prevA = self.createNavigationAnchor('prev', navigation.prevLink, navigation.prevTitle)
            div.append(prevA)
            else:
              pass

           if (nextLink):
            nextA = self.createNavigationAnchor('next', navigation.nextLink, navigation.nextTitle)
            div.append(nextA)
        else:
            pass
        
        return div

     def createNavigationAnchor(self, rel, url, title = None):

         if url.endswith('.xml'):
            url = url[:-4]
        if not url.endswith('.html'):
            url += '.html'
        
        attribs = {'class':'opds-navigation-anchor',
            'rel': rel,
            'href': url}
        if title is not None:
            attribs['title'] = title    
        a = ET.Element('a', attribs)
        
        if title is not None:
            a.text = title
        return a

     def createSearch(self, opensearchObj, query = None):
        div = ET.Element( 'div', {'class':'opds-search'} )
        
        osUrl = opensearchObj.osddUrl
        desc = opensearch.Description(osUrl)
        url = desc.get_url_by_type('application/atom+xml')
        if url is None:
            c = ET.Comment()
            c.text = " Could not load OpenSearch description from %s " % osUrl
            div.append(c)
        else:
            template = url.template


     def createCatalogHeader(self, catalog):
        div = ET.Element( 'div', {'class':'opds-catalog-header'} )
        title = ET.SubElement(div, 'h1', {'class':'opds-catalog-header-title'} )
        title.text = catalog._title 
        return div
   
      def createEntry(self, entry):

         e = ET.Element('p', { 'class':'opds-entry'} )
        
        elem = e        
        catalogLink = self.findCatalogLink(entry._links)
        if catalogLink:
            entry._links.remove(catalogLink)
            a = ET.SubElement(e, 'a', { 'class':'opds-entry-title', 'href':catalogLink.get('url') } )
            elem = a
        
        title = ET.SubElement(elem, 'h2', {'class':'opds-entry-title'} )
        title.text = entry.get('title')
        
        for key in self.entryDisplayKeys:
            value = entry.get(key)
            if value:
                displayTitle, displayValue = self.formatEntryValue(key, value)
                
                entryItem = ET.SubElement(e, 'span', {'class':'opds-entry-item'} )
                itemName = ET.SubElement(entryItem, 'em', {'class':'opds-entry-key'} )
                itemName.text = displayTitle + ':'
                itemName.tail = ' '
                itemValue = ET.SubElement(entryItem, 'span', {'class': 'opds-entry-value' } )
                itemValue.text = unicode(displayValue)
                ET.SubElement(entryItem, 'br')

        if entry._links:
            e.append(self.createEntryLinks(entry._links)
        
           return e

    def formatEntryValue(self, key, value):
        if type(value) == type([]):
            if len(value) == 1:
                displayTitle = self.entryDisplayTitles[key][0]
                displayValue = value[0]
                               
            else:
               
                displayTitle = self.entryDisplayTitles[key][1]
                displayValue = ', '.join(value)
        else:
           
            displayTitle = self.entryDisplayTitles[key][0]
            displayValue = value
            if 'date' == key: 
                displayValue = displayValue[:4]

        return (displayTitle, displayValue)


    def createEntryLinks(self, links):
    
       free = []
       opds = [] 
       html = []

       d = ET.Element('div', {'class':'opds-entry-links'} )
        
        for link in links:
            try:
                rel = link.get('rel')
                type = link.get('type')
            except KeyError:
                continue

               if rel == Link.acquisition:
                free.append(link)
               elif type == Link.opds:
                opds.append(link)
               elif type == Link.html:
                 html.append(link)

         linkTuples = [(free, 'Free:'),(opds, 'Catalog:'), (html, 'HTML:')]

        for (linkList, listTitle) in linkTuples:
            if len(linkList) > 0:
                s = ET.Element('span', { 'class':'opds-entry-item' } )
                title = ET.SubElement(s, 'em', {'class':'opds-entry-key'} )
                title.text = listTitle
                title.tail = ' '
                
                linkElems = [self.createEntryLink(aLink) for aLink in linkList]
                for linkElem in linkElems:
                    s.append(linkElem)
                    if linkElem != linkElems[-1]:
                        linkElem.tail = ', '
                        
                d.append(s)
                        
        return d

     def createEntryLink(self, link):

        if self.device:
            link = self.device.formatLink(link)
        
        if self.entryLinkTitles.has_key(link.get('type')):
            title = self.entryLinkTitles[link.get('type')]
        else:
            title = link.get('url')
            
        attribs = {'class':'opds-entry-link',
            'href' : link.get('url')
        }
      
        a = ET.Element('a', attribs)
        a.text = title
        return a

    def createEntryKey(self, key, value):

         if not value:
            return None
        e = ET.Element('span', { 'class': 'opds-entry' })
        keyName = ET.SubElement(e, 'em', {'class':'opds-entry-key'})
        keyName.text = unicode(key, 'utf-8') + ':'
        keyName.tail = ' '
        keyValue = ET.SubElement(e, 'span', { 'class': 'opds-entry-value opds-entry-%s' % key })
        keyValue.text = unicode(value)
        ET.SubElement(e, 'br')
        return e
        
     def createEntryList(self, entries):
        list = ET.Element( 'ul', {'class':'opds-entry-list'} )
        for entry in entries:
            item = ET.SubElement(list, 'li', {'class':'opds-entry-list-item'} )
            item.append(self.createEntry(entry))
            list.append(item)
        return list

    def findCatalogLink(cls, links):
         if links:
            for link in links:
                try:
                    linkType = link.get('type')
                except KeyError:
                    continue
                
                if Link.opds == linkType:
                    return link
        return None

    def toString(self):
        return self.prettyPrintET(self.html)


       

    
      
        


    
  
