from sqlite3 import *
import os
import re
import sys


def title_sort(title):
    title_pat = re.compile(config.config_title_regex, re.IGNORECASE)
    match = title_pat.search(title)
    if match:
        prep = match.group(1)
        title = title.replace(prep, '') + ', ' + prep
    return title.strip()


def lcase(s):
    return s.lower()


def ucase(s):
    return s.upper()


Base = declarative_base()


books_authors_link = Table('books_authors_link', Base.metadata,
    Column('book', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author', Integer, ForeignKey('authors.id'), primary_key=True)
    )

books_series_link = Table('books_series_link', Base.metadata,
    Column('book', Integer, ForeignKey('books.id'), primary_key=True),
    Column('series', Integer, ForeignKey('series.id'), primary_key=True)
    )

books_languages_link = Table('books_languages_link', Base.metadata,
    Column('book', Integer, ForeignKey('books.id'), primary_key=True),
    Column('lang_code', Integer, ForeignKey('languages.id'), primary_key=True)
    )

books_publishers_link = Table('books_publishers_link', Base.metadata,
    Column('book', Integer, ForeignKey('books.id'), primary_key=True),
    Column('publisher', Integer, ForeignKey('publishers.id'), primary_key=True)
    )


class Identifiers(Base):
    __tablename__ = 'identifiers'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    val = Column(String)
    book = Column(Integer, ForeignKey('books.id'))

    def __init__(self, val, id_type, book):
        self.val = val
        self.type = id_type
        self.book = book

    


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    book = Column(Integer, ForeignKey('books.id'))

    def __init__(self, text, book):
        self.text = text
        self.book = book

    def __repr__(self):
        return u"<Comments({0})>".format(self.text)


class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return u"<Tags('{0})>".format(self.name)


class Authors(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    sort = Column(String)
    link = Column(String)

    def __init__(self, name, sort, link):
        self.name = name
        self.sort = sort
        self.link = link

    def __repr__(self):
        return u"<Authors('{0},{1}{2}')>".format(self.name, self.sort, self.link)


class Languages(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    lang_code = Column(String)

    def __init__(self, lang_code):
        self.lang_code = lang_code

    def __repr__(self):
        return u"<Languages('{0}')>".format(self.lang_code)


class Publishers(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    sort = Column(String)

    def __init__(self, name, sort):
        self.name = name
        self.sort = sort

    def __repr__(self):
        return u"<Publishers('{0},{1}')>".format(self.name, self.sort)


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    book = Column(Integer, ForeignKey('books.id'))
    format = Column(String)
    uncompressed_size = Column(Integer)
    name = Column(String)

    def __init__(self, book, book_format, uncompressed_size, name):
        self.book = book
        self.format = book_format
        self.uncompressed_size = uncompressed_size
        self.name = name

    def __repr__(self):
        return u"<Data('{0},{1}{2}{3}')>".format(self.book, self.format, self.uncompressed_size, self.name)


class Books(Base):
    __tablename__ = 'books'

    DEFAULT_PUBDATE = "0101-01-01 00:00:00+00:00"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    sort = Column(String)
    author_sort = Column(String)
    pubdate = Column(String)
    path = Column(String)
    has_cover = Column(Integer)
    uuid = Column(String)

    authors = relationship('Authors', secondary=books_authors_link, backref='books')
    data = relationship('Data', backref='books')
    languages = relationship('Languages', secondary=books_languages_link, backref='books')
    publishers = relationship('Publishers', secondary=books_publishers_link, backref='books')
    identifiers = relationship('Identifiers', backref='books')

    def __init__(self, title, sort, author_sort, timestamp, pubdate, series_index, last_modified, path, has_cover,
                 authors, tags, languages=None):
        self.title = title
        self.sort = sort
        self.author_sort = author_sort
        self.pubdate = pubdate
        self.path = path
        self.has_cover = has_cover

    def __repr__(self):
        return u"<Books('{0},{1}{2}{3}{4}{5}{6}')>".format(self.title, self.sort, self.author_sort,
                                                                  self.pubdate, self.path, self.has_cover)

  

class Custom_Columns(Base):
    __tablename__ = 'custom_columns'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    name = Column(String)
    datatype = Column(String)
    mark_for_delete = Column(Boolean)
    editable = Column(Boolean)
    display = Column(String)
    is_multiple = Column(Boolean)
    normalized = Column(Boolean)

    def get_display_dict(self):
        display_dict = ast.literal_eval(self.display)
        if sys.version_info < (3, 0):
            display_dict['enum_values'] = [x.decode('unicode_escape') for x in display_dict['enum_values']]
        return display_dict


def setup_db():
    global engine
    global session
    global cc_classes

    if config.config_calibre_dir is None or config.config_calibre_dir == u'':
        content = ub.session.query(ub.Settings).first()
        content.config_calibre_dir = None
        content.db_configured = False
        ub.session.commit()
        config.loadSettings()
        return False

    dbpath = os.path.join(config.config_calibre_dir, "metadata.db")
    try:
        if not os.path.exists(dbpath):
            raise
        engine = create_engine('sqlite:///' + dbpath, echo=False, isolation_level="SERIALIZABLE", connect_args={'check_same_thread': False})
        conn = engine.connect()
    except Exception:
        content = ub.session.query(ub.Settings).first()
        content.config_calibre_dir = None
        content.db_configured = False
        ub.session.commit()
        config.loadSettings()
        return False
    content = ub.session.query(ub.Settings).first()
    content.db_configured = True
    ub.session.commit()
    config.loadSettings()
    conn.connection.create_function('title_sort', 1, title_sort)
    conn.connection.create_function('lower', 1, lcase)
    conn.connection.create_function('upper', 1, ucase)

    if not cc_classes:
        cc = conn.execute("SELECT id, datatype FROM custom_columns")

        cc_ids = []
        books_custom_column_links = {}
        cc_classes = {}
        for row in cc:
            if row.datatype not in cc_exceptions:
                books_custom_column_links[row.id] = Table('books_custom_column_' + str(row.id) + '_link', Base.metadata,
                                                          Column('book', Integer, ForeignKey('books.id'),
                                                                 primary_key=True),
                                                          Column('value', Integer,
                                                                 ForeignKey('custom_column_' + str(row.id) + '.id'),
                                                                 primary_key=True)
                                                          )
                cc_ids.append([row.id, row.datatype])
                if row.datatype == 'bool':
                    ccdict = {'__tablename__': 'custom_column_' + str(row.id),
                              'id': Column(Integer, primary_key=True),
                              'book': Column(Integer, ForeignKey('books.id')),
                              'value': Column(Boolean)}
                elif row.datatype == 'int':
                    ccdict = {'__tablename__': 'custom_column_' + str(row.id),
                              'id': Column(Integer, primary_key=True),
                              'book': Column(Integer, ForeignKey('books.id')),
                              'value': Column(Integer)}
                else:
                    ccdict = {'__tablename__': 'custom_column_' + str(row.id),
                              'id': Column(Integer, primary_key=True),
                              'value': Column(String)}
                cc_classes[row.id] = type('Custom_Column_' + str(row.id), (Base,), ccdict)

        for cc_id in cc_ids:
            if (cc_id[1] == 'bool') or (cc_id[1] == 'int'):
                setattr(Books, 'custom_column_' + str(cc_id[0]), relationship(cc_classes[cc_id[0]],
                                                                           primaryjoin=(
                                                                           Books.id == cc_classes[cc_id[0]].book),
                                                                           backref='books'))
            else:
                setattr(Books, 'custom_column_' + str(cc_id[0]), relationship(cc_classes[cc_id[0]],
                                                                           secondary=books_custom_column_links[cc_id[0]],
                                                                           backref='books'))


    Session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    session = Session()
    return True

