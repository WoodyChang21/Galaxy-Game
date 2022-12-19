import pymongo

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
#This specify which database you're looking into, if database doesn't exist, create one
mydb = client["Galaxy_project"]

#This creates a table called best_score
bestscore = mydb["best_score"]

# for i in range(0,5):
#     result = bestscore.insert_one({"_id":i, "Name":" ", "Score": 0})


# count_data = bestscore.count_documents({})
# print(count_data)

for id in range(0,5):
    result = bestscore.update_one({"_id":id},{"$unset":{"Name":""}})

#This should update whenever the bestscore 
#This is for class usage
def update_bestscore_class(self, score):
    data_list = []
    bestscore_list = []
    all_bestscore = bestscore.find({})

    #The bestscore_list has all the data
    for record in all_bestscore:
        data_list.append(record)
        bestscore_list.append(record["Score"])
    
    bestscore_list.append(score)
    #Only need the top 5
    bestscore_list.sort(reverse = True)
    
    for id in range(0,5):
        udpate_best = bestscore.update_one({"_id":id},{"$set":{"Score": bestscore_list[id]}})

    return max(bestscore_list)

def update_bestscore(score):
    data_list = []
    bestscore_list = []
    all_bestscore = bestscore.find({})

    #The bestscore_list has all the data
    for record in all_bestscore:
        data_list.append(record)
        bestscore_list.append(record["Score"])
    
    bestscore_list.append(score)
    #Only need the top 5
    bestscore_list.sort(reverse = True)
    
    for id in range(0,5):
        udpate_best = bestscore.update_one({"_id":id},{"$set":{"Score": bestscore_list[id]}})

    return max(bestscore_list)

def rank(self):
    bestscore_list = []
    all_bestscore = bestscore.find({})

    for record in all_bestscore:
        bestscore_list.append(record["Score"])
    
    bestscore_list.sort(reverse = True)

    return bestscore_list


