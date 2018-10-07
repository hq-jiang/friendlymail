import unittest
import friendlymail

#class TestMethods(unittest.TestCase):
#
#	def test_hash(self):
#		friendlymail.hash(ident)

if __name__=="__main__":
	for i in range(100):
		print(friendlymail.hash_ident(i))