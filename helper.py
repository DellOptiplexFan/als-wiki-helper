import re
def convert_to_html(text: str) -> str:
    outputLines = []
    in_ul = False
    for line in text.splitlines():
        if line[0] == "-":
            if in_ul == False:
                in_ul=True
                outputLines.append("<ul>")
            outputLines.append("<li>" + line[1:] + "</li>")
        else:
            if in_ul == True:
                outputLines.append("</ul>")
                in_ul=False
            outputLines.append("<div>" + line + "</div>")
    if in_ul == True:
        outputLines.append("</ul>")
    return "\n".join(line for line in outputLines)

def color_brackets(text: str) -> str:
    outputLines = []
    for line in text.splitlines():
        newLine = ""
        counter = 0
        for char in line:
            if char in ["(","["]:
                if counter==0:
                    newLine = newLine + ' <span style="color:grey;">' + char
                else:
                    newLine = newLine + char
                counter+=1
            elif char in [")","]"]:
                counter-=1
                newLine = newLine + char
                if counter==0:
                    newLine = newLine + '</span> '
            else:
                newLine= newLine + char
        outputLines.append(newLine)
    return "\n".join(line for line in outputLines)
            

def color_numbers(text:str, color:str) -> str:
    pattern = re.compile(
        r"""
        (?<![#])                      # not preceded by '#'
        (?<!\w)                       # not preceded by a letter/digit
        (                             
            [+\-]?                    # optional sign
            (?:\d+(\.\d+)?|\.\d+)     # 12, 12.34, or .45
            (?:%|[skMBT])?            # Optional %, s, k, M, B, T
        )
        (?!\w)                        # Not followed by a letter/digit
        """,
        re.VERBOSE
    )
    outputLines = [pattern.sub(rf'<span style="color:{color};"> \1 </span>', line) for line in text.splitlines()]
    return "\n".join(line for line in outputLines)


def colorize(text:str, color:str) -> str:
    text = color_brackets(text)
    text = color_numbers(text, color)
    return text

def full_convert_passive(text:str) -> str:
    text = convert_to_html(text)
    text = colorize(text, "cyan")
    return text

def full_convert_ability(text:str) -> str:
    text = convert_to_html(text)
    text = colorize(text, "red")
    return text

print(full_convert_passive("""This unit has a Mass bar that fills over time (5/s, uncapped).
-When an ally uses an active in range: gain 100 Mass over 10s (stackable).
-If stunned: instantly cleanse stun and gain 300 Mass over 20s (5s CD).
-If target is set to None: gain +25 Mass/s until attacking again."""))
