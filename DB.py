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


class DB:
    def __init__(self, meta: dict):
        self.meta = meta
        self.project_map = None
        self.file_map = None

        self._gen_maps()

    def _gen_maps(self):
        self.project_map = dict()
        self.file_map = dict()
        for project in self.meta["Data"]:
            for file in project["LatestFiles"]:
                file["_Project"] = project["Id"]
                self.file_map[file["Id"]] = file

            del project["LatestFiles"]

            self.project_map[project["Id"]] = project
