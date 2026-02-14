# How to Run

Follow this step-by-step guide to set up and run the program.

## Prerequisites

Before starting, ensure you have installed the necessary dependencies. Navigate to the `Share_detials_with_va` directory and run:

```bash
pip install -r requirements.txt


Step-by-Step Guide
1. Start the Backend Server

Open a new terminal window and run the following commands to navigate to the backend folder and start the server:
Bash
cd app_bundle/backend
python -m uvicorn app.main:app --reload


2. Run the Voice Assistant
Open the voice assistant folder and execute the test file:

Bash
# Assuming you are in the voice assistant directory
python jarvis_test.py

### Tips for your README
* **Code Blocks:** I used `bash` highlighting in the code blocks so the commands stand out and are easy for users to copy.
* **Structure:** I separated the "Prerequisites" (installation) from the "Execution" (running the app) to make it standard for GitHub projects.

Would you like me to generate a `requirements.txt` file template for this project as well?