import sqlalchemy as db
from sqlalchemy.orm import relationship

from main import Base

'''
    According to the logic of the script, the base structure should be many-to-many on itself. 
    But I didn't figure out how to do it. 
    Therefore, the structure of the database with two tables
'''


class PageToLink(Base):
    __tablename__ = 'page_to_link'
    link = db.Column(db.Integer, db.ForeignKey('link.id'), primary_key=True)
    page = db.Column(db.Integer, db.ForeignKey('page.id'), primary_key=True)


class PageModel(Base):
    __tablename__ = "page"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)
    links_on_page = relationship('LinkModel', secondary="page_to_link", backref="links", lazy=True)

    def __repr__(self):
        return self.title


class LinkModel(Base):
    __tablename__ = "link"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)

    def __repr__(self):
        return self.title
