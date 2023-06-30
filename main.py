import logging
import sys

from src.transportation import Tranportation

"""
   Setup logger
"""
logging.basicConfig(format="%(asctime)s -> %(message)s", level=logging.INFO)

"""
   Database:
   As I don't have any database in the project
   I use a list to store all transportation results
"""
DB = []


def run_workflow(withError: bool = False):
    logger.info("Running workflow ✨")
    t = Tranportation()
    t.run_pipeline(withError)
    return t


def show_menu():
    print("Please insert one of the following numbers:")
    print("1: 🚀 Run pipeline successfully")
    print("2: 🤕 Run pipeline with error")
    print("3: 🤓 Show all runs")
    print("4: 🔚 Exit \n")


if __name__ == "__main__":
    print("Welcome to Carlos Guerrero's Test")

    logger = logging.getLogger(__name__)

    while True:
        show_menu()
        l = sys.stdin.readline()

        try:
            option = int(l)
        except ValueError:
            print("💀 Error: Value must be a number: 1, 2, 3 \n")
            continue

        if option == 1:
            transportation = run_workflow(False)
            DB.append(transportation)
            continue

        if option == 2:
            transportation = run_workflow(True)
            DB.append(transportation)
            continue

        if option == 3:
            for i, t in enumerate(DB):
                print("📇 Index:", i + 1, t)
            continue

        if option == 4:
            print("Bye 👋!")
            break
