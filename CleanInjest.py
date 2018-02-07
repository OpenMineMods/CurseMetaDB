# CleanInject.py data/addons/ output.json

from sys import argv
from os import listdir, path
from json import loads, dumps
from MessCleaner import clean_category, clean_file, clean_project


def ls(folder: str):
    return [path.join(folder, i) for i in listdir(folder)]


folder = argv[1]
projects = dict()
categories = dict()
files = dict()

for project_folder in ls(folder):
    manifest = loads(open(path.join(project_folder, "index.json"), encoding='utf-8').read())
    project = clean_project(manifest)
    project["minecraft"] = list()
    project["categories"] = list()
    project["authors"] = list()

    pid = project["id"]

    cleaned_files = list()
    raw_files = ls(path.join(project_folder, "files"))

    for file in raw_files:
        file = clean_file(loads(open(file, encoding='utf-8').read()))
        cleaned_files.append(file)

    for file in cleaned_files:
        fid = file["id"]
        file["project"] = pid
        project["minecraft"] += file["minecraft"]
        project["files"].append(fid)
        files[fid] = file

    oldest_date = min(file["date"] for file in cleaned_files)
    newest_date = max(file["date"] for file in cleaned_files)

    project["stats"] = {
        "downloads": int(manifest["DownloadCount"]),
        "popularity": float(manifest["PopularityScore"]),
        "created": int(oldest_date),
        "latest": int(newest_date)
    }

    for category in manifest["Categories"]:
        category = clean_category(category)
        cid = category["id"]
        categories[cid] = category
        project["categories"].append(cid)

    for author in manifest["Authors"]:
        project["authors"].append({"username": author["Name"]})

    if "Attachments" in manifest:
        for attachment in manifest["Attachments"]:
            if "IsDefault" in attachment and attachment["IsDefault"]:
                project["icon"] = {"url": attachment["Url"], "hash": path.splitext(attachment["Title"])[0]}
        if "icon" not in project:
            attachment = manifest["Attachments"][0]
            project["icon"] = {"url": attachment["Url"], "hash": path.splitext(attachment["Title"])[0]}

    project["minecraft"] = list(set(project["minecraft"]))
    projects[pid] = project

out = dumps({
    "projects": projects,
    "categories": categories,
    "files": files
}, separators=(",", ":"), indent=4, sort_keys=True)

f_len = open(argv[2], 'w', encoding='utf-8').write(out)
print("Wrote {} bytes to {}".format(f_len, argv[2]))
