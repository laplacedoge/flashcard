import datetime
import sqlite3
import re
import os

SQL_CREATE_WORD_TABLE = """
    CREATE TABLE IF NOT EXISTS wordTable (
        wordId INTEGER
            CONSTRAINT pkWordId
                PRIMARY KEY
                AUTOINCREMENT,

        wordText TEXT
            CONSTRAINT uqWordText
                UNIQUE
            CONSTRAINT nnWordText
                NOT NULL,

        creationTime INTEGER
            CONSTRAINT nnCreationTime
                NOT NULL,

        modificationTime INTEGER
            CONSTRAINT nnModificationTime
                NOT NULL,

        accessTime INTEGER
            CONSTRAINT nnAccessTime
                NOT NULL
    );
    """

SQL_CREATE_MEANING_TABLE = """
    CREATE TABLE IF NOT EXISTS meaningTable (
        meaningId INTEGER
            CONSTRAINT pkMeaningId
                PRIMARY KEY
                AUTOINCREMENT,

        wordId INTEGER
            CONSTRAINT fkWordId
                REFERENCES wordTable (wordId),

        meaningText TEXT
            CONSTRAINT nnMeaningText
                NOT NULL,

        creationTime INTEGER
            CONSTRAINT nnCreationTime
                NOT NULL,

        modificationTime INTEGER
            CONSTRAINT nnModificationTime
                NOT NULL,

        accessTime INTEGER
            CONSTRAINT nnAccessTime
                NOT NULL,

        CONSTRAINT uqWordIdAndMeaningText
            UNIQUE (wordId, meaningText)
    );
    """

SQL_CREATE_SENTENCE_TABLE = """
    CREATE TABLE IF NOT EXISTS sentenceTable (
        sentenceId INTEGER
            CONSTRAINT pkSentenceId
                PRIMARY KEY
                AUTOINCREMENT,

        meaningId INTEGER
            CONSTRAINT fkMeaningId
                REFERENCES meaningTable (meaningId),

        sentenceText TEXT
            CONSTRAINT nnSentenceText
                NOT NULL,

        creationTime INTEGER
            CONSTRAINT nnCreationTime
                NOT NULL,

        modificationTime INTEGER
            CONSTRAINT nnModificationTime
                NOT NULL,

        accessTime INTEGER
            CONSTRAINT nnAccessTime
                NOT NULL,

        CONSTRAINT uqMeaningIdAndSentenceText
            UNIQUE (meaningId, sentenceText)
    );
    """

SQL_INSERT_WORD = """
    INSERT INTO
        wordTable (wordText,
                   creationTime, modificationTime, accessTime)
        VALUES (?, ?, ?, ?);
    """

SQL_INSERT_MEANING = """
    INSERT INTO
        meaningTable (wordId, meaningText,
                      creationTime, modificationTime, accessTime)
        VALUES (?, ?, ?, ?, ?);
    """

SQL_INSERT_SENTENCE = """
    INSERT INTO
        sentenceTable (meaningId, sentenceText,
                       creationTime, modificationTime, accessTime)
        VALUES (?, ?, ?, ?, ?);
    """

SQL_QUERY_WORD_ID = """
    SELECT wordId FROM wordTable WHERE wordText = ?;
    """

SQL_QUERY_MEANING_ID = """
    SELECT meaningId FROM meaningTable WHERE meaningText = ?;
    """

SQL_QUERY_SENTENCE_ID = """
    SELECT sentenceId FROM sentenceTable WHERE sentenceText = ?;
    """

SQL_SEARCH_WORD = """
    SELECT wordId, wordText
        FROM wordTable
        WHERE wordText = ?
        ORDER BY ?
        LIMIT ?;
    """

SQL_FUZZY_SEARCH_WORD = """
    SELECT wordId, wordText
        FROM wordTable
        WHERE wordText LIKE ?
        ORDER BY ?
        LIMIT ?;
    """

SQL_FETCH_WORD_BY_WORD_ID = """
    SELECT wordId, wordText,
           creationTime, modificationTime, accessTime
        FROM wordTable
        WHERE wordId == ?;
    """

SQL_FETCH_WORD_BY_WORD_TEXT = """
    SELECT wordId, wordText,
           creationTime, modificationTime, accessTime
        FROM wordTable
        WHERE wordText == ?;
    """

SQL_FETCH_WORDS = """
    SELECT wordId, wordText
        FROM wordTable
        ORDER BY ?
        LIMIT ?;
    """

SQL_DELETE_WORD_BY_WORD_ID = """
    DELETE FROM wordTable
        WHERE wordId == ?;
    """

SQL_COMMIT = """COMMIT;"""

PAT_SEARCH_WORD = re.compile(r"^[a-zA-Z0-9- ]+$")

class Connection(object):

    def __init__(self, dbPath: str) -> None:
        self._dbPath = dbPath
        self._dbDir = os.path.dirname(dbPath)

    def openDatabase(self):
        if not os.path.isdir(self._dbDir):
            os.makedirs(self._dbDir)

        if not os.path.isfile(self._dbPath):
            self._dbConn = sqlite3.connect(self._dbPath)
            self._dbCurs = self._dbConn.cursor()

            self._dbCurs.execute(SQL_CREATE_WORD_TABLE)
            self._dbCurs.execute(SQL_CREATE_MEANING_TABLE)
            self._dbCurs.execute(SQL_CREATE_SENTENCE_TABLE)
        else:
            self._dbConn = sqlite3.connect(self._dbPath)
            self._dbCurs = self._dbConn.cursor()

    def closeDatabase(self):
        self._dbCurs.close()
        self._dbConn.close()

    def searchWord(self, keyword: str, fuzzy: bool=False,
                   max: int=10, sortByTime: bool=False) -> list:
        if not PAT_SEARCH_WORD.match(keyword):
            return []

        self.openDatabase()

        sortStmtSnip = "accessTime ASC" if sortByTime else "wordText DESC"

        if not fuzzy:
            self._dbCurs.execute(SQL_SEARCH_WORD,
                                 (keyword, sortStmtSnip, max))
            words = self._dbCurs.fetchall()
        else:
            self._dbCurs.execute(SQL_FUZZY_SEARCH_WORD,
                                 (keyword + "%", sortStmtSnip, max))
            words = self._dbCurs.fetchall()

        self.closeDatabase()

        words = [dict(zip(["wordId", "wordText"], word)) for word in words]

        return words

    def fetchWordById(self, wordId: int) -> dict:
        response = {
            "wordId": wordId,
            "wordText": None,
            "creationTime": None,
            "modificationTime": None,
            "accessTime": None,
        }

        self.openDatabase()

        self._dbCurs.execute(SQL_FETCH_WORD_BY_WORD_ID, (wordId,))
        result = self._dbCurs.fetchone()
        if result is not None:
            response["wordText"] = result[1]
            response["creationTime"] = result[2]
            response["modificationTime"] = result[3]
            response["accessTime"] = result[4]

        self.closeDatabase()

        return response

    def deleteWordById(self, wordId: int):
        self.openDatabase()

        self._dbCurs.execute(SQL_DELETE_WORD_BY_WORD_ID, (wordId,))
        self._dbCurs.execute(SQL_COMMIT)

        self.closeDatabase()

    def fetchWords(self, max: int=10, sortByTime: bool=False) -> list:
        self.openDatabase()

        sortStmtSnip = "accessTime ASC" if sortByTime else "wordText DESC"

        self._dbCurs.execute(SQL_FETCH_WORDS, (sortStmtSnip, max))
        words = self._dbCurs.fetchall()

        self.closeDatabase()

        words = [dict(zip(["wordId", "wordText"], word)) for word in words]

        return words

    def fetchWordDetail(self, word: int | str) -> list:
        pass

    def insertWord(self, word: dict):
        timestamp = int(datetime.datetime.utcnow().timestamp())

        wordText = word["wordText"]

        if not "creationTime" in word:
            creationTime = timestamp
        else:
            creationTime = word["creationTime"]

        if not "modificationTime" in word:
            modificationTime = timestamp
        else:
            modificationTime = word["modificationTime"]

        if not "accessTime" in word:
            accessTime = timestamp
        else:
            accessTime = word["accessTime"]

        self.openDatabase()

        try:
            self._dbCurs.execute("BEGIN DEFERRED TRANSACTION;")

            self._dbCurs.execute(SQL_INSERT_WORD,
                (wordText, creationTime, modificationTime, accessTime))

            self._dbCurs.execute("END TRANSACTION;")

            wordId = self._dbCurs.lastrowid

        except sqlite3.IntegrityError as e:
            wordId = None

        self.closeDatabase()

        response = {
            "wordId": wordId,
            "wordText": wordText,
            "creationTime": creationTime,
            "modificationTime": modificationTime,
            "accessTime": accessTime,
        }

        return response

    def insertWordDetail(self, words: list):
        timestamp = int(datetime.datetime.utcnow().timestamp())

        self.openDatabase()

        try:
            self._dbCurs.execute("BEGIN DEFERRED TRANSACTION;")

            # Insert words
            for word in words:
                wordText = word["text"]
                wordMeanings = word["meanings"]

                # Insert word if necessary
                self._dbCurs.execute(SQL_QUERY_WORD_ID, (wordText,))
                result = self._dbCurs.fetchone()
                if result is not None:
                    wordId = result[0]
                else:
                    self._dbCurs.execute(SQL_INSERT_WORD,
                                         (wordText, timestamp,
                                          timestamp, timestamp))
                    wordId = self._dbCurs.lastrowid

                # Insert word meanings
                for wordMeaning in wordMeanings:
                    meaningText = wordMeaning["text"]
                    meaningSentences = wordMeaning["sentences"]

                    # Insert meaning if necessary
                    self._dbCurs.execute(SQL_QUERY_MEANING_ID, (meaningText,))
                    result = self._dbCurs.fetchone()
                    if result is not None:
                        meaningId = result[0]
                    else:
                        self._dbCurs.execute(SQL_INSERT_MEANING,
                                             (wordId, meaningText,
                                              timestamp, timestamp, timestamp))
                        meaningId = self._dbCurs.lastrowid

                    for meaningSentence in meaningSentences:

                        # Insert sentence if necessary
                        self._dbCurs.execute(SQL_QUERY_SENTENCE_ID,
                                             (meaningSentence,))
                        result = self._dbCurs.fetchone()
                        if result is None:
                            self._dbCurs.execute(SQL_INSERT_SENTENCE,
                                                 (meaningId, meaningSentence,
                                                  timestamp, timestamp, timestamp))

            self._dbCurs.execute("END TRANSACTION;")

        except sqlite3.IntegrityError as e:
            pass

        self.closeDatabase()
