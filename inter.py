#coding:utf-8
from similarity import sim

if __name__=='__main__':
	mysim=sim();
	sim,sent= mysim.calc_sim('What he has lost noble Macbeth are win.','dict.txt')
	print '%f %s' % (sim,sent)
