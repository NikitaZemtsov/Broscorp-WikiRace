import sqlalchemy as db
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from main import Base



class PageToPage(Base):
    __tablename__ = 'page_to_page'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Integer, db.ForeignKey('page.id'))
    page = db.Column(db.Integer, db.ForeignKey('page.id'))
    UniqueConstraint('page', 'link', name='unique_relationship')


class PageModel(Base):
    __tablename__ = "page"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)
    links_on_page = relationship('PageModel', secondary="page_to_page",
                                 primaryjoin=id == PageToPage.page,
                                 secondaryjoin=id == PageToPage.link)

    def __repr__(self):
        return self.title

