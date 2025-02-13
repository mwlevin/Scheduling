from src import optim


years = [2025, 2026, 2027]
willing_file = "data/willing to teach.csv"
frequencies_file = "data/frequencies.csv"
initials_file = "data/initials.csv"
special_file = "data/special.csv"
required_file = "data/required.csv"

test = optim.optim(years, willing_file, initials_file, frequencies_file, special_file, required_file)

if test.solve():
    test.printCourseAssign("courses.csv")
    test.printFacultyAssign("faculty.csv")
