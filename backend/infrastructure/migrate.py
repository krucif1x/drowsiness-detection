#Alembic is a database migration tool for SQLAlchemy, which helps you manage changes to your database tables and columns over time

from alembic import command #command object contains functions that let you run Alembic commands from within your Python code
from alembic.config import Config#Config class is used to load and read Alembic's config settings from a file


def run_migrations():
    """
    Runs Alembic migrations to update the database schema.
    """
    alembic_cfg = Config("alembic.ini") #creates a config object by reading the alembic.ini file
    #"alembic.ini" contains essential info like database connection URL and location of your migration scripts

    # Explicitly set script_location relative to this ini file
    alembic_cfg.set_main_option("script_location", "alembic") #Method Call
    #THis line tells the config where to find the migration scripts
    #It sets the script_location to a directory named "alembic"
    #This directory contains the "versions" foler where all the individual migration files are stored

    command.upgrade(alembic_cfg, "head") #function call
    #Calls the "upgrade" function from the command object
    #"alembic_cfg" passess the config so that command knows which database to connect to
    #"head" is a special keyword that tells Alembic to apply all migrations necessary 
    #to bring the database schema up to the most recent version available
