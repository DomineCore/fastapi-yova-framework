from sqlmodel import create_engine, SQLModel

engine = create_engine("sqlite:///database.sqlite3")
SQLModel.metadata.create_all(engine)
