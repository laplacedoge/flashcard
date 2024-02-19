# from flashcard.database import Connection

# dbPath = "/home/alex/code/project/flashcard/database/word.db"

# conn = Connection(dbPath)

# # conn.openDatabase()

# # conn.closeDatabase()
    
# words = [
#     {
#         "text": "drink",
#         "meanings": [
#             {
#                 "text": "A liquid that can be swallowed as refreshment or nourishment.",
#                 "sentences": [
#                     "I ordered a drink with my meal at the restaurant.",
#                     "She prefers a cold drink on a hot day to cool down.",
#                     "Can you get me a drink of water? I'm quite thirsty after the run.",
#                 ]
#             },
#             {
#                 "text": "To take (a liquid) into the mouth and swallow.",
#                 "sentences": [
#                     "We stopped by the stream to drink fresh water.",
#                     "He drinks coffee every morning as part of his routine.",
#                     "They drank to celebrate their friend's success at the party.",
#                 ]
#             },
#         ],
#     },
#     {
#         "text": "quick",
#         "meanings": [
#             {
#                 "text": "Moving fast or doing something in a short time.",
#                 "sentences": [
#                     "She gave a quick glance over her shoulder to make sure she wasn't being followed.",
#                     "He finished his homework with quick efficiency, leaving more time for video games.",
#                 ]
#             },
#             {
#                 "text": "At a fast speed; rapidly.",
#                 "sentences": [
#                     "The rumors about the new product spread quickly through the office.",
#                     "She quickly ran to the store to buy the ingredients needed for dinner.",
#                 ]
#             },
#         ]
#     },
#     {
#         "text": "queen",
#         "meanings": []
#     },
#     {
#         "text": "queue",
#         "meanings": []
#     },
# ]

# conn.insertWord(words)

# result = conn.searchWord("q", fuzzy=True, max=3, sortByTime=True)
# # result = conn.searchWord("q", max=2)

# print(result)

import flashcard

dbPath = "/home/alex/code/project/flashcard/database/word.db"

app =  flashcard.createApp(dbPath)

app.run(debug=True)
