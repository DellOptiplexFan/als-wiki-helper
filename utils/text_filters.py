import re

STATUS_EFFECTS = {
        "Bleed": "{{Passive|Bleed}}",
        "Flame": "{{Passive|Flame}}",
        "Cripple": "{{Passive|Cripple}}",
        "Dismantle": "{{Passive|Dismantle}}",
        "Fear": "{{Passive|Fear}}",
        "Freeze": "{{Passive|Freeze}}",
        "Poison": "{{Passive|Poison}}",
        "Slow": "{{Passive|Slow}}",
        "Electrified": "{{Passive|Electrified}}",
        "Stun": "{{Passive|Stun}}",
        "Conquered": "{{Passive|Conquered}}",
        "Hemorrhage": "{{Passive|Hemorrhage}}",
        "Black Flames": "{{Passive|Black Flame}}",
        "Bomb": "{{Passive|Bomb}}",
        "Detonation": "{{Passive|Detonation}}",
        "Random": "{{Passive|Random}}",
        "Frostbite": "{{Passive|Frostbite}}",
        "Pressure": "{{Passive|Pressure}}",
        "Blizzard": "{{Passive|Blizzard}}",
        "Bolt": "{{Passive|Bolt}}",
        "Mutilate": "{{Passive|Mutilate}}",
        "Sunburn": "{{Passive|Sunburn}}",
        "Weakened": "{{Passive|Weakened}}",
        "Blue Flames": "{{Passive|Blue Flames}}",
        "Plasma": "{{Passive|Plasma}}",
        "Accelerate": "{{Passive|Accelerate}}",
        "Scorched": "{{Passive|Scorched}}",
        "WindSheer": "{{Passive|WindSheer}}",
        "Soaked": "{{Passive|Soaked}}",
        "AntiMagic": "{{Passive|AntiMagic}}",
        "Despair": "{{Passive|Despair}}",
        "Blaze": "{{Passive|Blaze}}",
        "Petrification": "{{Passive|Petrification}}",
        "Extinguish": "{{Passive|Extinguish}}",
        "Rupture": "{{Passive|Rupture}}",
        "Exposed": "{{Passive|Exposed}}",
        "Bloodlust": "{{Passive|Bloodlust}}",
        "Solar Flames": "{{Passive|Solar Flames}}",
        "Unstable": "{{Passive|Unstable}}",
        "Shred": "{{Passive|Shred}}",
        "Brittle": "{{Passive|Brittle}}",
        "Daze": "{{Passive|Daze}}",
        "Restrict": "{{Passive|Restrict}}",
        "Dismantled": "{{Passive|Dismantle}}"
    }

def status_effects(text: str) -> str:
    for effect in sorted(STATUS_EFFECTS, key=len, reverse=True):
        pattern = re.compile(rf"\b{re.escape(effect)}\b", re.IGNORECASE)
        text = pattern.sub(STATUS_EFFECTS[effect] + " ", text)
    return text
