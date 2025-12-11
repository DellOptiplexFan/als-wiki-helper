import re

def convert_to_html(text: str) -> str:
    output = []
    in_ul = False

    for line in text.splitlines():
        if line.startswith("-"):
            if not in_ul:
                in_ul = True
                output.append("<ul>")
            output.append("<li>" + line[1:] + "</li>")
        else:
            if in_ul:
                in_ul = False
                output.append("</ul>")
            output.append("<div>" + line + "</div>")

    if in_ul:
        output.append("</ul>")

    return "\n".join(output)


def color_numbers(text: str, color: str) -> str:
    pattern = re.compile(
        r"""
        (?<![#])(?<!\w)
        ([+\-]?(?:\d+(\.\d+)?|\.\d+)(?:%|[skMBT])?)
        (?!\w)
        """,
        re.VERBOSE
    )

    return pattern.sub(rf'<span style="color:{color};"> \1 </span>', text)


def color_brackets(text: str) -> str:
    out = []
    for line in text.splitlines():
        new = ""
        depth = 0
        for c in line:
            if c in "([":  
                if depth == 0:
                    new += f' <span style="color:grey;">{c}'
                else:
                    new += c
                depth += 1
            elif c in ")]":
                depth -= 1
                new += c
                if depth == 0:
                    new += "</span> "
            else:
                new += c
        out.append(new)
    return "\n".join(out)


def colorize(text: str, color: str) -> str:
    text = color_brackets(text)
    text = color_numbers(text, color)
    return text
