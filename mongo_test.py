import constants


def update_record(person, date_string, new_hours, mongo_client):
    tracker_collection = mongo_client["tracker_db"]["tracker"]
    my_query = {"_id": "{}_{}".format(person, date_string)}
    tracker_records = tracker_collection.find_one(my_query)
    result_hours = new_hours
    if tracker_records:
        current_hours = tracker_records["hours"]
        result_hours = new_hours + current_hours
        tracker_collection.update_one(my_query, {"$set": {"hours": result_hours}})
    else:
        tracker_collection.insert_one({"_id": "{}_{}".format(person, date_string), "hours": new_hours,
                                       "date_string": date_string, "person": person})

    return result_hours


def get_all_records_of_the_day(day_string, mongo_client):
    tracker_collection = mongo_client["tracker_db"]["tracker"]
    all_records = []
    for each_rec in tracker_collection.find({"date_string": day_string}):
        all_records.append(each_rec)
    return all_records


def convert_mongo_dict_to_graph_input(tracker_list):
    print tracker_list
    data = []
    for each_record in tracker_list:
        actual_name = next(item for item in constants.PEOPLE_LIST if item["value"] == each_record["person"])["label"]
        print "Actual name {}".format(actual_name)
        each_graph_input = {'x': [1, 2, 3], 'y': [each_record["hours"]],
                            'type': 'bar', 'name': actual_name}
        data.append(each_graph_input)
    return data


# from pymongo import MongoClient
#
# my_mongo_client = MongoClient('localhost', 27017)
#
# get_all_records_of_the_day("06/16/20", my_mongo_client)
# my_mongo_client.close()
