import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/instructors')
def instructors_data():
    db_path = '/Users/abod/Desktop/HW12/810_startup.db'

    try:
        db = sqlite3.connect(db_path)
    except sqlite3.OperationalError:
        return f"Error: Unable to open the Database at {db_path}"
    else:
        query = """ select i.CWID, i.Name, i.Dept, g.Course, count(g.Course) as Students
                    from
                        instructors i
                        join grades g
                            on i.CWID = g.InstructorCWID
                    group by g.InstructorCWID, g.Course  """

        data = [{'cwid': cwid, 'name': name, 'dept': dept, 'course': course, 'students': students}
                for cwid, name, dept, course, students in db.execute(query)]

        db.close()

        return render_template(
                'instructors.html',
                title='Stevens instructors',
                header='Stevens Repository',
                table_name='Courses and student counts',
                instructors=data)

app.run(debug=True)