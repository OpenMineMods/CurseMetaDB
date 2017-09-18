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

import psycopg2


class CurseMetaDB:
    def __init__(self, db, user="", host="", port="", password=""):
        self._conn = psycopg2.connect(database=db, user=user, host=host, port=port, password=password)
        self._cur = self._conn.cursor()

    # General

    def exec(self, cmd: str, *args):
        self._cur.execute(cmd, args)
        try:
            return self._cur.fetchall()
        except psycopg2.ProgrammingError:
            return list()

    def load_meta(self, meta: list):
        for item in meta:
            print(type(item))
            self._cur.execute("""INSERT INTO projects (project, category, name, url)
                         VALUES (%(Id)s, %(PrimaryCategoryId)s, %(Name)s, %(WebSiteURL)s);""", item)

        self._save()

    # Internal

    def _save(self):
        self._conn.commit()

    def _create_tables(self):
        self.exec("""CREATE TABLE IF NOT EXISTS projects
                     (id serial PRIMARY KEY, project integer, category integer,
                     name varchar, url varchar);""")

        self._save()
