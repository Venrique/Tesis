import unittest
import tesis

class TestTesis(unittest.TestCase):

    def test_define_file_name(self):
        want = 'pagina_1.jpg'
        got = tesis.define_file_name(1) 
        self.assertEqual(got, want)
        
if __name__ == '__main__':
    unittest.main()
