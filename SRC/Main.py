# SRC/Main.py

from ProcessTracker import (
    Session,
    initialize_default_process_types,
    start_operation,
    complete_operation,
    get_all_operations
)
import time


def display_operations(session):
    """Helper function to display all operations in the database."""
    operations = get_all_operations(session)
    print("\nCurrent state of operations:")
    for operation in operations:
        process_name = operation.process_type.Name
        start_time = operation.StartTime.strftime("%Y-%m-%d %H:%M:%S") if operation.StartTime else "Not Started"
        end_time = operation.EndTime.strftime("%Y-%m-%d %H:%M:%S") if operation.EndTime else "Not Completed"
        print(f"OperationID: {operation.OperationID}, ProcessType: {process_name}, Status: {operation.Status}, "
              f"Start Time: {start_time}, End Time: {end_time}")
    print("\n")


def simulate_process(session, process_name, duration_seconds=2):
    """Simulates starting and completing a process with a given duration."""
    print(f"Starting '{process_name}' operation...")
    start_operation(session, process_name)
    display_operations(session)

    # Simulate the duration of the process
    time.sleep(duration_seconds)

    print(f"Completing '{process_name}' operation...")
    complete_operation(session, process_name)
    display_operations(session)


def main():
    # Initialize the database session
    session = Session()

    # Initialize default process types and add corresponding operations
    print("Initializing default process types and operations...")
    initialize_default_process_types(session)
    display_operations(session)

    # List of processes to simulate
    processes = ["Refueling", "Catering", "Unloading", "Loading", "Walk Around"]

    # Simulate each process happening once
    for process_name in processes:
        simulate_process(session, process_name, duration_seconds=1)

    # Final display of the operation states
    print("Final state of all operations after simulation:")
    display_operations(session)

    # Close the session when done
    session.close()


if __name__ == "__main__":
    main()
