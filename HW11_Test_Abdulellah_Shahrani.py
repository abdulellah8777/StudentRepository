import unittest
import sqlite3
from HW11_Abdulellah_Shahrani import Repository, Student, Instructor, Major


class TestRepository(unittest.TestCase):

    def setUp(self):
        self.dir = '/Users/abod/Desktop/python/DataBase'
        self.result = Repository(self.dir, False)


    def test_majors_data(self):
        """ A function to test the majors data """
        expected = [['SFEN', ['SSW 540', 'SSW 555', 'SSW 810'], ['CS 501', 'CS 546']],
                    ['CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']]]

        result = [major.table_rows() for major in self.result._major.values()]

        self.assertEqual(expected, result)

    def test_students_data(self):
        """ A function to test the students data """
        expected = [['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [None]],
                    ['10115', 'Bezos, J', 'SFEN', ['SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546']],
                    ['10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546']],
                    ['11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], [], [None]],
                    ['11717', 'Kernighan, B', 'CS', [], ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']]]

        result = [student.table_rows() for student in self.result._student.values()]

        self.assertEqual(expected, result)

    def test_instructors_data(self):
        """ A function to test the instructors data """
        expected = [[['98764', 'Cohen, R', 'SFEN', 'CS 546', 1]],
                    [['98763', 'Rowland, J', 'SFEN', 'SSW 810', 4],
                    ['98763', 'Rowland, J', 'SFEN', 'SSW 555', 1]],
                    [['98762', 'Hawking, S', 'CS', 'CS 501', 1],
                    ['98762', 'Hawking, S', 'CS', 'CS 546', 1],
                    ['98762', 'Hawking, S', 'CS', 'CS 570', 1]]]

        result = [list(instructor.table_rows()) for cwid, instructor in self.result._instructor.items()]

        self.assertEqual(expected, result)

    def test_instructor_table_db(self):
        """ A function to test the instructor_table_db """
        db = sqlite3.connect('/Users/abod/Desktop/python/DataBase/810_startup.db')

        query = """ select i.CWID, i.Name, i.Dept, g.Course, count(g.Course) as Students
                            from
                                instructors i
                                join grades g
                                    on i.CWID = g.InstructorCWID
                            group by g.InstructorCWID, g.Course """

        result = set()

        for row in db.execute(query):
            result.add(row)

        expected = {('98762', 'Hawking, S', 'CS', 'CS 501', 1),
                    ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
                    ('98762', 'Hawking, S', 'CS', 'CS 570', 1),
                    ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),
                    ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),
                    ('98764', 'Cohen, R', 'SFEN', 'CS 546', 1)}

        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)

