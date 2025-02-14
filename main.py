from src import optim
import sys

years = [2025, 2026, 2027]
scenario = sys.argv[1]

test = optim.optim(years, "data/"+scenario)

if test.solve():
    test.printCourseAssign("courses.csv")
    test.printFacultyAssign("faculty.csv")
