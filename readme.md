# News Generator

## Requirements
* Python
* Django
* React
* Sklearn
* MySQL

## How to run frontend
1. Install react using ``https://www.liquidweb.com/kb/install-react-js-windows/``
2. Open terminal in the directory react-project
3. Install the dependencies using ``npm install``
4. To run the application use ``npm start``
5. The application will be displayed in a browser at url ``http://127.0.0.1:5000``

## How to run Backend
1. Install python
2. Open the terminal in directory news_generator
3. Install project requirements using ``pip install -r requirements.txt``
4. Once the requirements are installed open mysql and create a database with name 'news'
5. Change the MySQL details in news_generator/news_generator/settings.py
6. In terminal type python manage.py makemigrations backend && python manage.py migrate to create tables in db
7. In the new terminal start python, import nltk, nltk.download('punkt'), nltk.download('stopwords')
8. Once the tables are created successfully run ``python manage.py runserver``

## Changes apart from installations
* If you face any issues in fetching (scraping) news then use the API keys and change them in news_generator/backend/news_scraper.py
* Classification models are kept in news_generator/static/finalized_model.pkl and news_generator/static/vectorized.pickle




## API keys
* main:0e5c7cf34cdf4eb293d75e319dd38ca5
* fc96bec3a64941b581d2ecd95c74f7df
* 320a4cd777b14c6a81d6084dd32e1822
* 2a7a62c8b8f64547a8ce28b459bca05c
