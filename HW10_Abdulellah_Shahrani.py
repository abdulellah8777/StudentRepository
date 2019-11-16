from os import path
from prettytable import PrettyTable
from collections import defaultdict
from HW08_Abdulellah_Shahrani import file_reading_gen


class Repository:
    ''' a class to store all info about the student and instructor '''
    def __init__(self, the_dir, ptab=True):
        self._the_dir = the_dir
        self._major = dict()
        self._student = dict()
        self._instructor = dict()

        try:
            self._get_major(path.join(the_dir, 'majors.txt'))
            self._get_student(path.join(the_dir, 'students.txt'))
            self._get_instructor(path.join(the_dir, 'instructors.txt'))
            self._get_grade(path.join(the_dir, 'grades.txt'))

        except ValueError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)

        if ptab:
            print('Majors Summary')
            self.major_pre_tab()

            print('Student Summary')
            self.student_pre_tab()
        
            print('Instructor Summary')
            self.instructor_pre_tab()

    def _get_major(self, the_dir):
        ''' to read the major info and store it in major dict '''
        for major, flag, course in file_reading_gen(the_dir, 3, sep='\t', header=True):
            if major not in self._major:
                self._major[major] = Major(major)
            self._major[major].add_major(flag, course)
  
    def _get_student(self, the_dir):
        ''' to read the student info and store it in student dict '''
        for cwid, name, major in file_reading_gen(the_dir, 3, sep=';', header=True):
            if major not in self._major:
                print(f'a student with the CWID {cwid} has unknown major')
            else:
                self._student[cwid] = Student(cwid, name, self._major[major])

    def _get_instructor(self, the_dir):
        ''' to read the instructor info and store it in instructor dict '''
        for cwid, name, dept in file_reading_gen(the_dir, 3, sep='|', header=True):
            self._instructor[cwid] = Instructor(cwid, name, dept)

    def _get_grade(self, the_dir):
        ''' to assign the grade to each student and instructor '''
        for stud_cwid, course, grade, inst_cwid in file_reading_gen(the_dir, 4, sep='|', header=True):
            if stud_cwid in self._student:
                self._student[stud_cwid].add_stud(course, grade)
            else:
                raise ValueError(f"can't find the value for the student with the CWID{stud_cwid}")

            if inst_cwid in self._instructor:
                self._instructor[inst_cwid].add_inst(course)
            else:
                raise ValueError(f"can't find the value for the instructor with the CWID{stud_cwid}")

    def major_pre_tab(self):
        ''' to print a pretty table with the students info '''
        pt = PrettyTable(field_names=Major.pt_top)

        for name in self._major.values():
            pt.add_row(name.table_rows())

        print(pt)

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


class Student:
    ''' a class to store the Student '''
    pt_top = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives']

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
        major, completed, remain_req, remain_elec = self.major.remain_courses(self.course)
        return [self.cwid, self.name, major, sorted(completed), sorted(remain_req), sorted(remain_elec)]


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


class Major:
    pt_top = ['Dept', 'Required', 'Electives']
    pass_grade = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']

    def __init__(self, major):
        self.major = major
        self.required = set()
        self.elective = set()

    def add_major(self, flag, course):
        ''' sort the majors courses between required and elective courses '''
        if flag == 'R':
            self.required.add(course)
        elif flag == 'E':
            self.elective.add(course)
        else:
            raise ValueError(f'wrong flag for the {self.major} major')
    
    def remain_courses(self, the_course):
        ''' to test if the student passed the course or not and return:
            the major, completed courses, remaining required and elective courses 
        '''
        complete = set()
        for course, grade in the_course.items():
            if grade in Major.pass_grade:
                complete.add(course)

        remain_req = self.required - complete
        remain_elec = self.elective - complete

        if len(remain_elec) < len(self.elective):
            remain_elec = {None}

        return self.major, complete, remain_req, remain_elec

    def table_rows(self):
        ''' to return a list of majors info to add to the pretty table '''
        return [self.major, sorted(self.required), sorted(self.elective)]


def main():
    the_dir = "/Users/abod/Desktop/python/tables_1"

    Repository(the_dir)


if __name__ == "__main__":
    main()
