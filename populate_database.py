from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

engine = create_engine('sqlite:///ItemCatalog1.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Items for Soccer
category1 = Category(name="Soccer")

session.add(category1)
session.commit()

item1 = Item(title="Jersey", description="Text for Jersey.
             Lorem ipsum dolor sit amet, viderer consequat ea has.
             Nec ad imperdiet scriptorem, noster possim delicata vel cu,
             id vis aperiri nominavi voluptatibus. Accusata sensibus
             oportere no qui, an sale essent his.",
             category=category1, username='Swetha')

session.add(item1)
session.commit()

item2 = Item(title="Soccer Cleats", description="Text for
             Lorem ipsum dolor sit amet, viderer consequat ea has.
             Nec ad imperdiet scriptorem, noster possim delicata vel cu,
             id vis aperiri nominavi voluptatibus. Accusata sensibus
             oportere no qui, an sale essent his.",
             category=category1, username='Swetha k')

session.add(item2)
session.commit()

item3 = Item(title="Shinguards", description="Text for ShinGuards.
             Lorem ipsum dolor sit amet, viderer consequat ea has.
             Nec ad imperdiet scriptorem, noster possim delicata vel cu,
             id vis aperiri nominavi voluptatibus. Accusata sensibus
             oportere no qui, an sale essent his.",
             category=category1, username='Swetha k')

session.add(item3)
session.commit()

item4 = Item(title="Two shinguards", description="Text for Two Shinguards.
             Lorem ipsum dolor sit amet, viderer consequat ea has.
             Nec ad imperdiet scriptorem, noster possim delicata vel cu,
             id vis aperiri nominavi voluptatibus. Accusata sensibus
             oportere no qui, an sale essent his.",
             category=category1, username='Swetha k')

session.add(item4)
session.commit()


# Items for SnowBoarding
category2 = Category(name="SnowBoarding")

session.add(category2)
session.commit()

item1 = Item(title="Goggles", description="Text for Goggles.
             Lorem ipsum dolor sit amet, viderer consequat ea has.
             Nec ad imperdiet scriptorem, noster possim delicata vel cu,
             id vis aperiri nominavi voluptatibus. Accusata sensibus
             oportere no qui, an sale essent his.",
             category=category1, username='Swetha k')

session.add(item1)
session.commit()

item2 = Item(title="Snowboard", description="Text for Snowboard.
             Lorem ipsum dolor sit amet, viderer consequat ea has.
             Nec ad imperdiet scriptorem, noster possim delicata vel cu,
             id vis aperiri nominavi voluptatibus. Accusata sensibus
             oportere no qui, an sale essent his.",
             category=category1, username='Swetha k')


session.add(item2)
session.commit()


# Items for Basketball
category3 = Category(name="Basketball")

session.add(category3)
session.commit()

item1 = Item(title="Basketball", description="Text for Basketball.
             Lorem ipsum dolor sit amet, viderer consequat ea has.
             Nec ad imperdiet scriptorem, noster possim delicata vel cu,
             id vis aperiri nominavi voluptatibus. Accusata sensibus
             oportere no qui, an sale essent his.",
             category=category1, username='Swetha k')

session.add(item1)
session.commit()

# Items for Baseball
category4 = Category(name="Baseball")

session.add(category4)
session.commit()

item1 = Item(title="Bat", description="Text for Bat.
             Lorem ipsum dolor sit amet, viderer consequat ea has.
             Nec ad imperdiet scriptorem, noster possim delicata vel cu,
             id vis aperiri nominavi voluptatibus. Accusata sensibus
             oportere no qui, an sale essent his.",
             category=category1, username='Swetha k')

session.add(item1)
session.commit()

# Items for Frisbee
category5 = Category(name="Frisbee")

session.add(category5)
session.commit()

item1 = Item(title="Frisbee", description="Text for Frisbee.
             Lorem ipsum dolor sit amet, viderer consequat ea has.
             Nec ad imperdiet scriptorem, noster possim delicata vel cu,
             id vis aperiri nominavi voluptatibus. Accusata sensibus
             oportere no qui, an sale essent his.",
             category=category1, username='Swetha k')


session.add(item1)
session.commit()

# Items for Hockey
category6 = Category(name="Hockey")

session.add(category6)
session.commit()

item1 = Item(title="Stick", description="Text for Stick.
             Lorem ipsum dolor sit amet, viderer consequat ea has.
             Nec ad imperdiet scriptorem, noster possim delicata vel cu,
             id vis aperiri nominavi voluptatibus. Accusata sensibus
             oportere no qui, an sale essent his.",
             category=category1, username='Swetha k')


session.add(item1)
session.commit()

print "added Categories and items!"
