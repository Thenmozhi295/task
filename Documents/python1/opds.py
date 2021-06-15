
from datetime import datetime
from PIL import Image


class Catalog(object):

    def __init__(self, title, author_name=None):
       
        self.title = title
        
        self.author_name = author_name
        
        self.entries = []

    def add_entry(self, title,urls, uuid=None, summary=None,
                  author_name=None,
                  image=None, updated=None,
                  rights=(), languages=('eng', )):
       
        self.entries.append(dict(
            id=id,
            uuid=uuid,
            title=title,
            
            updated=updated or issued,
            rights=rights,
            urls=urls,
            summary=summary,
            author_name=author_name,
            
            image=image,
            
            languages=languages,
            )


def to_opds(catalog, url, root_url=None, updated=None, uuid=None):
   
    updated = updated or datetime.now()
    uuid = uuid or uuid4()
    root_url = root_url or url
return()

catalog = Catalog(title=title, **options)
catalog.add_entry(
  uuid='88df7295-5071-4438-a390-e6df64669fb4',
  title='cheran_senguttuvan'
  updated=datetime.datetime(2019, 03, 00),
  languages=('en', 'Tamil')
  urls={'application/atom+xml;profile=opds-catalog;kind=navigation': 'http://opds-catalogs/cheran_senguttuvan.xml'},
 )

return to_opds(catalog, url)
