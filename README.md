Instructions for running:

packages to install:

1. django
2. nltk
3. plotly
4. pandas


to run:

python3 manage.py makemigrations

python3 manage.py migrate

python manage.py runserver

code structure:

- sentiment_analysis holds all the helper functions to arrange data
in different ways for graphing capabilities
- models contains the actual code for performing sentiment analysis in the two dunder methods


Project purpose:

We wanted to create an online journal where you could easily look back on past
posts and track your mood. This is useful in determining if you tend ot be more happy at certain
parts of the day, certain times of the year, ect.

Our about page statement:

Post your thoughts, ideas, and goals and isolate them based on their fundamental mood. Using four basic, mutually exclusive mood types, we help you dilute your thoughts into their simplest groups. Segmenting your thoughts like this can help you relax and free your mind to focus on what's important. EmotionJournal will track the positive and negative sentiment of your posts over time and help you examine your journal entries in new ways to help you uncover your own personal insights.

