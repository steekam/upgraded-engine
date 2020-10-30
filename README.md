XML Assignment

A simple Flask "CLI" application that serializes data from the database

## Project Setup
Install depencies based on `requirements.txt`
```bash
pip install
```

The application comes with several flask CLI helper commands to help setup the project for the demo.

- `flask migrate` : Creates a `db.sqlite` database file and creates a `student` table.
- `flask seed-students <COUNT>` : Seeds student records.
- `flask refresh` : Drops all tables and creates the schema again.
- `flask export-students` : Exports student records to `student.xml` file

## Demo
- Install dependencies
- Copy `.env.example` to `.env`
- Migrate schema
```
flask migrate
```
- Seed 10 student records
```
flask seed-students 10
```
- Export xml data
```
flask export-students
```

## Sample XML output
```xml
<?xml version="1.0" ?>
<students>
	<student>
		<id>1</id>
		<student_number>26</student_number>
		<first_name>Mariah</first_name>
		<last_name>Kelly</last_name>
		<email>richardtrujillo@yahoo.com</email>
	</student>
	<student>
		<id>2</id>
		<student_number>94</student_number>
		<first_name>Donna</first_name>
		<last_name>Nash</last_name>
		<email>alexandriaswanson@gonzalez.com</email>
	</student>
	<student>
		<id>3</id>
		<student_number>58</student_number>
		<first_name>Brittany</first_name>
		<last_name>Ramirez</last_name>
		<email>bthompson@johnson-morgan.com</email>
	</student>
</students>
```