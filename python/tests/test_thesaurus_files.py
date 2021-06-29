import unittest
from typing import List

from python.SumUp.ThesaurusFiles import ThesaurusFiles
from python.SumUp.ThesaurusFilesBuilder import ThesaurusFilesBuilder


class MyTestCase(unittest.TestCase):
    def test_builder(self):
        thesaurus_files: List[ThesaurusFiles] = ThesaurusFilesBuilder.thesauri_files()
        self.assertEqual(len(thesaurus_files), 13)
        one_thesaurus_file = thesaurus_files[0]
        self.assertEqual(one_thesaurus_file.thesaurus_version, "2009")
        self.assertEqual(one_thesaurus_file.thesaurus_file, "Thesaurus_26062009.json")
        self.assertEqual(one_thesaurus_file.substance_file, "Index_substances_26062009.json")


if __name__ == '__main__':
    unittest.main()
