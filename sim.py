#coding:utf-8
############################# Documents #################################
#									#
# -Interface：								#
#    cal_sim(sentence,dictionary)					#
#									#
# 	- 'sentence' is the input of an English sentence.		#
# 	- 'dictionary' is the path of sentences dictionary		#
# 	The dictionary is asked to be formated as 1-line-1-sentence.	#
#									#
#	- Return two parameters [similarity, best_sentence]		#
#	- 'similarity':	float						#
#	- 'best_sentence':  string					#	
#									#
#########################################################################


import sys
#import jieba
import operator
import math


doc_dict = []
doc_vectors = []
dfs = {}
class sim:
	def calc_df(self,documents):		#统计每个词出现的次数
	    for d in documents:
	        for w in set(d):
	            if w not in dfs:
	                dfs[w] = 1
	            else:
	                dfs[w] += 1
	
	def method_cosine(self,question):
	    pass
	
	def method_bm25(self,question):
	    def idf(word):
	        df = (word in dfs) and dfs[word] or 0.0
	        return math.log((len(doc_dict) - df + 0.5) / (df + 0.5))	#bm25算法里面，判断一个词与整个句子库的相关性的权重，即IDF
	
	    def bm25(quest, doc, K1=2.0, b=0.75):	#这里两个参数都可以更改，会影响结果。但b一般是0.75
	        tf = {}
	        for w in quest:
	            tf[w] = 0.0
	        for w in doc:
	            if w in tf:
	                tf[w] += 1.0		#统计输入的句子的每个词在已有词库中是否存在，出现多少次。
	        bm25 = 0.0
	        for k in tf.keys():
	            bm25 += idf(k) * (tf[k] * (K1 + 1)) / (tf[k] + K1 * (1 - b + b * len(doc) / avgdl))		#bm25算法核心（一般的推导公式），得到的是每个词相关性得分，然后加在一起得到句子的相关性
	        return bm25
	
	    totdl = 0.0
	    for d in doc_vectors:
	        totdl += len(d)
	    avgdl = totdl / len(doc_vectors)		#avgdl=所有词的数量/所有句子的数量
	    scores = {}
	    #quest_vector = [x for x in jieba.cut(question)]	#对句子分词，其实这步没必要用jieba库
	    quest_vector = [x for x in question.split(' ')]	#于是我直接用空格进行分词，与用库分词的效果基本一样，但有一些区别。
	    for idx, doc in enumerate(doc_vectors):
	        scores[idx] = bm25(quest_vector, doc)		#得到每个句子的相关性
	    candidates = sorted(scores.iteritems(), key=operator.itemgetter(1))[-5:]	#这里列出了排名前五的句子及其相关度，我在调用处只选取了排名第一的作为结果。
	    return candidates[::-1]
	
	def method_tfidf(self,question):	#这个是另外一种方法：TF-IDF，可以在find_similar_questions中修改选择使用哪一种方法进行计算。
	    def tfidf(quest, doc):
	        tf = {}
	        for w in quest:
	            tf[w] = 0.0
	        for w in doc:
	            if w in tf:
	                tf[w] += 1.0
	        tfidf = 0.0
	        for k in tf.keys():
	            df = (k in dfs) and dfs[k] or 0.0
	            tfidf += (tf[k] / len(doc)) * math.log(len(doc_dict) / (1 + df))
	        return tfidf
	    quest_vector = [x for x in jieba.cut(question)]
	    tfidfs = {}
	    for idx, doc in enumerate(doc_vectors):
	        tfidfs[idx] = tfidf(quest_vector, doc)
	    candidates = sorted(tfidfs.iteritems(), key=operator.itemgetter(1))[-5:]
	    return candidates[::-1]
	
	def find_similar_questions(self,question):	#这里可以选择两种计算相似度的算法，这里用的bm25
	    return self.method_bm25(question) 	
	
	def load_doc_dict(self,filename):
	    f = open(filename)
	    l = f.readline()
	    while l:
	        doc_dict.append(l)
	        l = f.readline()
	    f.close()
	
	def calc_sim(self,sentence,dictionary):		#接口主要调用的这个函数
	    try:
        	self.load_doc_dict(dictionary)
    	    except IOError:
        	print 'Open dictionary file failed.'
        	sys.exit(-1)
	
	    for q in doc_dict:
	        #doc_vectors.append([ x for x in jieba.cut(q)])
		doc_vectors.append([ x for x in q.split(' ')])
	    self.calc_df(doc_vectors)		#统计所有词的出现次数，记录在dfs[]里。
	    candidates = self.find_similar_questions(sentence)		#得到结果
	    return [candidates[0][1],doc_dict[candidates[0][0]]]	#输出结果
