from DB import DB
from json import loads
from sys import argv

db = DB(loads(open(argv[1]).read()))
