from PySuffixTree import SuffixTree

s = SuffixTree()
#s.addString('abc')
#s.addString('abx')
#s.addString('abc$')

s.buildTree('abcdefabxybcdmnabcdex$', True	)
print s
#coffee = "TACAATAGGTGAACCATCATCCCT$"
#s.addString(coffee)
#s.addString('banana$')

