- Command to create view :
  query = create view logArticles as select split_part(path, '/', 3) as path from log where path LIKE '/article/%;

- To run the program :
  python log.py
