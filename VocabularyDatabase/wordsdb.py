import datetime
import pymongo as pm

fh = open('C:\MKM_WORK\PYTHON\pythonProjectsAndNotes\VocabularyDatabase\Vocabulary_set.csv', 'r')
wd_list = fh.readlines()

wd_list.pop(0)

vocab_list = []

for rawstring in wd_list:
    word, definition = rawstring.split(',', 1)
    definition = definition.rstrip()
    vocab_list.append({'Word' : word, 'Definition' : definition}) 

# print(vocab_list)

client = pm.MongoClient('mongodb://localhost:27017')
db = client['vocab']

vocab_collection = db['vocab_list']
vocab_collection.drop()

vocab_dict = {'Word' : 'cryptic', 'Definition' : 'secret with hidden meaning'}
result = vocab_collection.insert_one(vocab_dict)
print(f'inserted ID: {result.inserted_id}')

dbs = client.list_database_names()
if 'vocab' in dbs:
    print('Database exists')

result = vocab_collection.insert_many(vocab_list)
# print(result.inserted_ids)

data = vocab_collection.find_one()
print(data)

for data in vocab_collection.find({}, {'_id': 0, 'Definition': 0}):    # Excluding ID and Definition to get word list.
    print(data)

data = vocab_collection.find_one({'Word': 'boisterous'})
print(data)

upd = vocab_collection.update_one({'Word': 'boisterous'}, 
{'$set': {'Definition': 'Rowdy; Noisy'}})
print(f'Modified count: {upd.modified_count}')
print(vocab_collection.find_one({'Word': 'boisterous'}))
upd = vocab_collection.update_many({}, {'$set': {'Last_updated UTC:': 
datetime.datetime.utcnow().strftime('%Y-%m-%d%H%M%SZ')}})
print('modified count:', upd.modified_count)