# ScraperAnalysisAI

# You have to follow the readme guidelines to run the project. It works great with streamlit server and it takes excel input file and allows you to download the output as csv and saves the data in the pgsql database that you have to set up. It requires that you have a preinstalled pgsql admin for desktop with username, hostname, port, password. You can create database and table with sql_queries.txt and change their names in your .env file and  Trajectory_task/scraper.py. You have to add your own api key in the .env file. It requires that you have a chrome and chrome driver.

# How to use:
- clone the github repo: git clone https://github.com/GitCodeSM/ScraperAnalysisAI.git
- install from the requirements.txt. Ignore package.txt if you have chrome and chrome driver
- change the directory to Trajectory_task
- 
- run the main file: streamlit run streamlit_ui.py

# Manually run using: 
- streamlit run streamlit_ui.py

# New features that can be added:
1. better ui.
2. text analysis for more signals or context.
3. use of other ai models.
4. Resolve selenium chrome compatibility issue for streamlit cloud app
