#! venv/bin/python

from gpt4all import GPT4All


GPT4All_MODEL = "wizardlm-13b-v1.2.Q4_0.gguf"

model = GPT4All(GPT4All_MODEL)


LOCATION_PROMPT = """
=========== Instructions ===========

Create a vivid description of fictional location

The output should be in Markdown format.  Include bullet points and sections for each detail.

Include the following details:

- landscape
- climate
- flora
- fauna
- architecture
- culture
- history

Can include other details as well.  Be creative and have fun!

=========== Example ===========

# The Enchanted Forest

## Landscape

- The Enchanted Forest is a dense forest with towering trees that block out the sun.

## Climate

- The climate is temperate with mild temperatures year-round.

### Flora

- The forest is filled with a variety of plants and flowers that glow in the dark.

### Fauna

- The forest is home to magical creatures like unicorns and fairies.

## Culture

- The culture is based on magic and nature.

### Architecture

- The architecture is made of living trees that grow into buildings.

### History

- The forest was created by a powerful wizard centuries ago.
- The wizard used his magic to protect the forest from harm.
- The forest is now a sanctuary for magical creatures and nature.

=========== End of Instructions ===========
"""


PERSON_PROMPT = """
=========== Instructions ===========

Create a detailed character profile for an RPG

The output should be in Markdown format. Include sections and bullet points for each detail of the character.

Include the following details:

- Name and Title
- Race and Class
- Appearance
- Personality
- Skills and Abilities
- Equipment and Artifacts
- Background Story

Feel free to include other details such as alignment, companions, or notable achievements. Be creative and have fun!

=========== Example ===========

# Seraphina Lightweaver, The Dawnbringer

## Race and Class

- Race: Elf
- Class: Paladin

## Appearance

- Tall and slender with golden skin
- Long, flowing silver hair
- Piercing blue eyes that glow when using magic
- Wears shining armor engraved with ancient runes

## Personality

- Compassionate and unwaveringly just
- Values honor and courage
- Seeks to bring light to the darkest places

## Skills and Abilities

- Master swordswoman
- Proficient in healing magic
- Able to summon a celestial steed

## Equipment and Artifacts

- Sunblade: A sword that emits radiant light
- Armor of the Valiant: Enchanted armor that provides protection from dark magic
- Amulet of Hope: Boosts healing powers and inspires courage in allies

## Background Story

- Born into a noble family but forsook her title to join the paladins
- Traveled the land to fight darkness and corruption
- Became a beacon of hope for those fighting against evil


=========== Example A ===========

# Seraphina Lightweaver, The Dawnbringer

## Race and Class

- Race: Elf
- Class: Paladin

## Appearance

- Tall and slender with golden skin
- Long, flowing silver hair
- Piercing blue eyes that glow when using magic
- Wears shining armor engraved with ancient runes

## Personality

- Compassionate and unwaveringly just
- Values honor and courage
- Seeks to bring light to the darkest places

## Skills and Abilities

- Master swordswoman
- Proficient in healing magic
- Able to summon a celestial steed

## Equipment and Artifacts

- Sunblade: A sword that emits radiant light
- Armor of the Valiant: Enchanted armor that provides protection from dark magic
- Amulet of Hope: Boosts healing powers and inspires courage in allies

## Background Story

- Born into a noble family but forsook her title to join the paladins
- Traveled the land to fight darkness and corruption
- Became a beacon of hope for those fighting against evil

=========== Example B ===========

# Grog Stonefist, The Mountain's Roar

## Race and Class

- Race: Dwarf
- Class: Berserker

## Appearance

- Short, muscular build with skin as tough as leather
- Bald head with a long, braided beard mixed with gray and brown strands
- Deep scars across his face and arms, trophies from countless battles
- Wears minimal armor, relying on his skin and will to withstand blows

## Personality

- Boisterous and fearless, often diving headfirst into battle
- Has a surprisingly good sense of humor, often cracking jokes
- Loyal to friends, treats his comrades like family

## Skills and Abilities

- Incredible strength, capable of wielding large axes with ease
- High endurance, can fight for hours without tiring
- Rage ability, becomes stronger as he takes damage

## Equipment and Artifacts

- Twin Axes of Grunvald: Legendary axes that were said to have split a mountain in two
- Belt of the Bear: Grants him strength and endurance beyond his natural capabilities

## Background Story

- Grew up in the mining tunnels of his homeland, learning to fight in the tight corridors
- Became a legend after saving his village from a marauding dragon
- Wanders the lands looking for the next great challenge

=========== Example C ===========

# Thalia Whisperwind, Shadow of the Forest

## Race and Class

- Race: Half-Elf
- Class: Ranger

## Appearance

- Medium height with a lithe, athletic build
- Dark green eyes that blend with the forest
- Long, dark brown hair often kept in a braid
- Wears leather armor dyed in shades of green and brown

## Personality

- Quiet and introspective, prefers the company of animals to people
- Fiercely protective of the natural world
- Skilled strategist, always thinking several steps ahead

## Skills and Abilities

- Expert archer, never misses her mark
- Able to communicate with animals and bend them to her will
- Stealthy, can move through the forest without making a sound

## Equipment and Artifacts

- Bow of the Greenwood: A magical bow that can shoot arrows of pure energy
- Cloak of Leaves: Renders her nearly invisible when in wooded areas

## Background Story

- Orphaned at a young age and raised by the creatures of the forest
- Learned the ways of the ranger to protect her home from those who would harm it
- Now roams the lands, defending the natural world wherever it is threatened
=========== End of Instructions ===========
"""

def check_stop(token_id, token_string):
    # print(token_id, token_string)
    return True


def generate_location():
    with model.chat_session():
        response = model.generate(
            PERSON_PROMPT,
            temp=1.4,
            max_tokens=8000,
            callback=check_stop,
            repeat_penalty=1.6,
        )
        print(response)


if __name__ == '__main__':
    generate_location()
