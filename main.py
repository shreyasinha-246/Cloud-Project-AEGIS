from database import create_tables
from dashboard import start_dashboard

def main():

    create_tables()

    start_dashboard()


if __name__ == "__main__":
    main()