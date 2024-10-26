# SRC/Main.py

from ProcessTracker import (
    Session,
    initialize_default_processes,
    start_process,
    complete_process,
    allow_pushback,
    get_all_processes
)


def display_processes(session):
    """Helper function to display all processes in the database."""
    processes = get_all_processes(session)
    print("\nCurrent state of processes:")
    for process in processes:
        print(f"ID: {process.id}, Name: {process.name}, Status: {process.status}, "
              f"Start Time: {process.start_time}, End Time: {process.end_time}")
    print("\n")


def main():
    # Initialize the database session
    session = Session()

    print("Initializing default processes...")
    initialize_default_processes(session)
    display_processes(session)

    # Simulate starting and completing each process
    print("Starting 'Refueling' process...")
    start_process(session, "Refueling")
    display_processes(session)

    print("Completing 'Refueling' process...")
    complete_process(session, "Refueling")
    display_processes(session)

    print("Starting 'Catering' process...")
    start_process(session, "Catering")
    display_processes(session)

    print("Completing 'Catering' process...")
    complete_process(session, "Catering")
    display_processes(session)

    print("Starting 'Unloading & Loading' process...")
    start_process(session, "Unloading & Loading")
    display_processes(session)

    print("Completing 'Unloading & Loading' process...")
    complete_process(session, "Unloading & Loading")
    display_processes(session)

    print("Starting 'Walk Around' process...")
    start_process(session, "Walk Around")
    display_processes(session)

    print("Completing 'Walk Around' process...")
    complete_process(session, "Walk Around")
    display_processes(session)

    # Check if pushback is allowed
    print("Checking if pushback is allowed...")
    allow_pushback(session)

    # Final display of the process states
    display_processes(session)

    # Close the session when done
    session.close()


if __name__ == "__main__":
    main()
