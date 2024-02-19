SELECT * FROM wordTable;

SELECT * FROM meaningTable;

SELECT * FROM sentenceTable;

SELECT seq + 1 AS nextId FROM sqlite_sequence WHERE name = 'wordTable';

SELECT seq + 1 AS nextId FROM sqlite_sequence WHERE name = 'meaningTable';

SELECT seq + 1 AS nextId FROM sqlite_sequence WHERE name = 'sentenceTable';
