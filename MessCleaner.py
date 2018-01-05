"""
    CurseMetaDB is a Python interface to query Curse metadata
    Copyright (C) 2017 Joona <joonatoona@digitalfishfun.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Additional permission under GNU GPL version 3 section 7

    If you modify this Program, or any covered work, by linking or combining
    it with curseMeta (or a modified version of that program), containing parts
    covered by the terms of the EUPL, the licensors of this Program grant you
    additional permission to convey the resulting work.
"""

from datetime import datetime

project_fields = {
    "WebSiteURL": "site",
    "PackageType": "type",
    "Categories": "categories",
    "Summary": "description",
    "Name": "title",
    "IsFeatured": "featured",
    "Id": "id"
}

file_fields = {
    "Dependencies": "dependencies",
    "FileDate": "date",
    "GameVersion": "minecraft",
    "DownloadURL": "url",
    "Id": "id",
    "FileName": "displayname",
    "FileNameOnDisk": "filename"
}

attachment_fields = {
    "Description": "desc",
    "Url": "url",
    "ThumbnailUrl": "thumbnail",
    "IsDefault": "default",
    "Title": "name"
}

category_fields = {
    "URL": "url",
    "Id": "id",
    "Name": "title"
}

dependency_fields = {
    "AddOnId": "file",
    "file": "file"
}

type_map = {
    "modPack": 0,  # modpack
    "mod": 1,  # mod
    "singleFile": 2,  # texturepack
    "folder": 3,  # world
}


def clean_project(project: dict):
    del project["Stage"]
    cleaned_project = dict()
    for orig in project_fields:
        cleaned_project[project_fields[orig]] = project[orig]

    cleaned_project["featured"] = bool(cleaned_project["featured"])
    cleaned_project["type"] = type_map[cleaned_project["type"]]
    cleaned_project["files"] = list()
    return cleaned_project


def clean_dep(dep: dict):
    cleaned_dep = dict()
    cleaned_dep["optional"] = dep["Type"] == "optional"
    del dep["Type"]
    for f in dep:
        cleaned_dep[dependency_fields[f]] = dep[f]

    return cleaned_dep


def clean_file(file: dict):
    if type(file) == list:
        file = file[0]
    cleaned_file = dict()
    cleaned_deps = list()

    for dep in file["Dependencies"]:
        cleaned_deps.append(clean_dep(dep))

    for orig in file_fields:
        cleaned_file[file_fields[orig]] = file[orig]

    cleaned_file["dependencies"] = cleaned_deps

    try:
        cleaned_file["date"] = int(datetime.strptime(cleaned_file["date"], "%Y-%m-%dT%H:%M:%S").timestamp())
    except ValueError:
        cleaned_file["date"] = int(datetime.strptime(cleaned_file["date"], "%Y-%m-%dT%H:%M:%S.%f").timestamp())

    return cleaned_file


def clean_category(category: dict):
    cleaned_category = dict()
    for orig in category_fields:
        cleaned_category[category_fields[orig]] = category[orig]

    return cleaned_category


def clean_attachment(attachment: dict):
    cleaned_attachment = dict()
    for orig in attachment_fields:
        cleaned_attachment[attachment_fields[orig]] = attachment[orig]

    return cleaned_attachment
