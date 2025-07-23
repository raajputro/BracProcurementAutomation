What to do first:

Install Pycharm Community Edition to your system

Install Python to your system

Install Git to your system

Clone the repository to your system

Open the cloned folder in Pycharm IDE

Create a Virtual Environment and activate it

                  python -m venv venv
 for windows:       venv\Scripts\activate
 for linux/macOS:   source venv/bin/activate
Open a terminal, upgrade pip first, then do the following

 python -m pip install --upgrade pip
 pip install -r requirements.txt
 playwright install
Tools installed here:

Playwright → An automation library to perform end-to-end web testing or web automation. → https://playwright.dev/python/

Pytest → A test framework. → https://docs.pytest.org/en/stable/

Rich → Renders Python tracebacks with syntax highlighting and formatting. → https://rich.readthedocs.io/en/stable/traceback.html

What will we do:

We will be using the POM design pattern here, where we will create web pages and store them in /pages folder,

write our tests [test cases or test suites] in /tests/test_cases/ folder

create a .env file and store our required credentials there, just as shown in the .env.example file

write commonly used methods to interact with in /utils folder

How to run the test:

Run the following command in the Pycharm Terminal for the preferred test run:

-> To run all tests: pytest

-> To run a selected test: pytest ./tests/test_cases/your_desired_test_file_name.py