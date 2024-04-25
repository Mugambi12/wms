# Water Management System

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/mugambi12/water_management_system?color=blueviolet)
![Number of lines of code](https://img.shields.io/tokei/lines/github/mugambi12/water_management_system?color=blueviolet)
![Code language count](https://img.shields.io/github/languages/count/mugambi12/water_management_system?color=blue)
![GitHub top language](https://img.shields.io/github/languages/top/mugambi12/water_management_system?color=blue)
![GitHub last commit](https://img.shields.io/github/last-commit/mugambi12/water_management_system?color=brightgreen)

![Water Management System Demo](./app/frontend/static/images/readme/dashboard.png)

## Overview

The Water Management System is a Flask-based web application designed to streamline and optimize water management processes. It empowers users with various functionalities, including:

- **Secure user management:** Facilitates secure user registration, login, and logout. Additionally, provides a password reset feature to allow users to securely reset their passwords in case they forget them.
- **Role-based access control:** Enhances security by assigning different access levels (e.g., standard user, administrator).
- **Dynamic dashboards:** Provides users with personalized insights into their water usage patterns through interactive charts and graphs.
- **Water consumption and expense tracking:** Enables users to monitor their water consumption and associated expenses, promoting accountability and responsible water use.
- **Real-time chat:** Fosters communication and collaboration among users.
- **Admin broadcast messages:** Allows administrators to keep users informed through announcements and updates.
- **Feedback tracking system:** Gathers valuable user input to facilitate continuous improvement of the application.

This technology-driven approach aims to address water sustainability challenges by empowering users and encouraging responsible water management practices.

## Tech Stack

The Water Management System utilizes the following technologies:

- Python for backend development
- Flask for web framework
- Blueprints for modular structure
- WebSockets(Flask-SocketIO) for real-time communication
- Bootstrap, CSS, and HTML for frontend design
- JavaScript for interactive elements

## Getting Started

### Prerequisites

Before you start using the Water Management System, ensure you have the following prerequisites installed and configured on your system:

- **Python:** The system is built using Python, so ensure you have Python installed. You can download and install Python from the [official Python website](https://www.python.org/).

- **Virtual Environment (optional but recommended):** It's recommended to use a virtual environment to manage dependencies and isolate the project environment. You can create a virtual environment using `virtualenv` or `venv` module, which comes built-in with Python.

  #### Alternative: 1.

  ##### Using venv (Python 3)

  ```cmd
  > python -m venv venv
  > venv\Scripts\activate
  ```

  #### Alternative: 2.

  ##### Using virtualenv

  ```cmd
  > pip install virtualenv
  > virtualenv venv
  > venv\Scripts\activate
  ```

### Installation

Follow these steps to set up the Water Management System on your local machine:

1. **Clone the repository:**

   ```cmd
   > git clone https://github.com/mugambi12/water_management_system.git
   > cd water_management_system
   ```

2. **Install dependencies:**

   Navigate to the project directory and install the required dependencies using pip:

   ```cmd
   > pip install -r requirements.txt
   ```

### Usage

Once you have completed the installation, follow these steps to run the Water Management System:

1. **Navigate to `WMS` folder**

   ```cmd
   > cd wms
   ```

1. **Run the application:**

   Start the Flask server by executing the following command from the project directory:

   #### Alternative: 1.

   ```cmd
   > python run.py
   ```

   #### Alternative: 2.

   ```cmd
   > flask run
   ```

   By default, the application will be accessible at `http://localhost:5000`.

1. **Access the application:**

   Open your web browser and navigate to `http://localhost:5000` to access the Water Management System.

1. **Explore the features:**

   Once the application is running, you can explore its various features, including user management, dashboards, water consumption tracking, real-time chat, and more.

1. **Contribute (optional):**

   If you would like to contribute to the project, feel free to fork the repository, make your changes, and submit a pull request. Your contributions are highly appreciated!

---
