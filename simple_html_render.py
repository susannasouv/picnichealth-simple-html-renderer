def find_opening_closing_pairs_of_tags(simple_html, opening_tag, closing_tag):
    opening_to_closing_tag_indices = []
    opening_tag_index = simple_html.find(opening_tag)
    # TODO: check that not escaped tag
    while opening_tag_index != -1:
        closing_tag_index = simple_html.find(closing_tag, opening_tag_index + len(opening_tag))
        if closing_tag_index == -1:
            raise SyntaxError("{0} tag not properly closed".format(opening_tag))
        opening_to_closing_tag_indices.append((opening_tag_index, closing_tag_index))
        opening_tag_index = simple_html.find(opening_tag, closing_tag_index + len(closing_tag))
    return opening_to_closing_tag_indices


def find_opening_closing_pairs_of_nestable_tags(simple_html, opening_tag, closing_tag):
    assert opening_tag != closing_tag
    opening_to_closing_tag_indices = []
    unmatched_indices = []
    opening_tag_index = simple_html.find(opening_tag)
    while opening_tag_index != -1:
        closing_tag_index = simple_html.find(closing_tag, opening_tag_index + len(opening_tag))
        next_opening_tag_index = simple_html.find(opening_tag, opening_tag_index + len(opening_tag))
        if next_opening_tag_index != -1 and next_opening_tag_index < closing_tag_index:
            unmatched_indices.append(opening_tag_index)
        else:
            opening_to_closing_tag_indices.append((opening_tag_index, closing_tag_index))
            opening_tag_index = next_opening_tag_index


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
    open_style_tag = "<style>"
    close_style_tag = "</style>"
    opening_closing_pairs_of_style_tags = find_opening_closing_pairs_of_tags(simple_html, open_style_tag, close_style_tag)
    for start, end in opening_closing_pairs_of_style_tags:
        styles.update(parse_style_tag_content(simple_html[start + len(open_style_tag):end]))
    # parse all of the non-styling content and stitch together
    styleless_html = ""
    non_style_start_index = 0
    for style_start, style_end in opening_closing_pairs_of_style_tags:
        non_style_end_index = style_start
        styleless_html += simple_html[non_style_start_index:non_style_end_index]
        non_style_start_index = style_end + len(close_style_tag)
    # append the final non-style html that comes after the final closing style tag
    styleless_html += simple_html[non_style_start_index:]
    return render_html_with_styles(styleless_html, styles)


def render_html_with_styles(styleless_html, styles={}):
    supported_styleable_elements = ("p")
    opening_p_tag, closing_p_tag = "<p>", "</p>"

    # TODO use find_opening_closing_pairs_of_nestable_tags to support nesting
    opening_closing_pairs_of_p_tags = find_opening_closing_pairs_of_tags(styleless_html, opening_p_tag, closing_p_tag)

    output = ""
    for start, end in opening_closing_pairs_of_p_tags:
        output += parse_p_tag_content(styleless_html[start + len(opening_p_tag):end], styles)

    p_less_html = ""

    non_p_start_index = 0
    for p_start, p_end in opening_closing_pairs_of_p_tags:
        non_p_end_index = p_start
        p_less_html += styleless_html[non_p_start_index:non_p_end_index]
        non_p_start_index = p_end + len(closing_p_tag)
    p_less_html += styleless_html[non_p_start_index:]

    opening_table_tag, closing_table_tag = "<table>", "</table>"
    opening_closing_pairs_of_table_tags = find_opening_closing_pairs_of_tags(p_less_html, opening_table_tag, closing_table_tag)

    for start, end in opening_closing_pairs_of_table_tags:
        output += parse_table_tag_content(styleless_html[start + len(opening_table_tag): end], styles)

    return output


def parse_table_tag_content(table_tag_content, styles={}):
    # TODO
    return ""


def parse_p_tag_content(p_tag_content, styles={}):
    min_height = p_tag_content.count("\n") + 1
    min_width = max([len(line) for line in p_tag_content.split("\n")])
    if "p" in styles:
        p_stylings = styles["p"]
        if "height" in p_stylings:
            intended_height = p_stylings["height"]
            p_tag_content += "\n{0}".format(" " * min_width) * (intended_height - min_height)
        if "margin-bottom" in p_stylings:
            p_tag_content += ("\n{0}".format(" " * min_width) * p_stylings["margin-bottom"])
        if "margin-top" in p_stylings:
            p_tag_content = ("{0}\n".format(" " * min_width) * p_stylings["margin-top"]) + p_tag_content
        if "width" in p_stylings:
            intended_width = p_stylings["width"]
            tmp_p_tag_content = ""
            for line in p_tag_content.split("\n"):
                tmp_p_tag_content += line + ((intended_width - len(line)) * " ") + "\n"
            p_tag_content = tmp_p_tag_content
        if "margin-left" in p_stylings:
            tmp_p_tag_content = ""
            for line in p_tag_content.split("\n"):
                tmp_p_tag_content += (" " * p_stylings["margin-left"]) + line + "\n"
            p_tag_content = tmp_p_tag_content
        if "margin-right" in p_stylings:
            tmp_p_tag_content = ""
            for line in p_tag_content.split("\n"):
                tmp_p_tag_content += line + (" " * (min_width - len(line) + p_stylings["margin-right"])) + "\n"
            p_tag_content = tmp_p_tag_content

    return p_tag_content


def parse_style_tag_content(style_tag_content):
    # removes all whitespace
    style_tag_content = "".join(style_tag_content.split())
    styles = {}
    supported_styleable_elements = ("p", "table")
    supported_styling_attributes = ("height", "width", "margin-bottom", "margin-left", "margin-right", "margin-top")
    starting_index = 0
    while starting_index < len(style_tag_content):
        opening_curly_index = style_tag_content.find("{", starting_index)
        if opening_curly_index == -1:
            raise SyntaxError("Style properties improperly defined")
        element_to_be_styled = style_tag_content[starting_index:opening_curly_index]
        if element_to_be_styled  not in supported_styleable_elements:
            raise SyntaxError("{0} element styling not supported".format(element_to_be_styled))
        closing_curly_index = style_tag_content.find("}", opening_curly_index)
        if closing_curly_index == -1:
            raise SyntaxError("Style properties improperly closed")
        if element_to_be_styled not in styles:
            styles[element_to_be_styled] = {}
        unparsed_styling = style_tag_content[opening_curly_index + 1:closing_curly_index]
        styling_attributes = unparsed_styling.split(";")
        if len(styling_attributes) <= 1:
            raise SyntaxError("Style properties improperly terminated")
        # exclude the empty string at the end
        for styling_attribute in styling_attributes[:len(styling_attributes)-1]:
            try:
                attribute_name, attribute_value = styling_attribute.split(":")
                if attribute_name not in supported_styling_attributes:
                    raise SyntaxError("{0} styling not supported".format(attribute_name))
                attribute_value_int = int(attribute_value)
                styles[element_to_be_styled][attribute_name] = attribute_value_int
            except ValueError:
                raise SyntaxError("Style attribute improperly defined, {0}".format(styling_attribute))
        starting_index = closing_curly_index + 1
    return styles
