import pytest
import System
import json
import RestoreData

username = 'calyam'
password =  '#yeet'
username2 = 'hdjsr7'
username3 = 'yted91'
course = 'cloud_computing'
assignment = 'assignment1'
profUser = 'goggins'
profPass = 'augurrox'

# 1.
def test_login(grading_system):
    grading_system.login(username, password)
    with open('Data/users.json') as f:
        users_json = json.load(f)
    true_role = users_json[username]["role"]
    assert true_role == grading_system.users[username]["role"]

    true_courses = users_json[username]["courses"]
    for c in grading_system.users[username]["courses"]:
        assert c in true_courses
    assert len(true_courses) == len(grading_system.users[username]["courses"])


# 2.
def test_check_password(grading_system):
    test = grading_system.check_password(username,password)
    test2 = grading_system.check_password(username,'#yeet')
    test3 = grading_system.check_password(username,'#Yeet')
    test4 = grading_system.check_password(username,'#YEET')
    test5 = grading_system.check_password(username,'#yeet1')
    if test == test3 or test == test4 or test == test5:
        assert False
    if test == test2:
        assert True

# 3.
def test_change_grade(staff_grading_system):
    student_name = "yted91"
    course = "software_engineering"
    assignment = 'assignment1'
    new_grade = 10
    with open('Data/users.json') as f:
        users_json = json.load(f)
    staff_grading_system.usr.change_grade(student_name, course, assignment, new_grade)
    assert users_json[student_name]["courses"][course][assignment]["grade"] == new_grade

# 4.
def test_create_assignment(staff_grading_system):
    test_name = "assignment_test"
    test_due_date = "test_date"
    staff_grading_system.usr.create_assignment(test_name, test_due_date, course)
    with open('Data/courses.json') as f:
        courses_json = json.load(f)
    test_assignment = courses_json[course]["assignments"][test_name]
    assert test_assignment["due_date"] == test_due_date

# 5. add_student - Professor.py
def test_add_student(prof_grading_system):
    stud_name = "akend3"
    prof_grading_system.usr.add_student(stud_name, course)
    with open('Data/users.json') as f:
        users_json = json.load(f)
    users_json[stud_name]["courses"][course]


# 6. drop_student Professor.py
def test_drop_students(prof_grading_system):
    stud_name = "akend3"
    course_name = "databases"
    prof_grading_system.usr.drop_student(stud_name, course_name)
    with open('Data/users.json') as f:
        users_json = json.load(f)
    current_courses = users_json[stud_name]["courses"]
    assert course_name not in current_courses


# 7.
def test_submit_assignment(stud_grading_system):
    assign = "assignment3"
    test_submission = "test_submission"
    test_sub_date = "test_date"
    stud_grading_system.usr.submit_assignment(course, assign, test_submission, test_sub_date)
    with open('Data/users.json') as f:
        users_json = json.load(f)
    student_name = stud_grading_system.usr.name
    updated_assignment = users_json[student_name]["courses"][course][assign]
    assert updated_assignment["submission"] == test_submission
    assert updated_assignment["submission_date"] == test_sub_date

# 8.
def test_check_ontime(stud_grading_system):
    due_date = "2/2/20"
    early_sub_date = "1/2/20"
    late_sub_date = "1/2/20"
    assert stud_grading_system.usr.check_ontime(due_date, due_date) == True
    assert stud_grading_system.usr.check_ontime(early_sub_date, due_date) == True
    assert stud_grading_system.usr.check_ontime(late_sub_date, due_date) == False



# 9.
def test_check_grades(stud_grading_system):
    course2 = 'software_engineering'
    checked_grades = stud_grading_system.usr.check_grades(course2)
    with open('Data/users.json') as f:
        users_json = json.load(f)
    student_name = stud_grading_system.usr.name
    stored_assignments = users_json[student_name]["courses"][course2]
    for assign, grade in checked_grades:
        assert stored_assignments[assign]["grade"] == grade

# 10.
def test_view_assignments(stud_grading_system):
    loaded_assignments = stud_grading_system.usr.view_assignments(course)
    with open('Data/courses.json') as f:
        courses_json = json.load(f)
    stored_assignments = courses_json[course]["assignments"]
    for assign, due_date in loaded_assignments:
        assert stored_assignments[assign]["due_date"] == due_date

# 11.
def test_login_no_username(grading_system):
    grading_system.login("", "")


# 12.
def test_add_nonexisting_student(prof_grading_system):
    stud_name = "nonexisting"
    prof_grading_system.usr.add_student(stud_name, course)
    with open('Data/users.json') as f:
        users_json = json.load(f)
    users_json[stud_name]["courses"][course]

# 13.
def test_drop_nonexisting_students(prof_grading_system):
    stud_name = "nonexisting!!!!"
    course_name = "databases"
    prof_grading_system.usr.drop_student(stud_name, course_name)
    with open('Data/users.json') as f:
        users_json = json.load(f)
    current_courses = users_json[stud_name]["courses"]

# 14.
def test_view_assignments_nonexisting_course(stud_grading_system):
    course_name = "nonexisting"
    loaded_assignments = stud_grading_system.usr.view_assignments(course_name)
    with open('Data/courses.json') as f:
        courses_json = json.load(f)
    stored_assignments = courses_json[course]["assignments"]
    for assign, due_date in loaded_assignments:
        assert stored_assignments[assign]["due_date"] == due_date

# 15.
def test_check_grades_invalid_course(stud_grading_system):
    course_name = 'Not enrolled course'
    checked_grades = stud_grading_system.usr.check_grades(course_name)
    with open('Data/users.json') as f:
        users_json = json.load(f)
    student_name = stud_grading_system.usr.name
    stored_assignments = users_json[student_name]["courses"][course_name]
    for assign, grade in checked_grades:
        assert stored_assignments[assign]["grade"] == grade

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem


@pytest.fixture
def staff_grading_system():
    gradeSystem = System.System()
    gradeSystem.login('cmhbf5', 'bestTA')
    return gradeSystem

@pytest.fixture
def stud_grading_system():
    gradeSystem = System.System()
    gradeSystem.login('hdjsr7', 'pass1234')
    return gradeSystem

@pytest.fixture
def prof_grading_system():
    gradeSystem = System.System()
    gradeSystem.login(profUser, profPass)
    return gradeSystem