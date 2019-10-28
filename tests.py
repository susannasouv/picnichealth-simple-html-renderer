import unittest
from simple_html_renderer.simple_html_render import simple_html_renderer


class TestSimpleHTMLRenderer(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(simple_html_renderer(""), "")

    def test_empty_tags(self):
        self.assertEqual(simple_html_renderer("<p></p>"), "")
        self.assertEqual(simple_html_renderer("<table></table>"), "")
        self.assertEqual(simple_html_renderer("<td></td>"), "")
        self.assertEqual(simple_html_renderer("<tr></tr>"), "")
        self.assertEqual(simple_html_renderer("<style></style>"), "")

    def test_missing_end_tags(self):
        with self.assertRaises(SyntaxError):
            simple_html_renderer("<p>")
        with self.assertRaises(SyntaxError):
            simple_html_renderer("<p></table>")

    def test_tags_with_simple_strings(self):
        self.assertEqual(simple_html_renderer("<p>Hello World!</p>"), "Hello World!")
        # self.assertEqual(simple_html_renderer("<table>Hey World!</table>"), "Hey World!")
        # self.assertEqual(simple_html_renderer("<td>Hi World!</td>"), "Hi World!")
        # self.assertEqual(simple_html_renderer("<tr>Hola World!</tr>"), "Hola World!")

    # def test_valid_table_with_one_nonempty_row(self):
    #     # valid table
    #     # one row
    #     # EXPECTED OUTPUT:
    #     # ----
    #     #| Hi |
    #     # ----
    #     self.assertEqual(simple_html_renderer("<table><tr><td>Hi</td></tr></table>"), " ----\n| Hi |\n ----")

    # def test_valid_table_with_two_nonempty_rows_longer_second_row(self):
    #     # two rows, second row is longer than first row
    #     # EXPECTED OUTPUT:
    #     # --------
    #     #| Hello  |
    #     # --------
    #     #| World! |
    #     # --------
    #     self.assertEqual(simple_html_renderer("<table><tr><td>Hello</td></tr><tr><td>World!</td></tr></table>"), " --------\n| Hello  |\n --------\n| World! |\n --------")

    # def test_valid_table_with_two_nonempty_rows_second_row_has_two_columns(self):
    #     # two rows, first row has one column, second row has two columns
    #     # EXPECTED OUTPUT:
    #     # -----------
    #     #| Hello     |
    #     # -----------
    #     #| World | ! |
    #     # -----------
    #     self.assertEqual(simple_html_renderer("<table><tr><td>Hello</td></tr><tr><td>World</td><td>!</td></tr></table>"), " -----------\n| Hello     |\n -----------\n| World | ! |\n -----------")

    # def test_valid_table_two_rows_only_first_row_is_nonempty(self):
    #     # two rows, first row has content, second row is empty
    #     # EXPECTED OUTPUT: 
    #     # -------
    #     #| Hello |
    #     # -------
    #     #|       |
    #     # -------
    #     self.assertEqual(simple_html_renderer("<table><tr><td>Hello</td></tr><tr><td></td></tr></table>"), " -------\n| Hello |\n -------\n -------")

    # def test_valid_table_two_rows_only_first_row_is_nonempty(self):
    #     # two rows, first row has content, second row is empty 
    #     # EXPECTED OUTPUT:
    #     # -------
    #     #| Hello |
    #     # -------
    #     # -------
    #     self.assertEqual(simple_html_renderer("<table><tr><td>Hello</td></tr><tr></tr></table>"), " -------\n| Hello |\n -------\n -------")

    # def test_valid_table_one_row_with_empty_column(self):
    #     # row with empty column
    #     # EXPECTED OUTPUT:
    #     # --
    #     #|  |
    #     # --
    #     self.assertEqual(simple_html_renderer("<table><tr><td></td></tr></table>"), " --\n|  |\n --")

    # def test_invalid_table_no_table_parent(self):
    #     # invalid tables
    #     # tr and td tags without a table parent
    #     self.assertEqual(simple_html_renderer("<tr><td>Hello</td></tr><tr><td>World</td></tr>"), "HelloWorld")

    # def test_invalid_table_table_tag_with_only_p_tag(self):
    #     # EXPECTED OUTPUT:
    #     # Hello
    #     #
    #     self.assertEqual(simple_html_renderer("<table><p>Hello</p></table>"),  "Hello\n")

    # def test_invalid_table_table_tag_with_only_td_tag(self):
    #     self.assertEqual(simple_html_renderer("<table><td>Hello</td></table>"),  "Hello\n")

    # def test_invalid_table_table_tag_with_only_tr_tag(self):
    #     self.assertEqual(simple_html_renderer("<table><tr>Hello</tr></table>"),  "Hello\n")

    # def test_invalid_table_table_tag_with_td_parent_of_tr_tag(self):
    #     self.assertEqual(simple_html_renderer("<table><td><tr>Hello</tr></td></table>"),  "Hello\n")

    # def test_valid_table_with_strings_before_and_after_inner_tags(self):
    #     # EXPECTED OUTPUT:
    #     # one two three four
    #     # -------
    #     #| Hello |
    #     # -------
    #     self.assertEqual(simple_html_renderer("<table> one <tr> two <td>Hello</td> three </tr> four </table>"),  " one two three four \n ------- \n| Hello |\n -------")

    def test_whitespace_preservation(self):
        # p tag with simple string preserves whitespace on the ends
        self.assertEqual(simple_html_renderer("<p>Hello World </p>"),  "Hello World ")
        # newlines should be preserved?
        self.assertEqual(simple_html_renderer("<p>Hello \n World</p>"),  "Hello \n World")

    # def test_invalid_html(self):
    #     # invalid tag is interpreted as a simple string
    #     self.assertEqual(simple_html_renderer("<p"),  "<p")
    #     self.assertEqual(simple_html_renderer("</p>"),  "</p>")
    #     self.assertEqual(simple_html_renderer("<q></q>"),  "<q></q>")

    def test_invalid_style_tag(self):
        with self.assertRaises(SyntaxError):
            # nonexistent tag type
            simple_html_renderer("<style>q{width:7;}</style>")

        with self.assertRaises(SyntaxError):
            # no { to indicate beginning of styling
            simple_html_renderer("<style>p</style>")

        with self.assertRaises(SyntaxError):
            # } delimiter indicates closing of styling
            simple_html_renderer("<style>p{</style>")

        with self.assertRaises(SyntaxError):
            # no actual content after :
            simple_html_renderer("<style>p{width:}</style>")

        with self.assertRaises(SyntaxError):
            # ; delimiter indicates the end
            simple_html_renderer("<style>p{width:10}</style>")

    def test_simple_style_tag_applied_p_tag(self):
        # EXPECTED OUTPUT:
        # Hi    
        self.assertEqual(simple_html_renderer("<style>p{width:6;}</style><p>Hi</p>"), "Hi    \n")
        # EXPECTED OUTPUT:
        # Hi
        #   
        #   
        #   
        #   
        #   
        self.assertEqual(simple_html_renderer("<style>p{height:6;}</style><p>Hi</p>"), "Hi\n  \n  \n  \n  \n  ")
        # EXPECTED OUTPUT:
        # Hi      
        self.assertEqual(simple_html_renderer("<style>p{margin-right:6;}</style><p>Hi</p>"), "Hi      \n")
        # EXPECTED OUTPUT:
        #       Hi
        self.assertEqual(simple_html_renderer("<style>p{margin-left:6;}</style><p>Hi</p>"), "      Hi\n")
        # EXPECTED OUTPUT:
        #   
        #   
        #   
        #   
        #   
        #  
        # Hi
        self.assertEqual(simple_html_renderer("<style>p{margin-top:6;}</style><p>Hi</p>"), "  \n  \n  \n  \n  \n  \nHi")
        # EXPECTED OUTPUT:
        # Hi
        #   
        #   
        #   
        #   
        #   
        #   
        self.assertEqual(simple_html_renderer("<style>p{margin-bottom:6;}</style><p>Hi</p>"), "Hi\n  \n  \n  \n  \n  \n  ")

    # def test_style_tags_for_p_tag_with_overflow_content(self):
    #     self.assertEqual("<style>p{width:4;}</style><p>Hello</p>", "H...")

    # def test_style_tags_for_tables(self):
    #     # TODO handle overflow by truncating
    #     # EXPECTED OUTPUT:
    #     # ------
    #     #| Hi   |
    #     # ------
    #     self.assertEqual(simple_html_renderer("<style>table{width:6;}</style><table><tr><td>Hi</td></tr></table>"), " ------\n| Hi    |\n ------")
    #     # EXPECTED OUTPUT:
    #     # ----
    #     #| Hi |
    #     #|    |
    #     #|    |
    #     #|    |
    #     #|    |
    #     #|    |
    #     # ----
    #     self.assertEqual(simple_html_renderer("<style>table{height:6;}</style><p>Hi</p>"), " ----\n| Hi |\n|    |\n|    |\n|    |\n|    |\n ----")
    #     # EXPECTED OUTPUT:
    #     # ----------
    #     #| Hi       |
    #     # ----------
    #     self.assertEqual(simple_html_renderer("<style>p{margin-right:6;}</style><p>Hi</p>"), " ----------\n| Hi       |\n ----------")
    #     # EXPECTED OUTPUT:
    #     # ----------
    #     #|       Hi |
    #     # ----------
    #     self.assertEqual(simple_html_renderer("<style>p{margin-left:6;}</style><p>Hi</p>"), " ----------\n|       Hi |\n ----------")
    #     # EXPECTED OUTPUT:
    #     # ----
    #     #|    |
    #     #|    |
    #     #|    |
    #     #|    |
    #     #|    |
    #     #|    |
    #     #| Hi |
    #     # ----
    #     self.assertEqual(simple_html_renderer("<style>p{margin-top:6;}</style><p>Hi</p>"), " ----\n|    |\n|    |\n|    |\n|    |\n|    |\n|    |\n| Hi |\n ----")
    #     # EXPECTED OUTPUT:
    #     # ----
    #     #| Hi |
    #     #|    |
    #     #|    |
    #     #|    |
    #     #|    |
    #     #|    |
    #     #|    |
    #     # ----
    #     self.assertEqual(simple_html_renderer("<style>p{margin-bottom:6;}</style><p>Hi</p>"), " ----\n| Hi |\n|    |\n|    |\n|    |\n|    |\n|    |\n|    |\n")

    # def test_style_tags_for_tables_with_overflow_content(self):
    #     # EXPECTED OUTPUT:
    #     # --------
    #     #| Hel... |
    #     # --------
    #     self.assertEqual(simple_html_renderer("<style>table{width:6;}</style><table><tr><td>Hello World!</td></tr></table>"), " --------\n| Hel... |\n --------")

    # def test_style_tags_for_tables_tr_tag(self):
    #     # TODO: maybe this should be optional for now?
    #     # EXPECTED OUTPUT:
    #     pass

    # def test_style_tags_for_tables_td_tag(self):
    #     # TODO: maybe this should be optional for now?
    #     # EXPECTED OUTPUT:
    #     pass

    # def test_style_tag_applies_after_element(self):
    #     # EXPECTED OUTPUT:
    #     # Hi    
    #     self.assertEqual(simple_html_renderer("<p>Hi</p><style>p{width:6;}</style>"), "Hi    ")

    # def test_style_tag_whitespace_no_effect(self):
    #     # TODO: maybe this should be optional for now?
    #     self.assertEqual(simple_html_renderer("<style>p{width:6;}</style><p>Hi</p>"), simple_html_renderer("<style>\np {\n  width: 6;\n}\n</style>"))

    def test_inner_style_tag_takes_priority(self):
        # EXPECTED OUTPUT:
        # Hi        
        self.assertEqual(simple_html_renderer("<style>p{width:6;}</style><p><style>p{width:10;}</style>Hi</p>"), "Hi        \n")
        # EXPECTED OUTPUT:
        # Hello 
        # Hi        
        self.assertEqual(simple_html_renderer("<style>p{width:6;}</style><p>Hello<style>p{width:10;margin-top:4;}</style>Hi</p>"), "Hello \n\n\n\n\nHi      ")



if __name__ == '__main__':
    unittest.main()

