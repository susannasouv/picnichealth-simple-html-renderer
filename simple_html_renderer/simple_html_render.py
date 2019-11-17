import sys
from html.parser import HTMLParser


supported_styleable_elements = ("p")
supported_styling_attributes = (
    "height", "width", "margin-bottom", "margin-left", "margin-right", "margin-top", "color")
color_to_number_encoding = {"black": 30, "red": 31, "green": 32,
                            "yellow": 33, "blue": 34, "purple": 35, "cyan": 36, "white": 37}


class SimpleHTMLParser(HTMLParser):
    supported_tags = ('p', 'table')
    supported_table_tags = ('tr', 'td')

    def __init__(self, styles={}):
        super().__init__()
        self.rows = []  # each item is an array of columns
        self.temp_curr_row = []  # array of columns
        self.tags_so_far = []
        self.content = []
        self.styles = styles
        self.tag_to_special_styles = {}

    def handle_starttag(self, tag, attrs):
        self.tags_so_far.append(tag)
        for attr in attrs:
            if attr[0] == 'style':
                if tag not in self.tag_to_special_styles:
                    self.tag_to_special_styles[tag] = {}
                if tag in self.styles:
                    self.tag_to_special_styles[tag].update(self.styles[tag])
                self.tag_to_special_styles[tag].update(
                    parse_styles_content(attr[1]))

    def handle_endtag(self, tag):
        curr_tag = self.tags_so_far.pop()
        if tag != curr_tag:
            raise SyntaxError('Tag {0} incorrectly closed'.format(curr_tag))
        elif tag == 'tr':
            self.rows.append(self.temp_curr_row)
            self.temp_curr_row = []
        elif tag == 'table':
            self.content.append(parse_table_tag_content(self.rows))
            self.rows = []
        if curr_tag in self.tag_to_special_styles:
            del self.tag_to_special_styles[curr_tag]

    def handle_data(self, data):
        if len(self.tags_so_far) <= 0:
            return
        most_recent_tag = self.tags_so_far[-1]
        if most_recent_tag == 'style':
            self.styles.update(parse_style_tag_content(data))
        elif most_recent_tag == 'td':
            self.temp_curr_row.append(data)
        elif most_recent_tag == 'p':
            self.content.append(parse_p_tag_content(
                data, self.tag_to_special_styles if most_recent_tag in self.tag_to_special_styles else self.styles))

    def feed(self, data):
        super().feed(data)
        return self.content


def find_opening_closing_pairs_of_tags(simple_html, opening_tag, closing_tag):
    opening_to_closing_tag_indices = []
    opening_tag_index = simple_html.find(opening_tag)
    while opening_tag_index != -1:
        closing_tag_index = simple_html.find(
            closing_tag, opening_tag_index + len(opening_tag))
        if closing_tag_index == -1:
            raise SyntaxError(
                "{0} tag not properly closed".format(opening_tag))
        opening_to_closing_tag_indices.append(
            (opening_tag_index, closing_tag_index))
        opening_tag_index = simple_html.find(
            opening_tag, closing_tag_index + len(closing_tag))
    return opening_to_closing_tag_indices


def simple_html_renderer(simple_html):
    """
    supported tags:
    p
    style
        width
        height
        margin
        padding
    table
        td
        tr (row span not supported)
    support tag specific styles
    """
    styles = {}
    simple_html_parser = SimpleHTMLParser(styles)
    ordered_content = simple_html_parser.feed(simple_html)
    output = "\n".join(ordered_content)
    return output


def parse_table_tag_content(parsed_table, styles={}):
    rendered_table = ""
    row_to_col_lens = [[len(col) + 2 for col in row] for row in parsed_table]
    longest_row = max([sum(row) + (len(row) - 1) for row in row_to_col_lens])

    for row in parsed_table:
        # prepend row with the correct number of dashes
        rendered_table += " "
        rendered_table += ("-" * longest_row)
        rendered_table += "\n"
        num_chars_row_data = sum([len(col) + 2 for col in row])
        num_delimiters = (len(row) - 1) if len(row) > 0 else 2
        # sum of the col lens + ((num of cols - 1) * 3)
        padding_for_last_row = longest_row - \
            (num_chars_row_data + num_delimiters)
        # append first pipe
        rendered_table += "| "
        rendered_table += " | ".join(row)
        rendered_table += (" " * padding_for_last_row)
        # append last pipe
        rendered_table += " |\n"
    # append closing row line
    rendered_table += " "
    rendered_table += ("-" * longest_row)
    rendered_table += "\n"

    return rendered_table


def parse_p_tag_content(p_tag_content, styles={}):
    min_height = p_tag_content.count("\n") + 1
    min_width = max([len(line) for line in p_tag_content.split("\n")])
    if "p" in styles:
        p_stylings = styles["p"]
        if "height" in p_stylings:
            intended_height = p_stylings["height"]
            p_tag_content += "\n{0}".format(" " * min_width) * \
                (intended_height - min_height)
        if "margin-bottom" in p_stylings:
            p_tag_content += ("\n{0}".format(" " * min_width)
                              * p_stylings["margin-bottom"])
        if "margin-top" in p_stylings:
            p_tag_content = ("{0}\n".format(" " * min_width)
                             * p_stylings["margin-top"]) + p_tag_content
        if "width" in p_stylings:
            intended_width = p_stylings["width"]
            tmp_p_tag_content = ""
            for line in p_tag_content.split("\n"):
                tmp_p_tag_content += line + \
                    ((intended_width - len(line)) * " ") + "\n"
            p_tag_content = tmp_p_tag_content
        if "margin-left" in p_stylings:
            tmp_p_tag_content = ""
            for line in p_tag_content.split("\n"):
                tmp_p_tag_content += (" " *
                                      p_stylings["margin-left"]) + line + "\n"
            p_tag_content = tmp_p_tag_content
        if "margin-right" in p_stylings:
            tmp_p_tag_content = ""
            for line in p_tag_content.split("\n"):
                tmp_p_tag_content += line + \
                    (" " * (min_width - len(line) +
                            p_stylings["margin-right"])) + "\n"
            p_tag_content = tmp_p_tag_content
        if "color" in p_stylings:
            color = color_to_number_encoding[p_stylings["color"]]
            # change color and then switch back to black
            p_tag_content = "\033[1;{0}m{1}\033[1;30m".format(
                color, p_tag_content)
    return p_tag_content


def parse_style_tag_content(style_tag_content):
    # removes all whitespace
    style_tag_content = "".join(style_tag_content.split())
    styles = {}
    starting_index = 0
    while starting_index < len(style_tag_content):
        opening_curly_index = style_tag_content.find("{", starting_index)
        if opening_curly_index == -1:
            raise SyntaxError("Style properties improperly defined")

        element_to_be_styled = style_tag_content[starting_index:opening_curly_index]
        if element_to_be_styled not in supported_styleable_elements:
            raise SyntaxError(
                "{0} element styling not supported".format(element_to_be_styled))

        closing_curly_index = style_tag_content.find("}", opening_curly_index)
        if closing_curly_index == -1:
            raise SyntaxError("Style properties improperly closed")

        if element_to_be_styled not in styles:
            styles[element_to_be_styled] = {}
        unparsed_styling = style_tag_content[opening_curly_index +
                                             1:closing_curly_index]
        styles[element_to_be_styled].update(
            parse_styles_content(unparsed_styling))
        starting_index = closing_curly_index + 1
    return styles


def parse_styles_content(unparsed_styling, styles={}):
    # TODO: Remove whitespace
    styling_attributes = unparsed_styling.split(";")
    if len(styling_attributes) <= 1:
        raise SyntaxError("Style properties improperly terminated")
    for styling_attribute in styling_attributes[:len(styling_attributes)-1]:
        try:
            attribute_name, attribute_value = styling_attribute.split(":")
            if attribute_name not in supported_styling_attributes:
                raise SyntaxError(
                    "{0} styling not supported".format(attribute_name))
            if attribute_name == "color":
                styles[attribute_name] = attribute_value
            else:
                attribute_value_int = int(attribute_value)
                styles[attribute_name] = attribute_value_int
        except ValueError:
            raise SyntaxError(
                "Style attribute improperly defined, {0}".format(styling_attribute))
    return styles


data = sys.stdin.read()
print(simple_html_renderer(data))
# idea: inline styling
# idea: reading from a file*
# idea: nested elements*
# idea: tables*
# idea: dependent on above: child styling
# idea: read from url
# idea: get newlines working
# idea: colors!
