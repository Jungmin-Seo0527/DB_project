import sqlite3
db = sqlite3.connect("movie.db")
db.row_factory = sqlite3.Row

# table=db.execute("select * from platform where id=?", (platform_id,)).fetchall()

# table=table[0].title
table="google_movies"
title="뮬란"
movie = db.execute(
    f'select * from {table} where title=?', (title,)
).fetchall()
print(movie.title)