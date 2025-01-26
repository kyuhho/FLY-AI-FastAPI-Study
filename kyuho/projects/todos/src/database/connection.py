from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Python Console
# from sqlalchemy import select
# session.scalar(select(1))

DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"

engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionFactory()

def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()

