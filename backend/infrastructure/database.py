from sqlmodel import Session, create_engine
#Session a temporary, high-level workspace that you use to talk to your database file (SQLite)
#create_engine is a function used to setup the main connection point to the database

DATABASE_URL = "sqlite:///./database.db"
#sqlite:/// specifies that we are using a SQLite database
#./database.db is the pathway to the database file
#./ means in the current directory
#database.db will be the name of the file where all the data is stored
engine = create_engine(DATABASE_URL, echo=False)

def get_session(): 
    with Session(engine) as session: 
        #with statement known as a context manager
        #Session(engine) creates a new, temporary session object connected to database engine
        yield session
        #yield is a generator function

#Function: This is the core of the generator pattern.

#1.When get_session() is called, it runs up to this line.

#2.It "yields" (provides) the session object to whatever code called it.

#3.The function then pauses.

#4.The other code uses the provided session to perform database operations (e.g., create, read, update, delete).

#5.Once the other code is done, the get_session function resumes, the with block ends, and the session is automatically and safely closed.



#Why yield is used instead of return. to manage the session's lifecycle. It allows the function to hand over a live, 
#open database session and then automatically close it after it has been used.
#Using return would instantly close the session, making it useless
