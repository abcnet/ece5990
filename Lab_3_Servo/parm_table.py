cw=1.3
no=1.5
ccw=1.7
dc=[]
f=[]

for i in range(4):
	l=len(f)
	pulse = no+0.05*i
	dc.append(pulse/(20+pulse)*100.0)
	f.append(1000.0/(20+pulse))
	print "Duty cycles for four speed steps counter-clockwise: ", dc[l::]
	print "Frequencies for four speed steps counter-clockwise: ", f[l::]

pulse=no
dc.append(pulse/(20+pulse)*100.0)
f.append(1000.0/(20+pulse))
print "Duty cycles for four speed steps clockwise: ", dc[-1]
print "Frequencies for four speed steps clockwise: ", f[-1]

for i in range(4):
	l=len(f)
	pulse = no-0.05*i
	dc.append(pulse/(20+pulse)*100.0)
	f.append(1000.0/(20+pulse))
	print "Duty cycles for four speed steps counter-clockwise: ", dc[l::]
	print "Frequencies for four speed steps counter-clockwise: ", f[l::]