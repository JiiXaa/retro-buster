# retroBuster

## About

The **"retroBuster"** VHS Cassettes Rental Management app, a solution designed for customers who enjoy the nostalgia of old-school films. This app provides an easy and convenient way to manage a VHS cassettes rental shop. With its user-friendly design, this app makes it simple to manage the available cassettes, keep track of new and existing customers, and stay up to date on who has borrowed what movie and when.

## Pseudocode:

- [] Create navigation for the project for the following endpoints:

  - [x] main page,
  - [x] videocassettes (VHS),
  - [x] VHS add,
  - [] login,
  - [] registration,
  - [] contact,

- [] Registration/Login logic

  - [] Registration: need to figure out how will registration work in the project as it will be only limited registered people/users (mainly the employees of the retroBuster shop).
    - [] Initial idea: When registering a user there will be input field (token) needed to be successfully registered. In that scenario the token would be provided to the potential employee by the owner or manager.
    - [] Password needs to be hashed during registration (can use: werkzeug.security: generate_password_hash or bcrypt)
    - [] Repeat password (to ensure the password is correct)
    - [] Inputs need to be validated (for: fields are required, password length, password special characters)
  - [] - Login:
    - [] Input validations
    - [] compare a password with the hash stored in the database

- [] Show 'flash' messages to provide feedback about the status of the user's actions, or to guide the user through the app.

- [x] Create VHS db model, and display all available video cassettes in the template. Route '/videocassettes'
- [x] Add view for adding a videocassette (VHS). Route 'videocassettes/add_vhs'
  - [x] Add form which adds a videocassette (VHS) on submit
- [x] Add view for removing a videocassette (VHS) (delete button located next to the title)
  - [x] When user clicks the delete button, show confirmation page including a form. When form is submitted the corresponding videocassette (VHS) entry is removed from database.
- [x] Add view for editing a VHS (edit button located next to the title)
  - [x] When a user clicks the edit button, a form is displayed with inputs pre-filled with the corresponding videocassette (VHS) data. Upon submitting the form, the entry for that videocassette is updated in the database.

### Database relationship model prototyping:

Database prototyping/building uses the SQLite library and the final version is stored on the ElephantSQL (PostgreSQL database hosting service)

- [] Videocassette class needs to have a one-to-one relationship with the Details class. Details instance will hold all important information about the the particular videocassette connected to it.

## TEST/BUGS:

- bugs:
  [x] videocassette (VHS) search only works for the single input search, need to fix the query for multiple inputs.

## dirty notes for the development only!

### Third-party packages used:

UUID used for generating unique primary keys for tables in database.

### Credits:

- I have decided to create a well organized folder and file structure in my project, as I believe it greatly improves code readability and makes navigating the codebase way easier. After thorough research, I have implemented a common folder and file structure. Article can be found here: <br>
  https://stackoverflow.com/questions/14415500/

- I also chosen to use the Flask Blueprint Architecture, the article can be found here: <br>
  https://realpython.com/flask-blueprint/ <br>
  https://hackersandslackers.com/flask-blueprints/ <br>
