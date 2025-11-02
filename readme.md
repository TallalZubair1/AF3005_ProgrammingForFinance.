Secure FinTech Portal (Assignment)

This is a mini-application developed for a cybersecurity assignment. It simulates a small FinTech (Financial Technology) portal with a focus on implementing and testing security-aware features.

The entire application is built as a single-file web app using HTML, Tailwind CSS, and plain JavaScript. It uses the browser's localStorage and sessionStorage to simulate a database and user sessions.

Features Implemented (as per requirements)

This application includes all the required features to allow for meaningful manual security testing:

User Registration & Login: (Test 1, 4, 11, 16)

Simulates a user database in localStorage.

Passwords are hashed using the Web Crypto API (SHA-256) before being stored.

Password Validation: (Test 2, 13)

Enforces strong password rules on the client-side (8+ chars, 1 number, 1 symbol).

Input Forms: (Test 3, 10, 12, 19, 20)

Provides forms for transactions, profile updates, etc.

Includes input validation (numeric, length) and sanitization (to prevent XSS).

Session Management: (Test 4, 5, 6)

Uses sessionStorage to maintain a user's logged-in state.

Includes an automatic logout timer (session expiry).

Includes a functional logout button.

Data Storage Layer: (Test 7, 18)

Simulated in localStorage.

Passwords are hashed (Test 7).

Sensitive user notes are encrypted (Test 18).

Error Handling: (Test 9, 17)

All functional logic is wrapped in try...catch blocks.

Users are shown generic error messages (e.g., "An unexpected error occurred") instead of specific stack traces.

Encryption / Decryption Option: (Test 18)

A "Secure Note" feature allows a user to encrypt data using their password (AES-GCM) and save it to localStorage. They can only decrypt it with the same password.

Audit / Activity Logs:

Tracks user actions (login, logout, registration, profile update) in a separate localStorage "table."

Profile Update Page: (Test 14)

Allows a logged-in user to update their email and bio.

Demonstrates access control, as a user can only edit their own profile.

File Upload Validation: (Test 8)

Includes a file input that validates the file type and extension (.txt, .pdf) on the client side.

How to Run

Download the secure-fintech-app.html file.

Double-click the file to open it in any modern web browser (e.g., Chrome, Firefox, Edge).

The application is now running.