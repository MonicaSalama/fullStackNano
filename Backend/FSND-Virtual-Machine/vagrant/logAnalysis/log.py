import psycopg2

DBNAME = 'news'


def get_connection():
    db = psycopg2.connect(dbname=DBNAME, host="localhost",
                          user="vagrant", password="vagrant")
    return db


def close_connection(db):
    db.close()


def get_most_three_popular_articles(cursor):
    query = """select path, count(*)
               from (select * from logArticles) as articleNames
               group by path
               order by count(*) DESC limit 3;"""

    cursor.execute(query)
    results = cursor.fetchall()
    print('Most popular three articles of all time:')
    for tup in results:
        print('\t- \"%s\" - %s views' % (tup[0], str(tup[1])))
    print('\n')


def get_most_popular_authors(cursor):
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
    print('Most popular article authors of all time:')
    for tup in results:
        print('\t- %s - %s views' % (tup[0], str(tup[1])))
    print('\n')


def get_days_with_more_than_1_percentage_errors(cursor):
    q1 = """select DATE(time), count(*) as cerror
            from log
            where status LIKE '404%'
            group by DATE(time)"""

    q2 = """select DATE(time), count(*) as ctotal
            from log
            group by DATE(time);"""

    query = """select error.date, (error.cerror*100.0/total.ctotal)
               from ({}) as error join ({}) as total
               on error.date = total.date
               where (error.cerror*100.0/total.ctotal) > 1;""".format(q1, q2)

    cursor.execute(query)
    results = cursor.fetchall()
    print('Days on which more than 1% of requests lead to errors:')
    for tup in results:
        print('\t- %s - %.2f%% errors' % (tup[0], tup[1]))


if __name__ == '__main__':
    db = get_connection()
    c = db.cursor()
    get_most_three_popular_articles(c)
    get_most_popular_authors(c)
    get_days_with_more_than_1_percentage_errors(c)
    close_connection(db)
