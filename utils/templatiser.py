def templatise_ability(name:str, upgrade:str, cooldown:str, text:str):
    template = f"""{{{{UnitAbility
|name={name}
|upgrade={upgrade}
|cooldown={cooldown}
|text={text}
}}}}"""
    return template

def templatise_passive(name:str, upgrade:str, text:str):
    template = f"""{{{{UnitPassive
|name={name}
|upgrade={upgrade}
|text={text}
}}}}"""
    return template
