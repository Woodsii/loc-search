import os
from sqlalchemy import ARRAY, Column, Integer, Text, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    identifiers = relationship(
        "SystemControlNumber",
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    author = Column(Text)
    title = Column(Text)
    title_remainder = Column(Text)
    publications = relationship(
        "Publication",
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    series = relationship(
        "Series",
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    notes = relationship(
        "Note",
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    subjects = relationship(
        "Subject",
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

class SystemControlNumber(Base):
    __tablename__ = 'identifiers'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), index=True)
    number = Column(Text, nullable=False, index=True)
    book = relationship("Book", back_populates="identifiers")

class Publication(Base):
    __tablename__ = 'publications'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), index=True)
    place = Column(Text)
    name = Column(Text)
    date = Column(Text)
    book = relationship("Book", back_populates="publications")

class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), index=True)
    name = Column(Text)
    volume = Column(Text)
    book = relationship("Book", back_populates="series")

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), index=True)
    text = Column(Text)
    book = relationship("Book", back_populates="notes")

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), index=True)
    heading = Column(Text)
    subheading = Column(Text)
    form = Column(ARRAY(Text))
    general = Column(ARRAY(Text))
    chron = Column(ARRAY(Text))
    geo =  Column(ARRAY(Text))
    book = relationship("Book", back_populates="subjects")

def init_db(url: str | None = None, echo: bool = False):
    url = url or os.environ.get("LOCDB_URL", "postgresql:///locdb")
    engine = create_engine(url, echo=echo)
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    init_db(echo=True)
    print("Empty Database Tables Initialized...")