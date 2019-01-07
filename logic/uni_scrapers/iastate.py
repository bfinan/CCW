import re
import Take
path = "/home/you/CCW/anonymized_transcript.txt"

with open(path, "r") as reader:
    untenable = reader.read()

course_number = re.compile(r'\dT?\d\d')
semester_string = re.compile(r'((FALL|SPRING|SUMMER) \d\d\d\d)|TRANSFER')


def is_a_take(transcript_line):
    if course_number.search(transcript_line):
        if ".0" in line:
            if 38 <= len(line) <= 55:
                return True
    else:
        return False


def semester_to_semestercode(sem_string):
    sem_string = sem_string.lstrip()
    replacements = [(" SEMESTER", ""), (" CREDITS ACCEPTED FROM", ""),
                    ("FALL ", "F"), ("SPRING ", "S"),
                    ("SUMMER ", "M"), ("WINTER", "W")]
    for replacement in replacements:
        sem_string = sem_string.replace(replacement[0], replacement[1])
    return sem_string

def semline_to_take(ss, is_transfer):
    out_take = Take()
    ss = ss.lstrip()
    first_digit = re.search("\d", ss)
    department = ss[0:first_digit.start()]
    department = department.rstrip()
    out_take.dept = department
    number = ss[first_digit.start():first_digit.start()+5]
    number = number.rstrip()
    out_take.number = number
    if not is_transfer:
        name = ss[11:33]
        name = name.lstrip().rstrip()
    else:
        name = department + " " + number
    out_take.name = name
    remainder = ss

    return out_take


current_semester = "SEMESTER NOT FOUND"

transcript_lines = untenable.splitlines()
for line_idx, line in enumerate(transcript_lines):
    if semester_string.search(line):
        current_semester = semester_to_semestercode(line)
    if is_a_take(line):
        line_take = semline_to_take(line, False)
        print("%s %s %s %s" % (current_semester, line_take.dept, line_take.number, line_take.name))