#!/usr/bin/python

saveOutput = False

print '** Starting simulation'
#h1.cmd('wget -O 10.0.0.17:8080/video5.mp4 > /dev/null')

for i in range(1, 17):    
	if saveOutput:
		exec("h%s.cmd('wget 10.0.0.17:8080/video%s.mp4')" % (i,i))
	else:
		exec("h%s.cmd('wget -O- 10.0.0.17:8080/video%s.mp4 > /dev/null')" % (i,i))
