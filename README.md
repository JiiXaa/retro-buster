# retroBuster

## About

The **"retroBuster"** VHS Cassettes Rental Management app, a solution designed for customers who enjoy the nostalgia of old-school films. This app provides an easy and convenient way to manage a VHS cassettes rental shop. With its user-friendly design, this app makes it simple to manage the available cassettes, keep track of new and existing customers, and stay up to date on who has borrowed what movie and when.

## Quick Overview:

A registered cashier (main user) can login and get the access to the list of available VHS tapes for all movies, list of registered customers and manage rental data associated with them:

- User have a access to the all movies available in the store and see all information like title, director, genre, total copies, available copies, date added etc.
- User can add movies and vhs tape copies associated with them.
- User can edit / delete movies and vhs tape copies associated with them.
- User can search movie by title, director or genre criteria (functionality works for multiple criteria search i.e. can look for a movie tile and genre etc.)
- User can see which copies are available or rented.
- User can rent/check-in movies for a existing customer.
- User can see history for a specific VHS tape copy from the movie details page. History data contains information: director, genre, customer, rent date, return date, due date, rent days.
- User can add, edit, delete and view customer page information.
  - Customer details page contains the information about customer, form to rent a movie from the customer page (need to specify a movie title and available copy number). Also user can access rental history for all active or previously rented movies.
- User can search customer by first name, last name and email (functionality works for multiple criteria search i.e. can look for a last name and email etc.)
- User can see all rental history (active and returned)
- User can access archived rentals from the rentals page

  - if deleted VHS tape copy has a rental history it is considered and added to archived rentals.

- Deleting movies from the database uses a hard deletion and all associated history is also deleted,
- Deleting VHS copy of a movie uses a soft deletion to be able to preserve all history of VHS tapes.
- Deleting customer uses hard deletion but all associated rental history is available after deleting. Every information with deleted customer says that customer does not exist or N/A.

Every user interaction/actions are confirmed with use of Flask's flash messages, i.e. after user edits a movie, app displays information that "movie updated successfully". Every pop up information disappear after 5 seconds.

**Home page** have quick access to the search movies/customers functionality and see the list of the movies that are due to be returned today.

**Main movies** page displays list of paginated movies (8 movies per page). Movies can be sorted by date added, title, director, genre or rating. Each movie container shows:

- image (image can be only added with existing URL, upload images is not implemented at this point),
- list of vhs tape copies (available / rented out),
- information about a movie,
- actions to edit, delete, view details page for a movie.

**Main customers** page displays list of customers, each container render customer first name, last name, email and actions such as edit, delete, view details for a customer.

**Rental history** page displays all rental history (active / returned).

**Archive rentals** page can be accessed from the rental history page, and display data for the deleted VHS copies.

## Database

### Database features:

- App using ElephantSQL hosting platform for storing Postgres database,
- Used soft delete technique to mark records as deleted without actually removing them from the database, it helps with:
  - Data recovery, accidentally removed data or recover historical data (Rentals vs. ArchivedRentals)
  - Data integrity, foreign key constraints, and complex relationships between tables.
    More information about soft delete can be found here: https://blog.miguelgrinberg.com/post/implementing-the-soft-delete-pattern-with-flask-and-sqlalchemy

### Database relationship model prototyping:

Database prototyping/building uses the SQLite library and the final version is stored on the ElephantSQL (PostgreSQL database hosting service)

- [x] 'Movie' class needs to have a one-to-many relationship with the 'VhsTapeCopy' class. 'VhsTapeCopy' instance will hold all important information about the all instances (vhs copies) connected to it (copy number/id, date added, is available, is removed).
- [x] 'VhsTapeCopy' (tape copy) class needs to have many-to-one relationship with the 'VhsRental' model to be able to track rental information such as which customer has rented that particular copy, when was borrowed, due to bring back.
- [x] 'VhsRental' class needs to have many-to-one relationship with 'Customer' as one customer can have multiple rental transaction/movies rented at the same time.
- [x] 'ArchivedRental' class needs to have many-to-one relationship with 'Movie' meaning that one movie can have multiple archived rentals.
- [x] 'VhsTapeCopy' needs to have many-to-one relationship with 'ArchivedRental' and 'VhsRental' meaning that one VHS tape copy can have multiple rentals or archived rentals.

### Database relationships final:

The database schema is represented using Python classes:

- **Movie**: Represents a movie title, with attributes such as title, director, genre, length, year, rating, description, and image. Each movie can have multiple VhsTapeCopy entries, multiple VhsRental entries, and multiple ArchivedRental entries associated with it.

  - Movie table has a one-to-many relationship with VhsTapeCopy table (physical representation of a VHS tape for a movie). Each movie can have multiple VhsTapeCopy entries (each VhsTapeCopy instance belongs to only one movie)

  - Movie table also has a one-to-many relationship with VhsRental table. Each movie can be rented multiple times, but each VhsRental entry belongs to only one movie.

  - Movie table has a one-to-many relationship with ArchivedRental table. Each movie can be archived multiple times, but each ArchivedRental entry belongs to only one movie.

- **VhsTapeCopy**: Represents a physical VHS tape copy for a movie, with attributes such as date added, copy number, availability status, and removed status. Each VhsTapeCopy entry belongs to only one movie and can have multiple VhsRental entries and multiple ArchivedRental entries associated with it.

  - VhsTapeCopy table has a one-to-many relationship with VhsRental table. Each VhsTapeCopy entry can be rented multiple times, but each VhsRental entry belongs to only one VhsTapeCopy entry.

  - VhsTapeCopy table also has a one-to-many relationship with ArchivedRental table. Each VhsTapeCopy entry can be archived multiple times, but each ArchivedRental entry belongs to only one VhsTapeCopy entry.

- **Customer**: Represents a customer, with attributes such as first name, last name, and email. Each customer can have multiple VhsRental entries and multiple ArchivedRental entries associated with it.

  - Customer table has a one-to-many relationship with VhsRental table. Each customer can rent multiple movies, but each VhsRental entry belongs to only one customer.

  - Customer table also has a one-to-many relationship with ArchivedRental table. Each customer can have multiple archived rentals, but each ArchivedRental entry belongs to only one customer.

- **User**: Represents a user (cashier) account, with attributes such as username, first name, last name, email, and hashed password. Each user can have multiple VhsTapeCopy entries and multiple ArchivedRental entries associated with it (It allow to see cashier history for removing/renting specific vhs tapes).

  - User table has a one-to-many relationship with VhsTapeCopy table. Each user can have multiple VhsTapeCopy entries, but each VhsTapeCopy entry belongs to only one user.

  - User table also has a one-to-many relationship with ArchivedRental table. Each user can have multiple archived rentals, but each ArchivedRental entry belongs to only one user.

- **VhsRental**: Represents rental history for a specific VHS tape copy, with attributes such as date rented, due date, return date, late status, and removed status (soft deletetion). Each VhsRental entry belongs to one customer, one VhsTapeCopy entry, and one movie.

**ArchivedRental**: Represents archived rental history for a deleted VHS tape copy, with attributes such as date rented, date returned, date archived, and user ID. Each ArchivedRental entry belongs to one customer, one VhsTapeCopy entry, and one movie.

## Development

### Pseudocode:

- [x] Create navigation for the project for the following endpoints:

  - [] main page (Could use advertisement data for cashiers to easily promote new or featured VHS tapes, and other deals to customers. Display this information to quickly recommend products and increase sales. This can also help manage inventory and promote slow-moving products.) - (loose design idea: could have 10 featured record shown, and if there is less featured tapes at the time in the database, could add if statement for adding popular tapes to populate missing numbers),
  - [x] Customers,
  - [x] Customers search/filter,
  - [x] Customer add,
  - [x] Movies main page, show all available movies with necessary details (this would be good idea to incorporate pagination to help improve loading time of the page by requesting 8 records)
  - [x] Movies search/sort by date, title, director, genre and rating,
  - [x] Movie add (Add movie title to database),
    - [x] VHS tape copy add (Add copy tapes of the movie),
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
- [x] Add view for adding a videocassette (VHS). Route 'movies/vhs_add_tape'
  - [x] Add form which adds a videocassette (VHS) on submit
- [x] Add view for removing a videocassette (VHS) (delete button located next to the title)
  - [x] When user clicks the delete button, show confirmation page including a form. When form is submitted the corresponding videocassette (VHS) entry is marked as removed (is_removed flag).
  - [x] When videocassette (VHS) is 'deleted' by the user, all rental history associated with that tape copy is moved to archived rentals page.
- [x] Add view for editing a VHS (edit button located next to the title)
- [x] Add sort movies functionality by: date, title, director, genre and rating.

  - [x] When a user clicks the edit button, a form is displayed with inputs pre-filled with the corresponding videocassette (VHS) data. Upon submitting the form, the entry for that videocassette is updated in the database.

- [x] Rental history - active/archived
  - [x] Deleting a VHS tape copy will not delete it from the database but set the is_removed flag to True. That is to avoid the constraint errors and keep relations between removed VHS tape copies, active rentals and archived rentals.
  - [x] Show active rentals on the rentals page.
  - [x] Archived rentals link located in the rentals page to be able to see archived rentals for deleted VHS tape copy.

### BUGS/IMPROVEMENTS:

- **Bugs:** <br>
  [x] videocassette (VHS) search only works for the single input search, need to fix the query for multiple inputs.<br>
  [] flash messages need to have separate styles for success and error state. For now all messages are displayed with the same green background pop-up. Would be nice to have a distinction between them i.e. success action = green popup, error = red popup.<br>
  [] When a user attempts to delete or edit a movie and presses the cancel button, they are currently redirected to the main movie page. It would be more convenient if the user could be redirected back to the specific movie page they were on before attempting the action.<br>
  [] When a user attempts to delete or edit a customer profile and presses the cancel button, they are currently redirected to the main customer page. It would be more convenient if the user could be redirected back to the specific customer profile page they were on before attempting the action.<br>

- **Improvements:** <br>
  [] To help users recommend certain movies to customers, it is planned to display featured movies on the main page in a slider/carousel format. The backend functionality for this feature is complete, and the front-end functionality using JavaScript has also been implemented and is currently displayed on desktop. However, to make the slider/carousel interactive, a third-party library will need to be added.<br>

## dirty notes for the development only!

### Third-party packages used:

UUID used for generating unique primary keys for tables in database.

### Credits:

- I have decided to create a well organized folder and file structure in my project, as I believe it greatly improves code readability and makes navigating the codebase way easier. After thorough research, I have implemented a common folder and file structure. Article can be found here: <br>
  https://stackoverflow.com/questions/14415500/

- I also chosen to use the Flask Blueprint Architecture, the article can be found here: <br>
  https://realpython.com/flask-blueprint/ <br>
  https://hackersandslackers.com/flask-blueprints/ <br>
