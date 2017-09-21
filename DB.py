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

from fuzzywuzzy.fuzz import partial_ratio


class DB:
    def __init__(self, meta: dict):
        self.meta = meta

        self._gen_maps()

    # Querying

    def get_project(self, pid: int):
        if pid in self.project_map:
            return self.project_map[pid]
        return False

    def get_file(self, fid: int):
        if fid in self.file_map:
            return self.file_map[fid]
        return False

    def search_projects(self, q: str, limit=25, threshold=80):
        out = list()
        for n in self.project_map.values():
            ratio = partial_ratio(q.lower(), n["Name"].lower())
            if ratio >= threshold:
                out.append((n, ratio))
        out.sort(key=lambda x: x[1])
        return [i[0] for i in out[::-1]][:limit]

    # Internal

    def _gen_maps(self):
        # ID -> Project mappings
        self.project_map = dict()
        self.file_map = dict()

        for project in self.meta["Data"]:
            for file in project["LatestFiles"]:
                file["_Project"] = project["Id"]
                self.file_map[file["Id"]] = file

            del project["LatestFiles"]

            self.project_map[project["Id"]] = project
