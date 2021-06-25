
import xml.sax

class XMLHandler(xml.sax.ContentHandler):

   def __init__(self):
        self.CurrentData = ""
        self.title= ""
        self.id   = ""
        self.updated= ""
        self.name = ""
        self.uri = ""
        self.language= ""
        self.issued = ""
  
  def startElement(self, tag,attributes):
       self.CurrentData = tag
       if tag == "entry":
          print("---entry---")
          title= attributes["title"]
          print("Name:", title)

  def endElement(self, tag):
     # if self.CurrentData == "title":
      #    print("title:", self.title)
      elif self.CurrentData == "id":
          print("id:", self.id)
      elif self.CurrentData == "updated":
          print("updated:", self.updated)
      elif self.currentData == "name":
          print("name:", self.name)
      elif self.CurrentData == "uri":
          print("uri:", self.uri)
      elif self.CurrentData == "language":
          print("language:", self.language)
      elif self.CurrentData == "issued":
          print("issued:", self.issued)

      self.CurrentData = ""

  def characters(self, content):
      #if self.CurrentData == "title":
       #   self.title = content
      if self.CurrentData == "id":
          self.id = content
      if self.CurrentData == "updated":
          self.updated = content
      if self.currentData == "name":
          self.name = content
      if self.CurrentData == "uri":
          self.uri = content
      if self.CurrentData == "language":
          self.language = content
      if self.CurrentData == "issued":
          self.issued = content

if (__name__ == "__main__"):
    parser =xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    
    Handler = XMLHandler()
    parser.setContentHandler(Handler)

    parser.parse("opds.xml")

