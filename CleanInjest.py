from DB import DB
from sys import argv
from json import dumps

db = DB(argv[1])
out = {"files": db.files, "projects": db.projects, "categories": db.categories}
print(db.categories.keys())
open(argv[2], 'w+').write(dumps(out, separators=(',',':')))
