# SRC/ProcessTracker.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Define the SQLite database URL
DATABASE_URL = "sqlite:///process_tracker.db"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a base class for declarative class definitions
Base = declarative_base()


# Define the Process model
class Process(Base):
    __tablename__ = 'processes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False, default="not_started")
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_active = Column(Boolean, default=False)

# Create the database tables
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

def add_process(session, name):
    """Adds a new process to the database."""
    new_process = Process(
        name=name,
        status="not_started"
    )
    session.add(new_process)
    session.commit()
    print(f"Process '{name}' added to the tracker.")

def start_process(session, name):
    """Marks a process as started with a timestamp."""
    process = session.query(Process).filter_by(name=name, status="not_started").first()
    if process:
        process.status = "in_progress"
        process.start_time = datetime.datetime.utcnow()
        process.is_active = True
        session.commit()
        print(f"Process '{name}' started at {process.start_time}")
    else:
        print(f"Process '{name}' is already started or does not exist.")

def complete_process(session, name):
    """Marks a process as completed with a timestamp."""
    process = session.query(Process).filter_by(name=name, status="in_progress").first()
    if process:
        process.status = "completed"
        process.end_time = datetime.datetime.utcnow()
        process.is_active = False
        session.commit()
        print(f"Process '{name}' completed at {process.end_time}")
    else:
        print(f"Process '{name}' is not in progress or does not exist.")

def all_processes_finished(session):
    """Checks if all processes are marked as completed in the database."""
    processes = session.query(Process).all()
    return all(process.status == 'completed' for process in processes)

def check_area_clear():
    """Simulates a check for area clearance (to be replaced with YOLOv8 integration)."""
    print("Checking if the area around the airplane is clear...")
    return input("Is the area around the airplane clear (yes/no)? ").lower() == 'yes'

def allow_pushback(session):
    """Determines if pushback is allowed based on process completion and area clearance."""
    if all_processes_finished(session) and check_area_clear():
        print("All processes are complete and the area is clear. Green light for pushback!")
    else:
        print("Pushback not allowed. Some processes are incomplete or the area is not clear.")

def initialize_default_processes(session):
    """Initializes the default processes for an airplane turnaround."""
    add_process(session, "Catering")
    add_process(session, "Refueling")
    add_process(session, "Unloading & Loading")
    add_process(session, "Walk Around")

def get_all_processes(session):
    """Fetches all processes from the database."""
    return session.query(Process).all()
