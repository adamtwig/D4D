'''
Developer: Juan Carcamo
Version: 1.0
Purpose: D4D (Data for Development) Challenge
         Data mining for Orange Cell Phone records
Details: Model classes used for data processing
Credits: Adam Terwilliger, Grahm Roderick, Jon Leidig,
         , Greg Wolffe
'''
import datetime as dt

class D4Duser:
 
    def __init__(self):
        self.user_id = 0
        self.antennas_visited_by_date = {}
        self.distance_features = {}
        self.time_features = {}
        self.last_known_pos = (0.0, 0.0)
        self.last_known_date = dt.datetime.now

    def print_user(self):
        print "user_id:", self.user_id
        print "antennas visited by day:\n", self.print_nested(self.antennas_visited_by_date),
        print "distance features by day: ", self.print_nested(self.distance_features)
        print "time features by day", self.print_nested(self.time_features) 

    def print_nested(self, obj):
        if type(obj) == dict:
            for k, v in obj.items():
                if hasattr(v, '__iter__'):
                    print k
                    self.print_nested(v)
                else:
                    print '%s : %s' % (k, v)
        elif type(obj) == list:
            for v in obj:
                if hasattr(v, '__iter__'):
                    self.print_nested(v)
                else:
                    print v
        else:
            print obj

    def get_data_str(self, data_list):
        data_str = ""
        #for data in data_list:
        #    data_str += (str(data)+',')
        data_str = ','.join([str(x) for x in data_list])
        return data_str

    def get_features_str(self, feature_name='distance'):
        features_str = ""
        features_dict = {}

        if feature_name == 'distance':
            features_dict = self.distance_features
        elif feature_name == 'time':
            features_dict = self.time_features
        else:
            return None
        list_of_features = []
        for feature_key in sorted(features_dict):
            list_of_features.append(self.get_data_str(features_dict[feature_key]))
        features_str=','.join(list_of_features)
        return features_str

    def get_one_feature_str(self, feature_name='distance', feature_key=''):
        feature_str = ""
        features_dict = {}

        if feature_name == 'distance':
            features_dict = self.distance_features
        elif feature_name == 'time':
            features_dict = self.time_features
        else:
            return None
        feature_str=','.join([str(x) for x in features_dict[feature_key]])
        return feature_str

    def get_features_headers_str(self):
        features_headers_str = ''
        features_dict = {}
        features_dict = self.distance_features

        for feature_key in sorted(features_dict):
            for data in features_dict[feature_key]:
                features_headers_str += (str(feature_key)+',')

        features_headers_str = features_headers_str[:-1]
        return features_headers_str

