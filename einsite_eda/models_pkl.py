import pickle

dir_name = '/models/'

def save_model(filename, model):
    pickle.dump(model, open(dir_name+filename, 'wb'))
    return "model saved as {}".format(dir_name+filename)
    
    
    
def load_model(filename):
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model