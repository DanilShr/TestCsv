import csv
import argparse
from statistics import mean

from tabulate import tabulate
from collections import defaultdict


def create_report(files, report, find):
    find = f"{find}_name"
    students = defaultdict(list)
    try:
        for file in files:
            with open(file, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile, delimiter=",")
                for row in reader:
                    students[row[find]].append(int(row["grade"]))

        for key, value in students.items():
            students[key] = round(mean(value), 2)

        sorted_students = sorted(students.items(), key=lambda x: x[1], reverse=True)
        head = find.title().replace("_", " ")
        with open(report, "w", newline="", encoding="utf-8") as report:
            writer = csv.writer(report)
            writer.writerow([f"{head}", "Grade"])
            for st, gr in sorted_students:
                writer.writerow([st, gr])

        headers = [f"{head}", "Grade"]

        print(
            tabulate(
                sorted_students,
                headers=headers,
                tablefmt="fancy_grid",
                showindex=True,
                numalign="left",
            )
        )
    except FileNotFoundError:
        print("File not found")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="This program reads a csv file and writes it into a csv file."
    )

    parser.add_argument("--files", "-f", type=str, nargs="+", required=True)

    parser.add_argument("--report", "-r", type=str, default=["report.csv"])

    parser.add_argument(
        "--value",
        "-v",
        type=str,
        choices=["student", "teacher", "subject"],
        default="student",
        required=False,
    )

    args = parser.parse_args()
    results = create_report(args.files, args.report, args.value)
