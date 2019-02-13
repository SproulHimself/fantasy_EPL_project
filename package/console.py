# from package.data_builder import *
# from os import remove
# import errno
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
#
#
# engine = create_engine('sqlite:///EPL_fantasy.db')
#
#
# def db_creator(filename):
#     try:
#         remove(filename)
#     except OSError as e:
#         if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
#             raise
#         else:
#             Base.metadata.create_all(engine)
#
#
# db_creator('/Users/sproul/Downloads/Project12-master/EPL_fantasy.db')
#
# Session = sessionmaker(bind=engine)
# session = Session()
#
# session.add_all(team_results)
# session.commit()
