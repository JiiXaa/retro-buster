# retroBuster

## About

The **"retroBuster"** VHS Cassettes Rental Management app, a solution designed for customers who enjoy the nostalgia of old-school films. This app provides an easy and convenient way to manage a VHS cassettes rental shop. With its user-friendly design, this app makes it simple to manage the available cassettes, keep track of new and existing customers, and stay up to date on who has borrowed what movie and when.

## Pseudocode:

- [] Create navigation for the project for the following endpoints:

  - [] main page (Could use advertisement data for cashiers to easily promote new or featured VHS tapes, and other deals to customers. Display this information to quickly recommend products and increase sales. This can also help manage inventory and promote slow-moving products.) - (loose design idea: could have 10 featured record shown, and if there is less featured tapes at the time in the database, could add if statement for adding popular tapes to populate missing numbers),
  - [x] Customers,
  - [x] Customers search/filter,
  - [x] Customer add,
  - [x] videocassettes (VHS),
  - [x] VHS main page (show all available VHS list, this would be good idea to incorporate pagination to help improve loading time of the page by requesting 10-20 records or so)
  - [x] Movie add (Add movie title to database),
  - [] tape add (Add copy tapes of the movie),
  - [x] VHS search/filter,
  - [x] login,
  - [x] registration,
  - [] contact,

- [x] Registration/Login logic

  - [x] Registration: need to figure out how will registration work in the project as it will be only limited registered people/users (mainly the employees of the retroBuster shop).
    - [x] Initial idea: When registering a user there will be input field (token) needed to be successfully registered. In that scenario the token would be provided to the potential employee by the owner or manager.
    - [x] Password needs to be hashed during registration (can use: werkzeug.security: generate_password_hash or bcrypt)
    - [x] Repeat password (to ensure the password is correct)
    - [x] Inputs need to be validated (for: fields are required, password length, password special characters)
  - [x] - Login:
    - [x] Input validations
    - [x] compare a password with the hash stored in the database

- [x] Show 'flash' messages to provide feedback about the status of the user's actions, or to guide the user through the app.

- [x] Create VHS db model, and display all available video cassettes in the template. Route '/videocassettes'
- [x] Add view for adding a videocassette (VHS). Route 'videocassettes/add_vhs'
  - [x] Add form which adds a videocassette (VHS) on submit
- [x] Add view for removing a videocassette (VHS) (delete button located next to the title)
  - [x] When user clicks the delete button, show confirmation page including a form. When form is submitted the corresponding videocassette (VHS) entry is removed from database.
- [x] Add view for editing a VHS (edit button located next to the title)
- [x] Add sort movies functionality by: date, title, director, genre and rating.

  - [x] When a user clicks the edit button, a form is displayed with inputs pre-filled with the corresponding videocassette (VHS) data. Upon submitting the form, the entry for that videocassette is updated in the database.

- [] Rental history - active/archived
  - [x] Deleting a VHS tape copy will not delete it from the database but set the is_removed flag to True. That is to avoid the constraint errors and keep relations between removed VHS tape copies, active rentals and archived rentals.
  - [x] Show active rentals on the rentals page.
  - [] Archived rentals link located in the rentals page to be able to see archived rentals for deleted VHS tape copy.

### Database relationship model prototyping:

Database prototyping/building uses the SQLite library and the final version is stored on the ElephantSQL (PostgreSQL database hosting service)

- [x] 'Videocassette' class needs to have a one-to-many relationship with the 'VhsDetails' class. 'VhsDetails' instance will hold all important information about the all instances (vhs copies) connected to it (copy number/id, date added, is available).
- [x] 'VhsDetails' (tape copy) class needs to have many-to-one relationship with the 'VhsRental' model to be able to track rental information such as which customer has rented that particular copy, when was borrowed, due to bring back.
- [x] 'VhsRental' class needs to have many-to-one relationship with 'Customer' as one customer can have multiple rental transaction/movies rented at the same time.

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
