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

from fuzzywuzzy.fuzz import partial_ratio, ratio


class DB:
    def __init__(self, meta: dict):
        self.projects = meta["projects"]
        self.files = meta["files"]
        self.categories = meta["categories"]
        self.authors = meta["authors"]

    # Querying

    def get_project(self, pid: int):
        if str(pid) in self.projects:
            return self.projects[str(pid)]
        return False

    def get_file(self, fid: int):
        if str(fid) in self.files:
            return self.files[str(fid)]
        return False

    def get_category(self, cid: int):
        if str(cid) in self.categories:
            return self.categories[str(cid)]
        return False

    def search_projects(self, q: str, ptype: str, limit=25, threshold=80, version="*"):
        out = list()
        popular = q == ""
        for n in self.projects.values():
            if ptype != "*" and n["type"] != ptype:
                continue
            if version != "*" and version not in n["versions"]:
                continue
            if not popular:
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
            else:
                out.append((n, 0))
        out.sort(key=lambda x: x[1])
        projects = [i[0] for i in out[::-1]]
        if popular:
            projects.sort(key=lambda p: p["popularity"], reverse=True)
        return projects[:limit]

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
