- Log Analysis Project
Internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.
The database contains newspaper articles, as well as the web server log for the site.
The log has a database row for each time a reader loaded a web page.
Using that information, the program will answer questions about the site's user activity.
The program will connect to the database, use SQL queries to analyze the log data, and print out the answers to some questions.
Questions the tool answers:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

Prerequisites
1. python 2
2. vagrant


How to run:
1. Move to Log Analysis Project directory
2. python log.py
3. Check output.txt

Output example:
  1. Most popular three articles of all time:
  	- "Candidate is jerk, alleges rival" - 338647 views
  	- "Bears love berries, alleges bear" - 253801 views
  	- "Bad things gone, say good people" - 170098 views

  2. Most popular article authors of all time:
  	- Ursula La Multa - 507594 views
  	- Rudolf von Treppenwitz - 423457 views
  	- Anonymous Contributor - 170098 views
  	- Markoff Chaney - 84557 views

  3. Days on which more than 1% of requests lead to errors:
  	- 2016-07-17 - 2.25% errors
