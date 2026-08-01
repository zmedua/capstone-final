
 Workout Tracker

A full-stack workout tracking application that allows users to securely create, organize, and track their workouts. Users can create accounts, manage personalized workout plans, add exercises, mark workouts as completed, view workout history, and save favorite exercises.

Features
User Authentication
User signup
User login
Secure password hashing with Flask-Bcrypt
Session-based authentication
Protected routes
Workout Management
Create workouts
View workouts
Edit workouts
Delete workouts
Mark workouts as completed
View workout history
Exercise Management
Browse exercises
Add exercises to workouts
Remove exercises from workouts
Record:
Sets
Repetitions
Weight
Cardio duration
Favorites
Save favorite exercises
Remove favorite exercises
Quickly access frequently used exercises
Search & Filtering
Search exercises by name
Filter by category
Filter by muscle group
Filter by difficulty
Technologies Used
Frontend
React
React Router
JavaScript
HTML
CSS
Fetch API
Backend
Python
Flask
SQLAlchemy
Flask-Migrate
Flask-Bcrypt
Marshmallow
SQLite
Development Tools
Git
GitHub
VS Code
Database Models
User
Workout
Exercise
WorkoutExercise (Join Table)
FavoriteExercise
Relationships
One User has many Workouts.
One User has many Favorite Exercises.
One Workout has many WorkoutExercises.
One Exercise can belong to many WorkoutExercises.
Workouts and Exercises are connected through the WorkoutExercise join table.
Installation
Clone the repository
git clone https://github.com/zmedua/capstone-rough-draft.git
cd capstone-rough-draft
Backend
cd server

pipenv install

pipenv shell

flask db upgrade

python seed.py

python app.py
Frontend
cd ../client

npm install

npm start
Future Improvements
ExerciseDB API integration
Exercise images and descriptions
Progress charts and workout analytics
Improved dashboard
Enhanced responsive design
Workout templates
Author

Zane Medua

GitHub: https://github.com/zmedua

LinkedIn: https://www.linkedin.com/in/zanemedua/



# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
