import numpy as np
import argparse

def load_file(fn):
	names = []
	f = open(fn)
	for line in f.xreadlines():
		names.append(line.strip())

	
	f.close()
	return names


def init_preferences(women,men):
	pref_women = {}
	for w in women:

		pref_women[w]={}
		order = np.random.permutation(np.arange(1,len(men)+1))
		idx= 0
		for m in men:
			pref_women[w][order[idx]] = m
			pref_women[w][m] = order[idx]
			idx+=1
	return pref_women



parser = argparse.ArgumentParser(description="""Stable marriage problem simulation""")
parser.add_argument('-f','--females', type=str, default=None, help='input file with female names')
parser.add_argument('-m','--males', type=str, default=None, help='input file with male names')
parser.add_argument('N', type=int, nargs='?', default=6, help='number of men/women')
args = parser.parse_args()

if(args.females is not None and args.males is not None):
	all_women = load_file(args.females)
	all_men = load_file(args.males)
	N = args.N

	try:
		women = np.random.choice([x for x in all_women if x not in all_men],size=N,replace=False)
		men = np.random.choice([x for x in all_men if x not in all_women],size=N,replace=False)
	except:
		print "N is bigger than the available names"
		import sys
		sys.exit(1)

else:
	N = 6
	women= ["Alice","Diana","Emma","Kate","Laura","Tina"]
	men=["Bob","Daniel","George","Kevin","Peter","Stephen"] 



pref_women = init_preferences(women,men)
pref_men= init_preferences(men,women)

couples = {}
status_men ={}
status_women={}

for m in men:
	status_men[m]=1 # propose to first choice 

it = 0


while(len(couples)<2*N):

	for m in men:
		if m not in couples:
			top_woman = pref_men[m][status_men[m]]

			if(top_woman not in couples):
				couples[top_woman]=m
				couples[m]=top_woman
				status_women[top_woman]=pref_women[top_woman][m]
				

			elif(top_woman in couples and pref_women[top_woman][m]<pref_women[top_woman][couples[top_woman]]):

						del couples[couples[top_woman]] #unpair with her previous guy
						couples[top_woman]=m
						couples[m]=top_woman
						status_women[top_woman]=pref_women[top_woman][m]

			else:
				status_men[m]+=1 
	it+=1

import pprint
pp = pprint.PrettyPrinter(depth=6)
pp.pprint(couples)
print "Converged after {} iterations.".format(it)


for person in couples.keys():
	assert(person == couples[couples[person]])

print "Preference scores (lower is better)"

print "Preference score for women:\t\t {}".format(np.sum(status_women.values()))
print "Preference score for men:\t\t {}".format(np.sum(status_men.values()))

print "Mean preference matched for women:\t {0:.2f}".format(np.mean(status_women.values()))
print "Mean preference matched for men:\t {0:.2f}".format(np.mean(status_men.values()))

print "Median preference matched for women:\t {0:.2f}".format(np.median(status_women.values()))
print "Median preference matched for men:\t {0:.2f}".format(np.median(status_men.values()))


		



