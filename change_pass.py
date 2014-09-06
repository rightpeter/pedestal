#!/usr/bin/evn python

from myTools import *

passwd = "12345678"
salt = uuid.uuid4().hex
hashed_passwd = hashlib.sha512(passwd + salt).hexdigest()

NewsDatabase.execute("""UPDATE usersTable SET password=%s WHERE id=100017""",
        hashed_passwd)
