import pickle

logpass_save = {"type": "admin"}
logpass_save["admin"] = "admin"
data = open('files/Database.txt', 'ab')
pickle.dump(logpass_save, data)
data.close()