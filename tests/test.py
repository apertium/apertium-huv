import sys, libhfst, glob, re

if len(sys.argv) <= 1: 
	print('test.py <lang code>')
	sys.exit(-1)


lang = sys.argv[1]

testf = []

if len(sys.argv) == 3: 
	testf = [sys.argv[2]]
else:
	testf = glob.glob('*.tsv')


istr1 = libhfst.HfstInputStream('../'+lang+'.automorf.hfst')
anal = istr1.read()
#anal.remove_epsilons()

istr2 = libhfst.HfstInputStream('../'+lang+'.autogen.hfst')
gene = istr2.read()
#gene.remove_epsilons()

def clean(s):
	return re.sub('@[^@]+@','',s)

print(testf)
err_g = 0
corr_g = 0
total_g = 0
err_a = 0
corr_a = 0
total_a = 0
for f in testf: 
	print(f + ':')
	tf = open(f).read().strip().split('\n')
	print('Generation:')
	for t in tf: 
		if t.strip() == '': continue

		row = t.strip().split('\t')

		if row[0] == '>': 
			continue
		

		g_res = gene.lookup(row[1])

		if g_res == (): 
			print('\t!\t%s\t%s\t%s' % (row[1], row[2], g_res))
			err_g += 1
			total_g += 1
			continue
		

		for g_res_i in g_res:
			if clean(g_res_i[0]) == row[2]: 
				print('\t✔\t%s\t%s' % (row[1], clean(g_res_i[0])))
				corr_g += 1
			else: 	
				print('\t-\t%s\t%s\t*%s' % (row[1], row[2], clean(g_res_i[0])))
				err_g += 1
			
			total_g += 1
		
	
	print('Analysis:')
	for t in tf: 
		if t.strip() == '': continue

		row = t.strip().split('\t')

		if row[0] == '<': 
			continue
		

		a_res = anal.lookup(row[2])
		found = False
		for r in a_res: 
			if row[1] == clean(r[0]): found = True
		
		if found: 
			print('\t✔\t%s\t%s' % (row[2], row[1]))
			corr_a += 1
		else: 	
			print('\t-\t%s\t%s\t%s' % (row[2], row[1], a_res))
			err_a += 1
		
		total_a += 1
	
	print('')
	print('-'*80)


corr = corr_g + corr_a
total = total_g + total_a

print('PASS:\t%.2f%%' % ((corr/total)*100.0))
print('GEN :\t%d\t%d\t%d' % (total_g, corr_g, err_g))
print('ANAL:\t%d\t%d\t%d' % (total_a, corr_a, err_a))
