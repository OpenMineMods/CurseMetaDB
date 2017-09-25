from sys import argv
from os import listdir, path
from json import loads, dumps
from MessCleaner import clean_category, clean_file, clean_project, clean_attachment


def ls(folder: str):
    return [path.join(folder, i) for i in listdir(folder)]

folder = argv[1]

projects = dict()
files = dict()
categories = dict()
authors = dict()

for project_folder in ls(folder):
    manifest = loads(open(path.join(project_folder, "index.json")).read())
    project = clean_project(manifest)
    project["versions"] = list()
    project["categories"] = list()
    project["authors"] = list()
    project["attachments"] = list()

    raw_files = ls(path.join(project_folder, "files"))
    for file in raw_files:
        file = clean_file(loads(open(file).read()))
        file["project"] = project["id"]
        project["versions"] += file["versions"]

        project["files"].append(file["id"])
        files[file["id"]] = file

    for category in manifest["Categories"]:
        category = clean_category(category)
        categories[category["id"]] = category
        project["categories"].append(category["id"])

    for author in manifest["Authors"]:
        authors[author["Name"]] = author["Url"]
        project["authors"].append(author["Name"])

    if "Attachments" in manifest:
        for attachment in manifest["Attachments"]:
            project["attachments"].append(clean_attachment(attachment))

    project["versions"] = list(set(project["versions"]))
    projects[project["id"]] = project

out = dumps({
    "projects": projects,
    "files": files,
    "categories": categories,
    "authors": authors
}, separators=(",", ":"))

f_len = open(argv[2], 'w+').write(out)
print("Wrote {} bytes to {}".format(f_len, argv[2]))
