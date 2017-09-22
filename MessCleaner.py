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
    "Stage": "stage",
    "DefaultFileId": "defaultFile",
    "WebSiteURL": "site",
    "DownloadCount": "downloads",
    "PackageType": "type",
    "PrimaryCategoryId": "primaryCategory",
    "Categories": "categories",
    "Summary": "desc",
    "Name": "title",
    "IsFeatured": "featured",
    "PopularityScore": "popularity",
    "GamePopularityRank": "rank",
    "PrimaryAuthorName": "author",
    "Id": "id"
}

file_fields = {
    "FileNameOnDisk": "filename",
    "ReleaseType": "type",
    "Dependencies": "dependencies",
    "IsAvailable": "available",
    "FileDate": "date",
    "GameVersion": "versions",
    "PackageFingerprint": "fingerprint",
    "IsAlternate": "alternate",
    "FileName": "name",
    "AlternateFileId": "alternateFile",
    "DownloadURL": "url",
    "Id": "id"
}

attachment_fields = {
    "Description": "desc",
    "Url": "url",
    "ThumbnailUrl": "thumbnail",
    "IsDefault": "default",
    "Title": "name"
}

type_map = {
    "mod": "mod",
    "singleFile": "texturepack",
    "folder": "world",
    "modPack": "modpack"
}


def clean_project(project: dict):
    cleaned_project = dict()
    for orig in project_fields:
        cleaned_project[project_fields[orig]] = project[orig]

    cleaned_project["featured"] = bool(cleaned_project["featured"])
    cleaned_project["downloads"] = int(cleaned_project["downloads"])
    cleaned_project["type"] = type_map[cleaned_project["type"]]
    cleaned_project["files"] = list()

    return cleaned_project


def clean_file(file: dict):
    if type(file) == list:
        file = file[0]
    cleaned_file = dict()
    for orig in file_fields:
        cleaned_file[file_fields[orig]] = file[orig]

    cleaned_file["project"] = None
    cleaned_file["date"] = int(datetime.strptime(cleaned_file["date"], "%Y-%m-%dT%H:%M:%S").strftime("%S"))

    return cleaned_file
