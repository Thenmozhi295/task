class entry():

    
    valid_keys = {
        'urn'                 : unicode, 
        'url'                 : unicode, 
        'title'               : unicode, 
        'content'             : unicode, 
        'updated'             : unicode,
        'publishers'          : list,
        'languages'           : list, 
        'authors'             : list,        
        'formats'             : list,
    }
        
    required_keys = ('urn', 'title')
    
    def validate(self, key, value):
        if key not in self.valid_keys:
            raise KeyError("invalid key in book.catalog.Entry: %s" % (key))

        wantedType = self.valid_keys[key]
        
        gotType = type(value)
        if not gotType == wantedType:
            error = True
            if unicode == wantedType:
                
                if str == gotType or int == gotType:
                    error = False
            
            if error:
                raise ValueError("invalid value in book.catalog.Entry: %s=%s should have type %s, but got type %s" % (key, value, wantedType, gotType))
    

    def __init__(self, obj, links=None):

        
        if not type(obj) == dict:
            raise TypeError("book.catalog.Entry takes a dict argument!")
        
        for key, val in obj.iteritems():
            self.validate(key, val)

        if 'title' not in obj:
            obj['title'] = '(no title)' 

        for req_key in Entry.required_keys:
            if not req_key in obj:
                raise KeyError("required key %s not supplied!" % (req_key))

        if not links:
            raise KeyError("links not supplied!")

        self._entry = copy.deepcopy(obj)
        self._links = links
                

    def get(self, key):
        if key in self._entry:
            return self._entry[key]
        else:
            if key in self.valid_keys:
                if list == self.valid_keys[key]:
                    return []
                else:
                    return None
            else:
                raise KeyError("requested key %s is not valid in Entry" % key)

    def set(self, key, value):
        self.validate(key, value)
        self._entry[key] = value


    def getLinks(self):
        return self._links


class Entry(entry):
   
    valid_keys = entry.valid_keys.copy()
    valid_keys['formats'] = list

if __name__ == '__main__':
    import doctest
    doctest.testmod()
