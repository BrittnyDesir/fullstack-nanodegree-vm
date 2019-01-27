#!/usr/bin/env python

import psycopg2

DBNAME = "news"

question_1 = "What are the most popular articles of all time?"
question_2 = "Who are the most popular authors of all time?"
question_3 = "On which day did more than 1% of requests lead to an error?"


query_1 = """
          SELECT title, count(*) AS views
          FROM articles JOIN log ON log.path
          LIKE CONCAT('/article/%', articles.slug)
          GROUP BY articles.title
          ORDER BY views DESC
          LIMIT 3;
          """

query_2 = """
          SELECT name, count(*) AS viewsPerAuthor
          FROM authors JOIN articles
          ON authors.id = articles.author
          JOIN log ON path
          LIKE CONCAT('/article/%', articles.slug)
          GROUP BY name
          ORDER BY viewsPerAuthor DESC
          LIMIT 3;
          """

query_3 = """
          SELECT * FROM errors
          JOIN requests
          ON errors.day = requests.perday
          WHERE cast(totalerrors as float)/cast(totalrequests as float) > .01;
          """


def get_articles(query):
    """Find most popular articles."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def get_authors(query):
    """Find most popular authors."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def get_days(query):
    """Find day where errors more than 1 percent."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


result1 = get_articles(query_1)
result2 = get_authors(query_2)
result3 = get_days(query_3)


# Print answers
print(question_1)
for row in result1:
    title = row[0]
    views = ' --- ' + str(row[1]) + " views"
    print(title + views)

print("\n")

print(question_2)
for row in result2:
    author = row[0]
    views = ' --- ' + str(row[1]) + " views"
    print(author + views)

print("\n")

print(question_3)
for row in result3:
    totalerrors = row[0]
    totalrequests = row[3]
    num1 = float(totalerrors)
    num2 = float(totalrequests)
    percent = '{0:.2f}'.format((num1 / num2 * 100))
    day = row[2].strftime('%B %d, %Y')
    print(str(day) + ' --- ' + str(percent) + '%')
