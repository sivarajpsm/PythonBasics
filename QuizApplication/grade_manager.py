
# Week 1 - Day 2 : Student Grade Manager
#
# Program flow (top to bottom):
#   Step 1 - DECLARE constants      (values that never change)
#   Step 2 - DECLARE data store     (where students are kept)
#   Step 3 - DEFINE functions       (recipes - nothing runs yet)
#   Step 4 - INVOKE main()          (the program actually starts here)
 
 
# =================================================================
# STEP 1: DECLARE CONSTANTS
# =================================================================
# Constants are written in UPPER_CASE so it is clear they should not change.
 
# DECLARE: lowest and highest valid mark (data type: int)
MIN_MARK = 0
MAX_MARK = 100
 
# DECLARE: grading scale as a tuple, because the rules should never change.
# Each item is a pair: (minimum mark, grade letter).
# The order matters: the highest grade is checked first.
GRADE_SCALE = ((90, "A"), (80, "B"), (70, "C"), (60, "D"), (0, "E"))
 
 
# =================================================================
# STEP 2: DECLARE DATA STORE
# =================================================================
# I use a dictionary with a unique student ID as the key.
# If the name were the key, a second "Siva" would overwrite the first.
# With IDs, both are kept:
#   {1: {"name": "Siva", "mark": 92}, 2: {"name": "Siva", "mark": 65}}
 
# DECLARE: empty dictionary - students are added while the program runs
students = {}
 
 
# =================================================================
# STEP 3: DEFINE FUNCTIONS
# =================================================================
# "def" only DEFINES a function (teaches Python the recipe).
# The code inside runs only when the function is INVOKED (called).
# Small helper functions come first, bigger ones that use them come later.
 
 
# DEFINE: is_valid_mark(mark) -> True / False
def is_valid_mark(mark):
    # Chained comparison: is the mark between 0 and 100?
    # The comparison itself gives True or False, so return it directly.
    return MIN_MARK <= mark <= MAX_MARK
 
 
# DEFINE: get_grade(mark) -> "A" to "E"
def get_grade(mark):
    # Loop through the scale from top to bottom.
    # Each pair is unpacked into two variables: min_mark and grade.
    for min_mark, grade in GRADE_SCALE:
        # Using >= makes the boundaries inclusive (90 is an A, 80 is a B).
        if mark >= min_mark:
            return grade    # first match wins, function exits here
 
 
# DEFINE: read_name() -> a valid name in Title Case
def read_name():
    # while True = keep asking until a valid name is returned
    while True:
        # INVOKE built-in input(), then .strip() removes extra spaces
        name = input("Enter student name: ").strip()
 
        if name == "":
            print("  Name cannot be empty. Try again.")
        else:
            # Nested if: these checks run only when the name is not empty.
            # Remove spaces before checking, so "Arun Kumar" is allowed
            # but "R2D2" or "123" is not.
            if not name.replace(" ", "").isalpha():
                print("  Name should contain letters only. Try again.")
            elif len(name) > 30:
                print("  Name is too long (max 30 characters). Try again.")
            else:
                return name.title()    # "siva" -> "Siva", exits the loop
 
 
# DEFINE: read_mark() -> a valid whole number from 0 to 100
def read_mark():
    while True:
        # input() always gives a string, e.g. "92" not 92
        raw = input("Enter mark (0-100): ").strip()
 
        # Check 1: empty input
        if raw == "":
            print("  Mark cannot be empty. Try again.")
            continue    # go back to the top of the loop and ask again
 
        # Check 2: not a whole number
        # int() crashes on text like "abc" or "92.5", so catch that here.
        try:
            mark = int(raw)    # convert string -> int
        except ValueError:
            print(f"  '{raw}' is not a whole number. Try again.")
            continue
 
        # Check 3: out of range, like 105 or -5
        # INVOKE is_valid_mark() defined above
        if not is_valid_mark(mark):
            print(f"  {mark} is out of range. Enter a mark from 0 to 100.")
            continue
 
        return mark    # all checks passed, exit with the valid mark
 
 
# DEFINE: add_student() -> asks, validates and stores one student
def add_student():
    print("\n--- Add Student ---")
 
    # INVOKE the input helpers defined above
    name = read_name()
    mark = read_mark()
 
    # Let the user know if this name already exists (it is still added).
    # Set comprehension: collect all existing names in lowercase.
    existing_names = {info["name"].lower() for info in students.values()}
    if name.lower() in existing_names:    # membership operator "in"
        print(f"  Note: '{name}' already exists. Adding as a new student.")
 
    # Students are never removed, so the next ID is simply count + 1.
    student_id = len(students) + 1
 
    # Store: key = student_id, value = a small dictionary of details
    students[student_id] = {"name": name, "mark": mark}
 
    # INVOKE get_grade() to show the grade straight away
    print(f"  Added {name} (ID {student_id}) - mark {mark}, grade {get_grade(mark)}")
 
 
# DEFINE: calculate_stats() -> (average, highest, lowest) as a tuple
def calculate_stats():
    # List comprehension: pull every mark into a plain list
    marks = [info["mark"] for info in students.values()]
 
    # Arithmetic: "/" always gives a float, e.g. 76.333...
    average = sum(marks) / len(marks)
 
    # Returning three values - Python packs them into one tuple
    return average, max(marks), min(marks)
 
 
# DEFINE: show_results() -> prints the table and the stats
def show_results():
    # Guard clause: without this check, the average would divide by zero.
    # An empty dictionary counts as False.
    if not students:
        print("\n  No students yet. Please add a student first.")
        return    # exit the function early
 
    # Header row. :<15 = left-align in 15 spaces, :>5 = right-align in 5
    print("\n--- Results ---")
    print(f"{'ID':<4}{'Name':<15}{'Mark':>5}{'Grade':>7}")
    print("-" * 31)    # string repetition: 31 dashes
 
    # .items() gives (key, value) pairs -> unpack into two variables
    for student_id, info in students.items():
        name = info["name"]
        mark = info["mark"]
        print(f"{student_id:<4}{name:<15}{mark:>5}{get_grade(mark):>7}")
 
    print("-" * 31)
 
    # INVOKE calculate_stats() and unpack the tuple into three variables
    average, highest, lowest = calculate_stats()
    print(f"Average: {average:.1f}    Highest: {highest}    Lowest: {lowest}")
 
 
# DEFINE: show_menu() -> prints the menu options
def show_menu():
    print("\n===== Student Grade Manager =====")
    print("1. Add student")
    print("2. Show results")
    print("3. Quit")
 
 
# DEFINE: main() -> the controller that runs the menu loop
def main():
    # Keep showing the menu until the user chooses to quit
    while True:
        # INVOKE show_menu() each time round the loop
        show_menu()
 
        # Keep the choice as a string, so "abc" can never crash int()
        choice = input("Choose an option (1-3): ").strip()
 
        # Control flow: only one branch runs
        if choice == "1":
            add_student()      # INVOKE
        elif choice == "2":
            show_results()     # INVOKE
        elif choice == "3":
            print("Goodbye!")
            break              # leave the loop -> main() ends -> program ends
        else:
            # Anything else (hello, 9, empty) -> message, then menu again
            print(f"  '{choice}' is not a valid option. Enter 1, 2 or 3.")
 
 
# =================================================================
# STEP 4: INVOKE - START THE PROGRAM
# =================================================================
# Everything above was only declared or defined. This is the line
# that actually starts the program.
# __name__ is "__main__" only when this file is run directly
# (python grade_manager.py), not when another file imports it.
if __name__ == "__main__":
    main()    # INVOKE main()
 