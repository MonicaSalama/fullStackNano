#!/usr/bin/env python2
import psycopg2

DBNAME = 'news'

"""Internal reporting tool to perform 3 functionalities.
- Get most popular three articles of all time.
- Get most popular get most popular authors.
- Report days where more than 1% of the requests had errors.
"""


def get_connection():
    """Creates database connection.
    """

    db = psycopg2.connect(dbname=DBNAME, host="localhost",
                          user="vagrant", password="vagrant")
    # db = psycopg2.connect(dbname=DBNAME)
    return db


def close_connection(db):
    """Closes database connection.
    """

    db.close()


def get_most_three_popular_articles(cursor, out_file):
    """Reports most popular three articles.
    """

    query = """select articles.title, count(*)
               from (select * from logArticles) as articlePath join articles
               on articlePath.path = articles.slug
               group by articles.title
               order by count(*) DESC limit 3"""

    cursor.execute(query)
    results = cursor.fetchall()
    out_file.write('1. Most popular three articles of all time:\n')
    for tup in results:
        out_file.write('\t- \"%s\" - %s views\n' % (tup[0], str(tup[1])))
    out_file.write('\n')


def get_most_popular_authors(cursor, out_file):
    """Reports most popular authors.
    """
    subquery1 = """select authors.name, articles.slug
                   from authors join articles
                   on authors.id = articles.author"""

    subquery2 = """select * from logArticles"""
    query = """select a.name, count(*)
               from ({}) as a join ({}) as b on a.slug = b.path
               group by a.name
               order by count(*) DESC;""".format(subquery1, subquery2)

    cursor.execute(query)
    results = cursor.fetchall()
    out_file.write('2. Most popular article authors of all time:\n')
    for tup in results:
        out_file.write('\t- %s - %s views\n' % (tup[0], str(tup[1])))
    out_file.write('\n')


def get_days_with_more_than_1_percentage_errors(cursor, out_file):
    """Report days where more than 1% of the requests had errors
    """

    q1 = """select DATE(time), count(*) as cerror
            from log
            where status LIKE '404%'
            group by DATE(time)"""

    q2 = """select DATE(time), count(*) as ctotal
            from log
            group by DATE(time)"""

    query = """select error.date, (error.cerror*100.0/total.ctotal)
               from ({}) as error join ({}) as total
               on error.date = total.date
               where (error.cerror*100.0/total.ctotal) > 1;""".format(q1, q2)

    cursor.execute(query)
    results = cursor.fetchall()
    out_file.write('3. Days on which more than 1% of requests lead to errors:\n')
    for tup in results:
        out_file.write('\t- %s - %.2f%% errors\n' % (tup[0], tup[1]))


if __name__ == '__main__':
    db = get_connection()
    c = db.cursor()
    # Used query to extrat article slug from the path ex:/article/x -> x
    create_view = """REPLACE view logArticles as
                     select split_part(path, '/', 3) as path
                     from log where path LIKE '/article/%';"""

    out_file = open('output.txt', 'w')
    get_most_three_popular_articles(c, out_file)
    get_most_popular_authors(c, out_file)
    get_days_with_more_than_1_percentage_errors(c, out_file)
    out_file.close()
    close_connection(db)
