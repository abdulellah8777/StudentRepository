from os import path
from prettytable import PrettyTable
from collections import defaultdict
from HW08_Abdulellah_Shahrani import file_reading_gen


class Repository:
    ''' a class to store all info about the student and instructor '''
    def __init__(self, the_dir, ptab=True):
        self._the_dir = the_dir
        self._student = dict()
        self._instructor = dict()

        try:
            self._get_student(path.join(the_dir, 'students.txt'))
            self._get_instructor(path.join(the_dir, 'instructors.txt'))
            self._get_grade(path.join(the_dir, 'grades.txt'))

        except ValueError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)

        if ptab:
            print('Student Summary')
            self.student_pre_tab()
        
            print('Instructor Summary')
            self.instructor_pre_tab()

    def student_pre_tab(self):
        ''' to print a pretty table with the students info '''
        pt = PrettyTable(field_names=Student.pt_top)

        for name in self._student.values():
            pt.add_row(name.table_rows())

        print(pt)

    def instructor_pre_tab(self):
        ''' to print a pretty table with the instructors info '''
        pt = PrettyTable(field_names=Instructor.pt_top)

        for name in self._instructor.values():
            for i in name.table_rows():
                '''if the instructor have multaple courses'''
                pt.add_row(i)

        print(pt)
        
    def _get_student(self, the_dir):
        ''' to read the student info and store it in student dict '''
        for cwid, name, major in file_reading_gen(the_dir, 3, sep='\t', header=False):
            self._student[cwid] = Student(cwid, name, major)

    def _get_instructor(self, the_dir):
        ''' to read the instructor info and store it in instructor dict '''
        for cwid, name, dept in file_reading_gen(the_dir, 3, sep='\t', header=False):
            self._instructor[cwid] = Instructor(cwid, name, dept)

    def _get_grade(self, the_dir):
        ''' to assign the grade to each student and instructor '''
        for stud_cwid, course, grade, inst_cwid in file_reading_gen(the_dir, 4, sep='\t', header=False):
            if stud_cwid in self._student:
                self._student[stud_cwid].add_stud(course, grade)
            else:
                raise ValueError(f"can't find the value for the student with the CWID{stud_cwid}")

            if inst_cwid in self._instructor:
                self._instructor[inst_cwid].add_inst(course)
            else:
                raise ValueError(f"can't find the value for the instructor with the CWID{stud_cwid}")


class Student:
    ''' a class to store the Student '''
    pt_top = ['CWID', 'Name', 'Completed Courses']

    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course = dict()

    def add_stud(self, course, grade):
        """ to store the grade of the student which mean that he took the course """
        self.course[course] = grade

    def table_rows(self):
        """ to return a list of Student info to add to the pretty table """
        return [self.cwid, self.name, sorted(self.course)]


class Instructor:
    ''' a class to store the Instructor '''
    pt_top = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.course = defaultdict(int)

    def add_inst(self, course):
        """ to count the students who toke the course """
        self.course[course] += 1

    def table_rows(self):
        """ a generator to return instructor info to add to the pretty table """
        for course, count in self.course.items():
            yield [self.cwid, self.name, self.dept, course, count]


def main():
    the_dir = "/Users/abod/Desktop/python/tables"

    Repository(the_dir)


if __name__ == "__main__":
    main()
