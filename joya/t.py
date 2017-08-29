v = '11:1,10:1'
x = v.split(',')
s= '10:3,9:1,11:4'
t = s.split(',')

for i in x:
	talla, cantidad = i.strip().split(':')
	for place, ii in enumerate(t):
		talla_s, cantidad_s = ii.strip().split(':')
		if talla == talla_s:			
			t[place] = talla_s + ':' + str((int(cantidad_s)-int(cantidad)))

print t
print ','.join(t)