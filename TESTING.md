# Testing the Travel Agent Management System

This document provides information on how to test the Travel Agent Management System application.

## Automated Testing

The project includes a test suite powered by pytest. To run the automated tests:

1. Make sure you have installed the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the tests using pytest:
   ```bash
   pytest -v
   ```

3. Alternatively, use the provided test script:
   ```bash
   ./test_setup.sh
   ```

## Manual Testing

### Setting Up for Testing

1. Run the setup script to create a virtual environment, install dependencies, and initialize the database:
   ```bash
   ./run.sh
   ```

2. Choose option 1 for the simple application or option 2 for the full application.

### Test Cases

#### Authentication
1. **Login with valid credentials**
   - Navigate to the login page
   - Enter username: `admin` and password: `admin123`
   - Expected: Successfully redirected to dashboard

2. **Login with invalid credentials**
   - Navigate to the login page
   - Enter incorrect username or password
   - Expected: Error message displayed

3. **Logout**
   - Click on logout link when logged in
   - Expected: Successfully logged out and redirected to home page

#### Travel Packages
1. **View all packages**
   - After login, navigate to Packages
   - Expected: List of available travel packages

2. **Create new package**
   - Navigate to Create Package form
   - Fill in required details and submit
   - Expected: New package created and displayed in package list

3. **View package details**
   - Click on a specific package
   - Expected: Detailed view of the package

#### Customer Management
1. **View all customers**
   - Navigate to Customers section
   - Expected: List of all customers

2. **Add new customer**
   - Fill in customer add form with valid data
   - Expected: Customer added to system

#### Booking Management
1. **Create new booking**
   - Select a customer and package
   - Fill in booking details
   - Expected: Booking created successfully

2. **View all bookings**
   - Navigate to bookings list
   - Expected: All bookings displayed

3. **Update booking status**
   - Change status of a booking
   - Expected: Status updated successfully

### Testing on Different Browsers

Test the application on multiple browsers to ensure compatibility:
- Google Chrome
- Firefox
- Safari (if available)

### Mobile Responsiveness

Test the application on different device sizes to ensure the interface is responsive:
- Desktop
- Tablet
- Mobile phone

## Reporting Issues

If you encounter any issues while testing, please document:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Screenshots (if applicable)
5. Environment details (browser, OS)
