from atom import AtomFeed
import mimetypes
import datetime

class Catalog():

    def __init__(self, atom_id, title, subtitle, root, search):
        self.atom_id = atom_id
        self.title = title
        self.subtitle = subtitle
        self.root = root
        self.search = search

class AcquisitionFeed(AtomFeed):

    def __init__(self, catalog, prev=None, next=None):
    
        links=[
                {'type': 'application/atom+xml;profile=opds-catalog;kind=navigation', 'rel': 'start', 'href': catalog.root, 'title': 'Home'},
            ]
        if prev is not None:
            links.append({'type': 'application/atom+xml;profile=opds-catalog;kind=acquisition', 'rel': 'previous', 'href': prev, 'title': 'Previous results'})
        if next is not None:
            links.append({'type': 'application/atom+xml;profile=opds-catalog;kind=acquisition', 'rel': 'next', 'href': next, 'title': 'Next results'})
        super(AcquisitionFeed, self).__init__(
            atom_id=catalog.atom_id,
            title=catalog.title,
            subtitle=catalog.subtitle,
            extra_attrs={
                'xmlns:opds': 'http://opds-spec.org/',
                'xmlns:opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
            },
            links=links,
            icon=catalog.icon)
        self.catalog = catalog
        self.generated = datetime.datetime.now()

    def addBookEntry(self, atom_id, title, published, summary, content_html, opds_url, authors=[], thumbnail=None, image=None, categories=[], html_url=None):
        
        links=[
                {'rel': 'http://opds-spec.org/acquisition', 'href': opds_url,'type': 'application/epub+zip'},
            ]
        
        if html_url is not None:
            links.append({'href': html_url})
        
        if image is not None:
            links.append({'href':image['url'], 'type':image['type'], 'rel':'http://opds-spec.org/image'})
		
        if thumbnail is not None:
            links.append({'href':thumbnail['url'], 'type':image['type'], 'rel':'http://opds-spec.org/image/thumbnail'})
		
        self.add_item(
            atom_id,
            title,
            self.generated,
            summary=summary,
            categories=categories,
            published=published,
            content=( {'type':'html'}, content_html ),
            links=links,
            authors=authors
        )

class RootAcquisitionFeed(AtomFeed):
    def __init__(self):
        super(RootAcquisitionFeed, self).__init__()
        raise NotImplementedError("TODO: Implement this class. Does someone really need a RootAcquisitionFeed? Probably not.")

class NavigationFeed():
    def __init__(self):
        raise NotImplementedError("TODO: Implement this class")

class RootNavigationFeed(AtomFeed):

    def __init__(self, catalog):
        super(RootNavigationFeed, self).__init__(
            atom_id=catalog.atom_id,
            title=catalog.title,
            subtitle=catalog.subtitle,
            extra_attrs={
                'xmlns:dcterms': 'http://purl.org/dc/terms/',
                'xmlns:opds': 'http://opds-spec.org/',
                'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
                'xmlns:opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
            },
            links=[
                {'type': 'application/atom+xml;profile=opds-catalog;kind=navigation', 'rel': 'self', 'href': catalog.root},
                {'type': 'application/atom+xml;profile=opds-catalog;kind=navigation', 'rel': 'start', 'href': catalog.root, 'title': 'Home'},
                {'type': 'application/opensearchdescription+xml', 'rel': 'search', 'href': catalog.search },
            ],
            icon=catalog.icon)
        self.generated = datetime.datetime.now()

    def addNavEntry(self, atom_id, title, url):
        raise NotImplementedError()
        
    def addAquisitionEntry(self, atom_id, title, url):
        self.add_item(atom_id, title, self.generated, links = [
            {'rel': 'subsection', 'type': 'application/atom+xml;profile=opds-catalog;kind=acquisition', 'href': url},
            {'rel': 'alternate', 'href': url}
        ])


