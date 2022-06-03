import pickle

###########################################################
# Экспериментальная

class example_class:
    a_number = 35
    a_string = "hey"
    a_list = [1, 2, 3]
    a_dict = {"first": "a", "second": 2, "third": [1, 2, 3]}
    a_tuple = (22, 23)

my_object = example_class()

my_pickled_object = pickle.dumps(my_object)  # Pickling the object
print(f"pickled :\n{my_pickled_object}\n")

my_object.a_dict = None

my_unpickled_object = pickle.loads(my_pickled_object)  # Unpickling the object
print(f"unpickled :\n{my_unpickled_object.a_dict}\n")
