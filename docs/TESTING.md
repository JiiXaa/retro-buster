# Testing

The retroBuster VHS rental management website has been tested the following criteria:

## Code Validation

### Lighthouse

I used lighthouse in chrome developer tools to test each of the pages for:

- Performance - how the page performs whilst loading.
- Accessibility - how accessible is the site for all users and how can it be improved.
- Best practices - how does the site conform to industry best practices.
- SEO - search engine optimization. Is the site optimized for search engine result rankings.

<img width="460" alt="Lighthouse audit result" src="https://github.com/JiiXaa/retro-buster/raw/main/screenshots/lighthouse-audit.png">

### W3C HTML Validator

Html checker does not show any errors.

### W3C CSS Validator

CSS checker shows only one error which comes from Font Awesome cdn import file related to the 'rotate' CSS property is being set to a custom CSS variable '--fa-rotate-angle', which is causing the validator to flag it as an error. It is safe to ignore it in this case because that property is used correctly by Font Awesome.

```css URI : https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css
.fa-rotate-by 	var(--fa-rotate-angle, none) is not a transform value : rotate(var(--fa-rotate-angle, none))
```

## Manual Testing

### Navigation:

#### User not logged in:

- [x] Click on Home link redirects to main page for unlogged user.
- [x] Click on Login link redirects to login page.
- [x] Click on Register link redirects to register page.

#### User logged in:

- [x] For mobile screen size check if the hamburger menu opens the mobile menu.
- [x] Click on the website's logo redirects to main page.
- [x] Click on Home link redirects to main page.
- [x] Click on Customer link redirects to customer list page.
- [x] Click on Search Customer link redirects to search customer page.
- [x] Click on Add Customer link redirects to add customer page.
- [x] Click on Search Movies link redirects to search movies page.
- [x] Click on Add Movies link redirects to add movies page.
- [x] Click on Rental link redirects to rental page.
- [x] Click on User Dashboard link redirects to user dashboard page.
- [x] Click on Logout link redirects to login page.

### Footer

- [x] Social media links redirect to the Github, LinkedIn or Facebook

### Submit Login/Register Form:

- [x] Try to submit.
- [x] Try to submit the empty form and verify that an error message about the required fields appears.
- [x] Try to submit the form with an invalid email address and verify that a relevant error message appears.
- [x] Try to submit the form with all inputs valid and verify that a success message appears.

- [x] If user exists in database submitting login form redirects to the user dashboard page.
- [x] Login action: If user does not exist, user is notified: **"Invalid username or password."**

- [x] Registration action: successful submitting registration form adds a user to the database.

### Customer page:

- [x] Quick search form allows to search for a specific customer by name/email criteria.
- [x] Page displays list of all registered customers.

### Movies page:

- [x] Quick search form allows to search for a specific movie by title/director/genre criteria.
- [x] Sort displayed movies by date/title/director/genre/rating criteria.
- [x] Pagination buttons on click opens a 8 different movie entries depending on a page number.
- [x] Page displays list of all movies (8 titles per page)

- [x] Movie edit button opens movie edit page
- [x] Movie delete button opens movie delete page
- [x] Movie details button opens movie details page

- [x] All information from database for a movie (copies available, which copies are available or rented out, movie details) are correct.

### Add VHS Copy Page

- [x] Submitting add copy number form adds a VHS tape copy to the database.
- [x] Vhs history displays all available and removed VHS copies

### Rentals page:

- [x] Archived rentals button redirects to the archived rentals page.
- [x] Active rentals pop-up shows actively rented movies if any or information "No active rentals in the database"
- [x] List of returned movies is displayed correctly.

### Page 404:

- [x] If wrong URL used, user see the custom 404.html page.
- [x] Go back button redirects user to the main page on click.

### Rent Movie:

Renting a VHS tape can be submitted from the movie detail page and clicking on specific VHS tape entry's 'RENT' link

- [x] Submitting rent movie with customer email creates rental entry.
- [x] Clicking back button goes back to the movie details

VHS tape also can be rented from the customer profile page:

- [x] Submitting rent VHS form with movie title and copy number creates rental entry.

### Add Movie:

- [x] Submitting movie add form adds a movie to the database.
- [x] Successful/unsuccessful movie added shows flash message to the user that movie is added or not.

### Search Movie

- [x] Search movie functionality display movie found.
- [x] Movie can be searched by multiple criteria i.e. director and title.

### Add Customer:

- [x] Submitting customer add form adds a customer to the database.
- [x] Successful/unsuccessful customer added shows flash message to the user that customer is added or not.

### Search Customer

- [x] Search movie functionality display movie found.
- [x] Customer can be searched by multiple criteria i.e. last name and email

### Rental History for deleted customer

- [x] Rental history information with deleted customer shows "Customer: N/A"

### Rental History for deleted VHS tape

- [x] Rental history for deleted VHS tape copy is moved to the archived rental history.
- [x] Deleted VHS tape is not removed from database (soft deletion), its is_removed flag in the database model is set to true and removed from VHS stock.

### Flash Messages

- [x] Adding movie show message to the user that movie was added to the database.
- [x] Searching for movie displays:
  - if found: Search results for (searched query)
  - if not found: No results found
- [x] Editing movie show message that movie was updated successfully.
- [x] Deleting movie show message that movie was deleted successfully.
- [x] Adding VHS tape copy shows message that copy was added to the database.
- [x] Renting VHS tape copy shows:
  - if available: "VHS tape rented successfully"
  - if customer have 5 active rentals: "Customer has already rented out the maximum number of VHS tapes."
- [x] Deleting VHS tape copy:
  - Deleting VHS tape requires a title confirmation, and if is not correct: "Movie title does not match."
  - If title confirmation matches: "Movie deleted successfully."
  - If movie have active VHS rentals" "Cannot delete movie with tapes checked out."

## Applications used to test the project:

- DBeaver used to test the SQL database

## Bugs

- Constant unit test was done as the features were added. Fixed, checked with appropriate commit messages. No official tracking system was used as the project scope was relatively small.

### Outstanding Bugs

- No outstanding bugs exist at this time that the developer is aware of.

## MAIN PAGE (README)

[Back to Main README](https://github.com/JiiXaa/retro-buster#testing)
