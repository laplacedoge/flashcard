-- Create word table
CREATE TABLE IF NOT EXISTS wordTable (
    wordId INTEGER
        CONSTRAINT pkWordId
            PRIMARY KEY
            AUTOINCREMENT,

    wordText TEXT
        CONSTRAINT uqwordText
            UNIQUE
        CONSTRAINT nnwordText
            NOT NULL
);

-- Create meaning table
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

-- Create sentence table
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
