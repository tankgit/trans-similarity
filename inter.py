#coding:utf-8
from sim2 import sim

if __name__=='__main__':
	mysim=sim()
	sim,sent= mysim.calc_sim('What he has lost noble Macbeth are win.','mkb.txt')
	print '%f %s\n' % (sim,sent)
    	sim,sent= mysim.calc_sim('What he has lost noble Macbeth are win.','mkb.txt')
	print '%f %s\n' % (sim,sent)
        sim,sent= mysim.calc_sim('What he has lost noble Macbeth are win.','mkb.txt')
	print '%f %s\n' % (sim,sent)
