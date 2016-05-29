#-*- coding:utf-8 -*-
import sys,os
import re
from collections import Counter
import pickle

def stripSomeThing(string):

    # remove email address
    match = re.match('[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})', string)
    if match:
        string = string.replace(match.group(0),"")
        #print ('===>',match.group(0))

    # remove punctuations  
    list = ['~','!','?','#','$','%','^','&','*','(',')','[',']','{','}','+','=','-','|','\\','\'','"','/',',','.','_',':',';','>','<']
    for char in list:
        string = string.replace(char,"")
    
    # remove stop words
    stopword_file = open("stopwords.txt", "r")
    stopword_list = stopword_file.readlines()[0].split()
    #print (stopword_list)
    stopword_file.close()
    

    string = ' '.join(word for word in string.split() if word not in stopword_list)
    
    string_final = ''
    slist = string.split()
    for term in slist:
        if '@' not in term:
            if len(term) > 1:
                string_final = string_final + term + " "

    return string_final

class Topic_model:

    topic = ''
    dir_path = ''
    sorted_tf = None
    total_feq = 0.0
    count = 0
    directory = 'temp'
    
    def __init__(self,topic,dir_path):
        self.topic = topic
        self.dir_path = dir_path

    def p(self,term):
        return self.sorted_tf[term]/self.total_feq
        
    def load(self,name):
        pkl_file = open(self.directory + "/" + name + '.pkl', 'rb')
        obj = pickle.load(pkl_file)
        self.topic = obj[0]
        self.dir_path = obj[1]
        self.sorted_tf = obj[2]
        self.total_feq = obj[3]
        self.count = obj[4]
        pkl_file.close()
        print ('load '+ name + ' successfully!', 'count=' + str(self.count), 'term_num=' + str(self.total_feq))

    
    def modeling(self):
    
        self.count = 0
        all_sentence = ''
        
        # read train files
        for file in os.listdir(self.dir_path):
            print (self.dir_path,file)
            
            # read
            with open(self.dir_path+'/'+file,'r', encoding='utf-8', errors='ignore' ) as f:
                content = f.readlines()
            #print (content)
    
            # remove \n stopwords    
            content = [x.strip('\n') for x in content]
            for sentence in content:
                sentence = sentence.lower()
                sentence = stripSomeThing(sentence)
                all_sentence += sentence
                
            self.count +=1
        
        all_sentence = all_sentence.split()
        self.sorted_tf = Counter(all_sentence)
        self.total_feq = sum(self.sorted_tf.values())
        
        # save train files
        obj = [ self.topic, self.dir_path, self.sorted_tf, self.total_feq, self.count]
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        out = open(self.directory + "/" + self.topic + ".pkl", "wb")
        pickle.dump(obj, out)
        out.close()
        del obj
        #print (self.sorted_tf)
        print (len(self.sorted_tf), 'count=' + str(self.count), 'term_num=' + str(self.total_feq))


class Rel_model:

    path = ''
    sorted_tf = None
    total_feq = 0
    count = 0
    directory = 'temp'

    def __init__(self,path):
        self.path = path
    
    def p(self,term):
        return self.sorted_tf[term]/self.total_feq
    
    def modeling(self):
        all_sentence = ''
        # read test files (for smoothing)
        for file in os.listdir(self.path + '/Test'):
            print ('reading Test ',file)
            self.count +=1
            with open(self.path + '/Test/' + file,'r', encoding='utf-8', errors='ignore' ) as f:
                content = f.readlines()
                content = [x.strip('\n') for x in content]
                for sentence in content:
                    sentence = sentence.lower()
                    sentence = stripSomeThing(sentence)
                    all_sentence += sentence
                    
        for file in os.listdir(self.path + '/Unlabel'):
            print ('reading Unlabel ',file)
            self.count +=1
            with open(self.path + '/Unlabel/' + file,'r', encoding='utf-8', errors='ignore' ) as f:
                content = f.readlines()
                content = [x.strip('\n') for x in content]
                for sentence in content:
                    sentence = sentence.lower()
                    sentence = stripSomeThing(sentence)
                    all_sentence += sentence
                    
        all_sentence = all_sentence.split()
        self.sorted_tf = Counter(all_sentence)
        self.total_feq = sum(self.sorted_tf.values())
        
        # save train files
        obj = [ self.sorted_tf, self.total_feq, self.count]
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        out = open(self.directory + "/ref_model.pkl", "wb")
        pickle.dump(obj, out)
        out.close()
        del obj
        del all_sentence
        
    def load(self):
        pkl_file = open(self.directory + "/ref_model.pkl", 'rb')
        obj = pickle.load(pkl_file)
        self.sorted_tf = obj[0]
        self.total_feq = obj[1]
        self.count = obj[2]
        pkl_file.close()
        print ('load ref_model successfully!', 'count=' + str(self.count), 'term_num=' + str(self.total_feq))
        
class TestData:

    docs = {}
    input_dir = ''
    directory = 'temp'
    
    def __init__(self,input_dir):
        self.input_dir = input_dir
    
    def load(self):
        pkl_file = open(self.directory + "/test_data.pkl", 'rb')
        obj = pickle.load(pkl_file)
        self.docs = obj
        pkl_file.close()
        print ('load test_data successfully!')
        
    def read_and_convert(self):
        for file in os.listdir(self.input_dir + '/Test'):
            print ('reading ',file)
            with open(self.input_dir + '/Test/' + file,'r', encoding='utf-8', errors='ignore' ) as f:
                doc = ''
                content = f.readlines()
                content = [x.strip('\n') for x in content]
                for sentence in content:
                    sentence = sentence.lower()
                    sentence = stripSomeThing(sentence)
                    doc += sentence  
                    
                doc = doc.split()
                self.docs.update({file: doc})
                
                # save train files
                obj = self.docs
                if not os.path.exists(self.directory):
                    os.makedirs(self.directory)
                out = open(self.directory + "/test_data.pkl", "wb")
                pickle.dump(obj, out)
                out.close()
                del obj
                
        
class Process:
    
    input_dir = ''
    output_file = ''
    labeled_size = -1
    #topics = []
    model_list = []
    total_doc_count = 0
    rel_model = None
    test_data = None
    
    def my_key(self,dict_key):
        try:
            return int(dict_key)
        except ValueError:
            return dict_key
    
    def __init__(self,argv):
        self.input_dir = argv[1]
        self.output_file = argv[2]
        if len(argv) > 3:
            self.labeled_size = argv[3]
    
    def create_model(self):
        # read files, unigram and store
        
        for topic_name in os.listdir(self.input_dir+"/Train"):
            t = Topic_model(topic_name,self.input_dir+"/Train/"+topic_name)
            #self.topics.append(dir)
            t.modeling()
            del t
        
        # read test files (for smoothing)
        r = Rel_model(self.input_dir)
        r.modeling()
        del r
        
        test = TestData(self.input_dir)
        test.read_and_convert()
        del test
        #print (r.sorted_tf.most_common(30))
        
    def load_model(self):
        # read from pickle
        for topic_name in os.listdir(self.input_dir+"/Train"):
            print (topic_name)
            topicModel = Topic_model('','')
            topicModel.load(topic_name)
            #print (topicModel.p('software'))
            self.model_list.append(topicModel)
            self.total_doc_count += topicModel.count 
            
        self.rel_model = Rel_model(self.input_dir)
        self.rel_model.load()

        self.test_data = TestData(self.input_dir)
        self.test_data.load()
    
    def process(self):

        self.create_model()
        self.load_model()
        print (self.total_doc_count)
        u = 10
        ans = {}
        
        scores = []
        for key in self.test_data.docs:
            print ('calculating.. ', key)
            terms = self.test_data.docs[key]
            scores = []
            for topicModel in self.model_list:
                #print (topicModel.topic)
                #print (self.test_data.docs[key])
                score = 1
                for term in terms:
                    # score
                    score = score * (topicModel.p(term) + u * self.rel_model.p(term))
                scores.append(score)
            max_index = scores.index(max(scores))
            #print (max_index)
            #print (self.model_list[max_index].topic)
            ans.update({int(key):self.model_list[max_index].topic})

        # sort    
        #ans_sort = sorted(ans,key=self.my_key)
        
        # output to file
        out = open(self.output_file, "w")
        for key in sorted(ans.items()):
            print (key[0],key[1])
            out.write(str(key[0]) + ' ' + key[1] +'\n')
        out.close()
            #print (scores)
            #print (topicModel.sorted_tf.most_common(10))
        
        
if __name__ == "__main__":
    p = Process(sys.argv)
    #print (p.input_dir)
    #print (p.output_file)
    #print (p.labeled_size)
    p.process()
    