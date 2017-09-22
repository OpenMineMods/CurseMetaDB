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
    it with curseDb (or a modified version of that program), containing parts
    covered by the terms of the EUPL, the licensors of this Program grant you
    additional permission to convey the resulting work.
"""

from fuzzywuzzy.fuzz import partial_ratio, ratio
from os import listdir, path
from json import loads
from MessCleaner import clean_project, clean_file


class DB:
    def __init__(self, meta_folder: str):
        self.projects = dict()
        self.files = dict()

        project_list = self._ls(meta_folder)
        for project in project_list:
            self._load_project(project)

        self.popular = dict()
        self._gen_popular()

    # Querying

    def get_project(self, pid: int):
        if pid in self.projects:
            return self.projects[pid]
        return False

    def get_file(self, fid: int):
        if fid in self.files:
            return self.files[fid]
        return False

    def search_projects(self, q: str, ptype: str, limit=25, threshold=80, version="*"):
        out = list()
        for n in self.projects.values():
            if ptype != "*" and n["type"] != ptype:
                continue
            if version != "*" and version not in n["versions"]:
                continue
            part_ratio = partial_ratio(q.lower(), n["title"].lower())
            full_ratio = ratio(q.lower(), n["title"].lower())

            body_ratio = partial_ratio(q.lower(), n["desc"].lower())
            full_body_ratio = ratio(q.lower(), n["desc"].lower())
            if part_ratio >= threshold:
                out.append((n, part_ratio + full_ratio))
                if len(out) >= limit:
                    break
                continue
            if body_ratio >= threshold:
                out.append((n, body_ratio + full_body_ratio))
                if len(out) >= limit:
                    break
        out.sort(key=lambda x: x[1])
        return [i[0] for i in out[::-1]][:limit]

    def search_files(self, filename: str):
        for file in self.files.values():
            if file["filename"].lower() == filename.lower():
                return file

    def get_files_for_version(self, project: int, version: str):
        project = self.get_project(project)
        if not project:
            return project
        files = project["files"]
        out = list()
        for file in files:
            if version in self.get_file(file)["versions"]:
                out.append(file)
        if len(out) > 0:
            return out
        return False

    def get_popular(self, ptype: str, limit=25, version="*"):
        if version != "*":
            return [i for i in self.popular[ptype] if version in self.get_project(i)["versions"]][:limit]
        return self.popular[ptype][:limit]

    # Init

    def _gen_popular(self):
        for ptype in ["mod", "texturepack", "world", "modpack"]:
            of_type = dict()
            for project in [i for i in self.projects if self.get_project(i)["type"] == ptype]:
                of_type[project] = self.get_project(project)
            self.popular[ptype] = sorted(of_type, key=lambda x: of_type[x]["rank"])

    def _load_project(self, project_folder: str):
        manifest = loads(open(path.join(project_folder, "index.json")).read())
        project = clean_project(manifest)
        project["versions"] = list()

        files = self._ls(path.join(project_folder, "files"))
        for file in files:
            file = clean_file(loads(open(file).read()))
            file["project"] = project["id"]
            project["versions"] += file["versions"]

            project["files"].append(file["id"])
            self.files[file["id"]] = file

        project["versions"] = list(set(project["versions"]))
        self.projects[project["id"]] = project

    # Utils

    def _ls(self, folder: str):
        return [path.join(folder, i) for i in listdir(folder)]
