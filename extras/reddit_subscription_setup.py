import sqlite3
from urllib.request import pathname2url

# Default subreddits
channels = {
    474221589303656487: [
        'holdmybeer',
        'holdmycosmo',
        'whatcouldgowrong',
        'unexpected',
    ]
}

# Setup the database
db = 'tmp/subscriptions.db'
try:
    dburi = 'file:{}?mode=rw'.format(pathname2url(db))
    conn = sqlite3.connect(dburi, uri=True)
except sqlite3.OperationalError:
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE subscriptions
                 (sid int , channel int, subreddit text)''')
    c.execute('''CREATE TABLE links
                 (channel int, link text)''')

    for x in channels:
        for y in channels[x]:
            c.execute("INSERT INTO subscriptions VALUES (0, ?, ?)", [x, y])

    conn.commit()
    conn.close()
