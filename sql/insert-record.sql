-- Insert record

BEGIN DEFERRED TRANSACTION;

INSERT
    INTO wordTable (wordText)
    VALUES ('drink');

INSERT
    INTO meaningTable (wordId, meaningText)
    VALUES (1, 'A liquid that can be swallowed as refreshment or nourishment.');

INSERT
    INTO sentenceTable (meaningId, sentenceText)
    VALUES (1, 'I ordered a drink with my meal at the restaurant.');

INSERT
    INTO sentenceTable (meaningId, sentenceText)
    VALUES (1, 'She prefers a cold drink on a hot day to cool down.');

INSERT
    INTO sentenceTable (meaningId, sentenceText)
    VALUES (1, 'Can you get me a drink of water? I''m quite thirsty after the run.');

INSERT
    INTO meaningTable (wordId, meaningText)
    VALUES (1, 'To take (a liquid) into the mouth and swallow.');

INSERT
    INTO sentenceTable (meaningId, sentenceText)
    VALUES (2, 'We stopped by the stream to drink fresh water.');

INSERT
    INTO sentenceTable (meaningId, sentenceText)
    VALUES (2, 'He drinks coffee every morning as part of his routine.');

INSERT
    INTO sentenceTable (meaningId, sentenceText)
    VALUES (2, 'They drank to celebrate their friend''s success at the party.');

INSERT
    INTO wordTable (wordText)
    VALUES ('quick');

INSERT
    INTO meaningTable (wordId, meaningText)
    VALUES (2, 'Moving fast or doing something in a short time.');

INSERT
    INTO sentenceTable (meaningId, sentenceText)
    VALUES (3, 'She gave a quick glance over her shoulder to make sure she wasn''t being followed.');

INSERT
    INTO sentenceTable (meaningId, sentenceText)
    VALUES (3, 'He finished his homework with quick efficiency, leaving more time for video games.');

INSERT
    INTO meaningTable (wordId, meaningText)
    VALUES (2, 'At a fast speed; rapidly.');

INSERT
    INTO sentenceTable (meaningId, sentenceText)
    VALUES (4, 'The rumors about the new product spread quickly through the office.');

INSERT
    INTO sentenceTable (meaningId, sentenceText)
    VALUES (4, 'She quickly ran to the store to buy the ingredients needed for dinner.');

END TRANSACTION;
