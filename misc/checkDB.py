import torndb
from db import *

NewsDatabase.reconnect()

result = NewsDatabase.query("""SELECT cal.id FROM (SELECT id, COUNT(id) AS
        total FROM commTable GROUP BY id) AS cal WHERE cal.total > 800""")
print result
