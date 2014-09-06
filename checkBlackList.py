import torndb
from db import *

NewsDatabase.reconnect()

result = NewsDatabase.query("""SELECT * FROM blackList""")
print result
