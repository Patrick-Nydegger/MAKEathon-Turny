# SRC/ProcessTracker.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import os

# Define the SQLite database URL
DATABASE_URL = "sqlite:///process_tracker.db"

# Remove existing database file if needed (optional)
if os.path.exists("process_tracker.db"):
    os.remove("process_tracker.db")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=False)

# Create a base class for declarative class definitions
Base = declarative_base()


# Define the ProcessType model (corresponds to ProcessType table)
class ProcessType(Base):
    __tablename__ = 'process_type'

    ProcessTypeID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Description = Column(String)

    # Relationship with Operation
    operations = relationship("Operation", back_populates="process_type")


# Define the Operation model (corresponds to Operation table)
class Operation(Base):
    __tablename__ = 'operation'

    OperationID = Column(Integer, primary_key=True, autoincrement=True)
    ProcessTypeID = Column(Integer, ForeignKey('process_type.ProcessTypeID'), nullable=False)
    FlightID = Column(Integer)  # Assuming FlightID is not used in this context
    StartTime = Column(DateTime, nullable=True)  # Allow NULL initially
    EndTime = Column(DateTime, nullable=True)    # Allow NULL initially
    Status = Column(String(20), default='Scheduled')
    Notes = Column(String)

    # Relationship with ProcessType
    process_type = relationship("ProcessType", back_populates="operations")


# Create the database tables
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)


def add_process_type(session, name, description):
    """Adds a new process type to the database."""
    process_type = ProcessType(Name=name, Description=description)
    session.add(process_type)
    session.commit()
    print(f"ProcessType '{name}' added to the tracker.")


def add_operation(session, process_type_name):
    """Adds a new operation for a given process type."""
    process_type = session.query(ProcessType).filter_by(Name=process_type_name).first()
    if not process_type:
        print(f"ProcessType '{process_type_name}' does not exist.")
        return

    operation = Operation(
        ProcessTypeID=process_type.ProcessTypeID,
        StartTime=None,  # StartTime will be set when the operation starts
        EndTime=None,    # EndTime will be set when the operation completes
        Status='not_started'
    )
    session.add(operation)
    session.commit()
    print(f"Operation for '{process_type_name}' added to the tracker.")


def start_operation(session, process_type_name):
    """Marks an operation as started with a timestamp."""
    process_type = session.query(ProcessType).filter_by(Name=process_type_name).first()
    if not process_type:
        print(f"ProcessType '{process_type_name}' does not exist.")
        return

    operation = session.query(Operation).filter_by(ProcessTypeID=process_type.ProcessTypeID, Status='not_started').first()
    if operation:
        operation.Status = 'in_progress'
        operation.StartTime = datetime.datetime.utcnow()
        session.commit()
        print(f"Operation '{process_type_name}' started at {operation.StartTime}")
    else:
        print(f"No 'not_started' operation found for '{process_type_name}'.")


def complete_operation(session, process_type_name):
    """Marks an operation as completed with a timestamp."""
    process_type = session.query(ProcessType).filter_by(Name=process_type_name).first()
    if not process_type:
        print(f"ProcessType '{process_type_name}' does not exist.")
        return

    operation = session.query(Operation).filter_by(ProcessTypeID=process_type.ProcessTypeID, Status='in_progress').first()
    if operation:
        operation.Status = 'completed'
        operation.EndTime = datetime.datetime.utcnow()
        session.commit()
        print(f"Operation '{process_type_name}' completed at {operation.EndTime}")
    else:
        print(f"No 'in_progress' operation found for '{process_type_name}'.")


def all_operations_finished(session):
    """Checks if all operations are marked as completed in the database."""
    operations = session.query(Operation).all()
    return all(operation.Status == 'completed' for operation in operations)


def get_all_operations(session):
    """Fetches all operations from the database."""
    return session.query(Operation).all()


def initialize_default_process_types(session):
    """Initializes the default process types and their operations."""
    default_processes = [
        ("Catering", "Providing food and beverages for the flight"),
        ("Refueling", "Refueling the airplane"),
        ("Unloading", "Unloading cargo and luggage"),
        ("Loading", "Loading cargo and luggage"),
        ("Walk Around", "Safety inspection of the airplane")
    ]
    for name, description in default_processes:
        add_process_type(session, name, description)
        add_operation(session, name)
