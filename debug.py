from DB import DB
from sys import argv
from json import loads

db = DB(loads(open(argv[1]).read()))
