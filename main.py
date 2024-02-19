import sqlite3, os

class DbConn(object):
    SQL_CREATE_TABLE_WORD = """
        CREATE TABLE IF NOT EXISTS wordTable (
            wordId INTEGER
                CONSTRAINT pkWordId
                    PRIMARY KEY
                    AUTOINCREMENT,

            wordText TEXT
                CONSTRAINT uqWordText
                    UNIQUE
                CONSTRAINT nnWordText
                    NOT NULL
        );
        """

    SQL_CREATE_TABLE_MEANING = """
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

            CONSTRAINT uqWordIdAndMeaningText
                UNIQUE (wordId, meaningText)
        );
        """

    SQL_CREATE_TABLE_SENTENCE = """
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

            CONSTRAINT uqMeaningIdAndSentenceText
                UNIQUE (meaningId, sentenceText)
        );
        """

    SQL_NEXT_ID_TABLE_WORD = """
        SELECT seq FROM sqlite_sequence WHERE name = 'wordTable';
        """

    SQL_NEXT_ID_TABLE_MEANING = """
        SELECT seq FROM sqlite_sequence WHERE name = 'meaningTable';
        """

    SQL_NEXT_ID_TABLE_SENTENCE = """
        SELECT seq FROM sqlite_sequence WHERE name = 'sentenceTable';
        """

    SQL_INSERT_WORD = """
        INSERT INTO wordTable (wordText) VALUES (?);
        """

    SQL_INSERT_MEANING = """
        INSERT INTO meaningTable (wordId, meaningText) VALUES (?, ?);
        """

    SQL_INSERT_SENTENCE = """
        INSERT INTO sentenceTable (meaningId, sentenceText) VALUES (?, ?);
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

    def __init__(self, dbPath: str) -> None:
        self._dbPath = dbPath

    def createDatabase(self):
        self._dbConn = sqlite3.connect(self._dbPath)
        self._dbCurs = self._dbConn.cursor()

        self._dbCurs.execute(DbConn.SQL_CREATE_TABLE_WORD)
        self._dbCurs.execute(DbConn.SQL_CREATE_TABLE_MEANING)
        self._dbCurs.execute(DbConn.SQL_CREATE_TABLE_SENTENCE)

    def openDatabase(self):
        if not os.path.isfile(self._dbPath):
            self.createDatabase()
        else:
            self._dbConn = sqlite3.connect(self._dbPath)
            self._dbCurs = self._dbConn.cursor()

    def closeDatabase(self):
        self._dbCurs.close()
        self._dbConn.close()

    def insertSentence(self, sentence: str):

        # Insert sentence if necessary
        self._dbCurs.execute(DbConn.SQL_QUERY_SENTENCE_ID, (sentence,))
        result = self._dbCurs.fetchone()
        if result is None:
            self._dbCurs.execute(DbConn.SQL_INSERT_SENTENCE,
                                 (self._meaningId, sentence))

    def insertMeaning(self, meaning: dict):
        meaningText = meaning["text"]
        meaningSentences = meaning["sentences"]

        # Insert meaning if necessary
        self._dbCurs.execute(DbConn.SQL_QUERY_MEANING_ID, (meaningText,))
        result = self._dbCurs.fetchone()
        if result is not None:
            self._meaningId = result[0]
        else:
            self._dbCurs.execute(DbConn.SQL_INSERT_MEANING,
                                 (self._wordId, meaningText))
            self._meaningId = self._dbCurs.lastrowid

        for meaningSentence in meaningSentences:
            self.insertSentence(meaningSentence)

    def insertWord(self, word: dict):
        wordText = word["text"]
        wordMeanings = word["meanings"]

        # Insert word if necessary
        self._dbCurs.execute(DbConn.SQL_QUERY_WORD_ID, (wordText,))
        result = self._dbCurs.fetchone()
        if result is not None:
            self._wordId = result[0]
        else:
            self._dbCurs.execute(DbConn.SQL_INSERT_WORD, (wordText,))
            self._wordId = self._dbCurs.lastrowid

        # Insert word meanings
        for wordMeaning in wordMeanings:
            self.insertMeaning(wordMeaning)

    def insertWords(self, words: list):
        for record in words:
            self.insertWord(record)

    def insert(self, records: list):
        """ Insert word, meaning, and sentence

        Here is the example:

        example = [
            {
                "text": "drink",
                "meanings": [
                    {
                        "text": "A liquid that can be swallowed as refreshment or nourishment.",
                        "sentences": [
                            "I ordered a drink with my meal at the restaurant.",
                            "She prefers a cold drink on a hot day to cool down.",
                            "Can you get me a drink of water? I'm quite thirsty after the run.",
                        ]
                    },
                    {
                        "text": "To take (a liquid) into the mouth and swallow.",
                        "sentences": [
                            "We stopped by the stream to drink fresh water.",
                            "He drinks coffee every morning as part of his routine.",
                            "They drank to celebrate their friend's success at the party.",
                        ]
                    },
                ],
            },
            {
                "text": "quick",
                "meanings": [
                    {
                        "text": "Moving fast or doing something in a short time.",
                        "sentences": [
                            "She gave a quick glance over her shoulder to make sure she wasn't being followed.",
                            "He finished his homework with quick efficiency, leaving more time for video games.",
                        ]
                    },
                    {
                        "text": "At a fast speed; rapidly.",
                        "sentences": [
                            "The rumors about the new product spread quickly through the office.",
                            "She quickly ran to the store to buy the ingredients needed for dinner.",
                        ]
                    },
                ]
            }
        ]
        
        """

        self.openDatabase()

        self._dbCurs.execute("BEGIN DEFERRED TRANSACTION;")

        self.insertWords(records)

        self._dbCurs.execute("END TRANSACTION;")

        self.closeDatabase()

if __name__ == "__main__":
    dbPath = "/home/alex/code/project/flashcard/database/record.db"

    conn = DbConn(dbPath)

    # conn.create_database()
    
    words = [
        {
            "text": "drink",
            "meanings": [
                {
                    "text": "A liquid that can be swallowed as refreshment or nourishment.",
                    "sentences": [
                        "I ordered a drink with my meal at the restaurant.",
                        "She prefers a cold drink on a hot day to cool down.",
                        "Can you get me a drink of water? I'm quite thirsty after the run.",
                    ]
                },
                {
                    "text": "To take (a liquid) into the mouth and swallow.",
                    "sentences": [
                        "We stopped by the stream to drink fresh water.",
                        "He drinks coffee every morning as part of his routine.",
                        "They drank to celebrate their friend's success at the party.",
                    ]
                },
            ],
        },
        {
            "text": "quick",
            "meanings": [
                {
                    "text": "Moving fast or doing something in a short time.",
                    "sentences": [
                        "She gave a quick glance over her shoulder to make sure she wasn't being followed.",
                        "He finished his homework with quick efficiency, leaving more time for video games.",
                    ]
                },
                {
                    "text": "At a fast speed; rapidly.",
                    "sentences": [
                        "The rumors about the new product spread quickly through the office.",
                        "She quickly ran to the store to buy the ingredients needed for dinner.",
                    ]
                },
            ]
        }
    ]

    conn.insert(words)
