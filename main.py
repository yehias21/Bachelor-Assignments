import pickle
if __name__ == '__main__':
    configDic={}
    try:
        with open('cache/clientdict.config', 'rb') as config_dictionary_file:
            configDic = pickle.load(config_dictionary_file)
    except:
        pass
    print(configDic)
