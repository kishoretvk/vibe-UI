# Generative UI: Enhanced Data App

This project is a Generative UI designed to visualize any arbitrary JSON data. It provides a flexible and interactive platform for exploring datasets through dynamic graphs, a comprehensive dashboard, and a data exploration view with dynamic filtering capabilities. The application supports both Dark and Light themes for a personalized user experience.

Built with React Native code, this UI minimizes external dependencies, resulting in a simple, easy-to-manage, and highly portable codebase.

## Features

*   **Dynamic Data Handling:** Ingest and process any valid JSON data structure for visualization and exploration.
*   **Dashboard:** Get an overview of key data insights and visualizations.
*   **Metrics Explorer:** Interactively explore data metrics with dynamic filtering based on the loaded JSON structure.
*   **Data Visualization:** Display data effectively using various graph types.
*   **Theme Support:** Seamlessly switch between visually distinct Dark and Light themes.
*   **Simplified Architecture:** Developed using React Native code to reduce reliance on external modules, enhancing maintainability.

## Setup and Installation

To get the Enhanced Data App running locally, follow these steps:

### Prerequisites

*   Node.js and npm (or yarn)
*   Python 3 and pip

### Frontend Setup

1.  Navigate to the project root directory in your terminal.
2.  Install the frontend dependencies:
    ```bash
    npm install
    ```
    or
    ```bash
    yarn install
    ```
3.  Start the frontend development server:
    ```bash
    npm start
    ```
    or
    ```bash
    yarn start
    ```
    The frontend should now be running, likely accessible at `http://localhost:5173` (check your terminal output for the exact URL).

### Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Install the backend dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the backend server:
    ```bash
    python app.py
    ```
    The backend server should now be running, likely accessible at `http://127.0.0.1:5000` (check your terminal output).

## Getting Started

1.  Ensure both the frontend and backend servers are running.
2.  Open your web browser and navigate to the frontend URL (e.g., `http://localhost:5173`).
3.  Load your JSON data into the application (details on how to load data might depend on the specific implementation within the app).
4.  Explore the Dashboard, Metrics Explorer, and Chat Assistant tabs to interact with your data.
5.  Toggle between Dark and Light themes using the theme toggle button.

## Screenshots

Here are some screenshots of the application:

![Screenshot 2025-04-21 at 8.58.06 AM](https://github.com/kishoretvk/vibe-UI/blob/main/Screenshot%202025-04-21%20at%208.58.06%E2%80%AFAM.png)
![Screenshot 2025-04-21 at 9.12.52 PM](https://github.com/kishoretvk/vibe-UI/raw/main/Screenshot%202025-04-21%20at%209.12.52%20PM.png)
![Screenshot 2025-05-04 at 12.17.26 PM](https://github.com/kishoretvk/vibe-UI/raw/main/Screenshot%202025-05-04%20at%2012.17.26%20PM.png)
![Screenshot 2025-05-04 at 12.17.41 PM](https://github.com/kishoretvk/vibe-UI/raw/main/Screenshot%202025-05-04%20at%2012.17.41%20PM.png)

## Contribution and Deployment

Information on contributing to the project or deploying it to a hosting platform can be added here. Pushing the code to a repository like GitHub is a common next step for collaboration and version control.
