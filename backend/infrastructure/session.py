#This code sets ups a connection to the SQLite database using SQLModel
#It provides a function to create all the necessary tables and another function to safely manage database session for reading and writing data


from sqlmodel import Session, SQLModel, create_engine
#"Session" is a class used to create database sessios (the "workspace for database tasks)
#"SQLModel" is the base class that all your database table models will inherit from
#"create_engine" is the function that establishes the low-level connection to the database

from backend.settings.app_config import settings #Import settings object from a local project file

sqlite_file_name = settings.ConnectionStrings.db_connections #Gets the databsae filename from "settings" object
sqlite_url = f"sqlite:///{sqlite_file_name}"#uses an f-string to construct the full database connection URL
#This URL tell SQLAlchemy what kind of database it is (sqlite) and where to find it


engine = create_engine(sqlite_url) #Creates the databasse engine (core object that manages the connection to the database.db file)

def init_db():
    SQLModel.metadata.create_all(engine) #Magic command to create your tables
    #"SQLModel.metadata" acts as a registry that keeps track fo all the table models you've defined in your code
    #".create_all(engine)" connects to the database using engine and isssue necessary SQL commands to create all registered
    #tables, but only if they don't already exist

def get_session(): #generator function that provides databse session in modern web applications
    with Session(engine) as session: #It creates a new Session linked to our database engine. The with statement guarantees that the session will be properly closed after use, even if errors occur.
        yield session #It provides the active session object to the code that called get_session, pauses its own execution, and then resumes after the session has been used in order to close it
