import datetime
from bttbConfig import *

joinTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
editTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
instruments = ', '.join(['Trumpet', 'Trombone'])
positions = ', '.join(['Dork', 'Geek'])
insertCmd = """
UPDATE alumni SET first='%s', nee='%s', last='%s', firstYear=%d, lastYear=%d,
email='%s', emailVisible=%d, isFriend=%d,
street1='%s', street2='%s', apt='%s', city='%s',
province='%s', country='%s', postalCode='%s', phone='%s', joinTime='%s',
editTime='%s', instruments='%s', positions='%s',
approved=%d, onCommittee=%d, rank='%s', password='%s'
WHERE id = %d;
""" % (DbFormat('john'), 				\
	   DbFormat('nee'), 				\
	   DbFormat('last'), 				\
	   105, 					\
	   1976, 					\
	   DbFormat('email'), 				\
	   1, 				\
	   1, 					\
	   DbFormat('street1'), 			\
	   DbFormat('street2'), 			\
	   DbFormat('apt'), 				\
	   DbFormat('city'), 				\
	   DbFormat('province'), 			\
	   DbFormat('country'), 			\
	   DbFormat('postalCode'), 		\
	   DbFormat('phone'), \
	   joinTime, 							\
	   editTime, 							\
	   DbFormat(instruments), 				\
	   DbFormat(positions), 				\
	   1, 					\
	   1, 					\
	   DbFormat('rank'),				\
	   DbFormat(None),			\
	   14450 )

print insertCmd
