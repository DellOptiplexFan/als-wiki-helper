import re
from utils.text_filters import status_effects
from utils.html_color import convert_to_html, colorize
from utils.templatiser import templatise_ability, templatise_passive

def full_convert_passive(text, name, upgrade):
    text = status_effects(text)
    text = convert_to_html(text)
    text = colorize(text, "cyan")
    return templatise_passive(name=name, upgrade=upgrade, text=text)

def full_convert_ability(text, name, upgrade, cooldown):
    text = status_effects(text)
    text = convert_to_html(text)
    text = colorize(text, "red")
    return templatise_ability(name=name, upgrade=upgrade, cooldown=cooldown, text=text)