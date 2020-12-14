from pathlib import Path
import sys
from xml.dom import minidom
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
import click

# Initialize app
app = Flask(__name__)

basedir = Path().parent.absolute()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    str(Path.joinpath(basedir, "db.sqlite"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    student_number = db.Column(
        db.Integer, autoincrement=True, unique=True, nullable=False)

    def __repr__(self):
        return f'<Student: {self.first_name} {self.last_name} ({self.email}) Student No: {self.student_number}>'


@app.cli.command("migrate")
def migrate():
    """Creates the database with its schema"""
    print("Creating database and tables")
    db.create_all()
    print("Done")


@app.cli.command("seed-students")
@click.argument("count", type=click.INT)
def seed(count):
    if count < 0 or count == 0:
        click.exceptions.BadArgumentUsage("Enter positive count").show()
        sys.exit(click.ClickException.exit_code)

    """Seeds the students table with student records"""
    faker = Faker()
    print(f"Seeding {count} records...")
    for i in range(count):
        db.session.add(
            Student(
                first_name=faker.unique.first_name(),
                last_name=faker.unique.last_name(),
                email=faker.unique.email(),
                student_number=faker.unique.random_int(1, 100)
            )
        )

    db.session.commit()
    print("Done seeding :)")


@app.cli.command("refresh")
def refresh():
    """Drops all tables and recreates the schema"""
    print("Dropping all tables")
    db.drop_all()
    print("Creating tables")
    db.create_all()

@app.cli.command("export-students")
def create_students_xml():
    """Exports the records in the students table to studente.xml file"""
    document = minidom.Document()

    # Creates students root element
    students = document.createElement("students")

    printable_properties = ['id', 'student_number',
                            'first_name', 'last_name', 'email']
    for student_record in Student.query.all():
        student = document.createElement("student")
        for property in printable_properties:
            property_element = document.createElement(property)
            property_element.appendChild(
                document.createTextNode(str(getattr(student_record, property)))
            )
            student.appendChild(property_element)
        students.appendChild(student)

    document.appendChild(students)

    document_path = Path.joinpath(basedir, "students.xml")
    with open(document_path, "w") as file:
        file.write(document.toprettyxml(indent="\t"))
    print("Exported data to students.xml")

@app.cli.command("deserialize")
def deserialize_xml_file():
    document = minidom.parse("students.xml")
    for student_element in document.getElementsByTagName("student"):
        element_nodes = [node for node in student_element.childNodes if node.nodeType == minidom.Node.ELEMENT_NODE]
        student_properties_dict = dict([(node.tagName, node.firstChild.nodeValue) for node in element_nodes])
        student = Student(**student_properties_dict)
        print(student)
