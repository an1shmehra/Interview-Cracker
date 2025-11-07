# scraper/pipelines.py
import sqlite3
import os
import datetime
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "questions.db")
SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fingerprint TEXT UNIQUE,
  title TEXT,
  body TEXT,
  body_snippet TEXT,
  editorial TEXT,
  difficulty TEXT,
  source TEXT,
  source_url TEXT,
  date_scraped TEXT
);
CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE);
CREATE TABLE IF NOT EXISTS question_tags (question_id INTEGER, tag_id INTEGER, PRIMARY KEY(question_id, tag_id));
CREATE TABLE IF NOT EXISTS examples (id INTEGER PRIMARY KEY AUTOINCREMENT, question_id INTEGER, example_text TEXT);
"""

class SQLitePipeline:
    def open_spider(self, spider):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()
        self.cur.executescript(SCHEMA)
        self.conn.commit()
        # also prepare a JSON file export
        export_dir = os.path.join(os.path.dirname(__file__), "..", "data", "exports")
        os.makedirs(export_dir, exist_ok=True)
        self.json_path = os.path.join(export_dir, f"gfg_export_{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json")
        self._export_f = open(self.json_path, "w", encoding="utf8")
        self._export_f.write("[\n")
        self._first = True

    def close_spider(self, spider):
        self._export_f.write("\n]\n")
        self._export_f.close()
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        # dedupe by fingerprint
        self.cur.execute("SELECT id FROM questions WHERE fingerprint=?", (item["fingerprint"],))
        row = self.cur.fetchone()
        if row:
            return item  # already stored

        body_snip = (item.get("body_text") or "")[:400]
        self.cur.execute(
            "INSERT INTO questions (fingerprint, title, body, body_snippet, editorial, difficulty, source, source_url, date_scraped) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (item.get("fingerprint"), item.get("title"), item.get("body_html"), body_snip, item.get("editorial_html"), item.get("difficulty"), item.get("source"), item.get("source_url"), item.get("date_scraped"))
        )
        qid = self.cur.lastrowid

        # tags
        for t in item.get("tags", []):
            if not t:
                continue
            self.cur.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (t,))
            self.cur.execute("SELECT id FROM tags WHERE name=?", (t,))
            tag_id = self.cur.fetchone()[0]
            try:
                self.cur.execute("INSERT OR IGNORE INTO question_tags (question_id, tag_id) VALUES (?, ?)", (qid, tag_id))
            except:
                pass

        # examples
        for ex in item.get("examples", []):
            self.cur.execute("INSERT INTO examples (question_id, example_text) VALUES (?, ?)", (qid, ex))

        self.conn.commit()

        # write to export JSON
        obj = dict(item)
        # convert lists to simple serializable items
        if "code_snippets" in obj:
            obj["code_snippets"] = obj["code_snippets"][:3]
        if not self._first:
            self._export_f.write(",\n")
        else:
            self._first = False
        json.dump(obj, self._export_f, ensure_ascii=False, indent=None)
        return item
