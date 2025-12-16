import random

# Milestone definitions for different age groups
MILESTONES = {
    "2": [
        "Kicks a ball",
        "Runs",
        "Walks up and down stairs holding on",
        "Eats with a spoon",
        "Follows 2-step instructions",
        "Says sentences with 2 to 4 words",
        "Sorts shapes and colors",
        "Plays make-believe",
    ],
    "3": [
        "Climbs well",
        "Runs easily",
        "Pedals a tricycle (3-wheel bike)",
        "Walks up and down stairs, one foot on each step",
        "Shows affection for friends without prompting",
        "Takes turns in games",
        "Understands 'mine' and 'his' or 'hers'",
        "Say first name, age, and sex",
        "Talks well enough for strangers to understand most of the time",
    ],
    "4": [
        "Hops and stands on one foot up to 2 seconds",
        "Catches a bounced ball most of the time",
        "Pours, cuts with supervision, and mashes their own food",
        "Would rather play with other children than by themselves",
        "Cooperates with other children",
        "Retells a story or sings a song",
        "Correctly names some colors and some numbers",
        "Draws a person with 2 to 4 body parts",
    ],
    "5": [
        "Stands on one foot for 10 seconds or longer",
        "Hops; may be able to skip",
        "Can do a somersault",
        "Uses a fork and spoon and sometimes a table knife",
        "Can use the toilet on her own",
        "Likes to sing, dance, and act",
        "Is aware of gender",
        "Speaks very clearly",
        "Tells a simple story using full sentences",
    ]
}

# Activity repository by age group
# Each activity has: title, description, materials, duration, benefits
ACTIVITIES_DB = {
    "2": [
        {
            "title": "Color Sorting with Toys",
            "description": "Gather various colorful toys (blocks, cars, balls). Prepare colored bins or pieces of paper (Red, Blue, Green). Ask your child to put the red toys on the red paper, etc.",
            "materials": "Colorful toys, colored paper or bins",
            "duration": "15-20 mins",
            "benefits": "Color recognition, fine motor skills, categorization"
        },
        {
            "title": "Sticky Note Wall Hunt",
            "description": "Stick colorful sticky notes on a wall at different heights (some they have to reach for, some they squat for). Ask them to 'catch' a specific color.",
            "materials": "Post-it notes",
            "duration": "10-15 mins",
            "benefits": "Gross motor skills, reaching, squatting, color recognition"
        },
        {
            "title": "Animal Walk",
            "description": "Call out an animal and demonstrate how it moves. 'Waddle like a penguin', 'Hop like a bunny', 'Stomp like an elephant'. Encourage them to mimic you.",
            "materials": "None",
            "duration": "10 mins",
            "benefits": "Gross motor skills, imagination, listening skills"
        },
        {
            "title": "Rice Bin Sensory Play",
            "description": "Fill a bin with dry rice. Add spoons, cups, and hidden small toys. Let them dig, pour, and scoop.",
            "materials": "Bin, rice, scoops, cups",
            "duration": "20-30 mins",
            "benefits": "Sensory processing, fine motor control"
        },
        {
            "title": "Pompom Push",
            "description": "Cut small holes in the lid of a shoe box or yogurt container. Have your child push pompoms through the holes.",
            "materials": "Box with lid, pompoms",
            "duration": "15 mins",
            "benefits": "Fine motor skills, pincer grasp, object permanence"
        },
        {
            "title": "Big Art",
            "description": "Tape a large piece of paper to the floor. Give them chunky crayons and let them draw freely using big arm movements.",
            "materials": "Large paper, crayons",
            "duration": "20 mins",
            "benefits": "Creativity, shoulder stability, fine motor skills"
        },
        {
            "title": "Pillow Road",
            "description": "Line up pillows on the floor to make a bumpy road. Hold their hand as they walk over the pillows.",
            "materials": "Pillows",
            "duration": "10-15 mins",
            "benefits": "Balance, gross motor skills"
        },
        {
            "title": "Water Transfer",
            "description": "Two bowls, one with water, one empty. Give them a sponge. Show them how to soak the sponge, move it to the empty bowl, and squeeze the water out.",
            "materials": "Bowls, water, sponge",
            "duration": "15-20 mins",
            "benefits": "Hand strength, coordination, sensory play"
        }
    ],
    "3": [
        {
            "title": "Shape Scavenger Hunt",
            "description": "Cut out a circle, square, and triangle from paper. Hold up the circle and ask your child to find something round in the house (clock, plate). Repeat for other shapes.",
            "materials": "Paper shapes",
            "duration": "20 mins",
            "benefits": "Shape recognition, observation skills"
        },
        {
            "title": "Pasta Necklace",
            "description": "Use dry penne pasta and a shoelace or yarn with a taped end. Thread the pasta to make a necklace. You can paint the pasta beforehand for extra fun.",
            "materials": "Dry pasta, yarn/string",
            "duration": "20-30 mins",
            "benefits": "Fine motor skills, hand-eye coordination, focus"
        },
        {
            "title": "Freeze Dance",
            "description": "Play music and dance. Stop the music suddenly and yell 'Freeze!'. Everyone must stand still like a statue. Start again.",
            "materials": "Music player",
            "duration": "15 mins",
            "benefits": "Listening skills, gross motor control, inhibition"
        },
        {
            "title": "Build a Fort",
            "description": "Use chairs, blankets, and pillows to build a fort or a tent. Read a book inside with a flashlight.",
            "materials": "Blankets, chairs, flashlight",
            "duration": "30+ mins",
            "benefits": "Problem solving, imagination, bonding"
        },
        {
            "title": "Simple Simon Says",
            "description": "Play 'Simon Says' with simple body parts. 'Simon says touch your nose'. 'Touch your toes' (don't do it!).",
            "materials": "None",
            "duration": "10-15 mins",
            "benefits": "Body awareness, listening, impulse control"
        },
        {
            "title": "Paper Plate Masks",
            "description": "Cut eye holes in a paper plate. Let them decorate it as a lion or monster with crayons and stuck-on paper bits.",
            "materials": "Paper plates, glue, crayons",
            "duration": "20 mins",
            "benefits": "Creativity, fine motor skills"
        },
        {
            "title": "Ball Rolling",
            "description": "Sit legs apart facing each other. Roll a ball back and forth. Try to roll it fast, slow, or bounce it once.",
            "materials": "Ball",
            "duration": "15 mins",
            "benefits": "Social interaction, turn-taking, hand-eye coordination"
        },
        {
            "title": "Matching Socks",
            "description": "Dump out the clean sock basket. Ask your child to find the matching pairs and roll them into balls.",
            "materials": "Clean socks",
            "duration": "15 mins",
            "benefits": "Visual discrimination, helping with chores, fine motor"
        }
    ],
    "4": [
        {
            "title": "Obstacle Course",
            "description": "Create a complex course: Crawl under the table, jump over the cushion, walk along the tape line, throw a sock in the laundry basket.",
            "materials": "Household items",
            "duration": "20-30 mins",
            "benefits": "Gross motor planning, memory, agility"
        },
        {
            "title": "Name Writing Practice",
            "description": "Write their name in highlighter or yellow marker. Have them trace over it with a pencil or dark crayon. Then try copying it below.",
            "materials": "Paper, highlighter, pencil",
            "duration": "15 mins",
            "benefits": "Letter formation, fine motor control"
        },
        {
            "title": "Scissor Skills",
            "description": "Draw straight lines, zig-zags, and curves on paper strips. Have your child cut along the lines using child-safe scissors.",
            "materials": "Paper, kid scissors",
            "duration": "15-20 mins",
            "benefits": "Bilateral coordination, fine motor skills"
        },
        {
            "title": "Memory Card Game",
            "description": "Use a deck of cards or matching picture cards. Place 6-8 pairs face down. Take turns flipping two over to find a match.",
            "materials": "Cards",
            "duration": "20 mins",
            "benefits": "Working memory, concentration, turn-taking"
        },
        {
            "title": "Story Stones",
            "description": "Paint simple pictures on rocks (sun, house, cat). Put them in a bag. Pull one out and start a story. Pull another to continue it.",
            "materials": "Rocks, paint/markers",
            "duration": "20 mins",
            "benefits": "Language development, narrative skills, creativity"
        },
        {
            "title": "Baking Helper",
            "description": "Bake cookies or muffins together. Let them measure (with help), pour, and stir the batter.",
            "materials": "Baking ingredients, bowls",
            "duration": "45 mins",
            "benefits": "Math concepts (volume), following directions, patience"
        },
        {
            "title": "Red Light, Green Light",
            "description": "Play the classic game. Green light = run/walk, Red light = stop immediately. Add 'Yellow light' for slow motion.",
            "materials": "None",
            "duration": "15 mins",
            "benefits": "Self-regulation, listening, gross motor skills"
        },
        {
            "title": "Leaf Rubbings",
            "description": "Collect leaves. Place them under paper and rub with the side of a crayon to reveal the texture and shape.",
            "materials": "Leaves, paper, crayons",
            "duration": "20 mins",
            "benefits": "Nature appreciation, fine motor control"
        }
    ],
    "5": [
        {
            "title": "Board Game Night",
            "description": "Play a simple board game like Snakes and Ladders or Candy Land. Focus on following rules and handling winning/losing.",
            "materials": "Board game",
            "duration": "30 mins",
            "benefits": "Social skills, counting, emotional regulation"
        },
        {
            "title": "DIY Pizza",
            "description": "Make mini pizzas on english muffins. Let them chop soft toppings (mushrooms, peppers) with a kid-safe knife and arrange them.",
            "materials": "English muffins, sauce, cheese, toppings",
            "duration": "30 mins",
            "benefits": "Independence, fine motor skills, nutrition awareness"
        },
        {
            "title": "Rhyming Challenge",
            "description": "Say a word like 'Cat'. Ask them to say as many words as they can that rhyme with it (bat, hat, mat). Take turns.",
            "materials": "None",
            "duration": "10-15 mins",
            "benefits": "Phonological awareness, language skills"
        },
        {
            "title": "Hopscotch",
            "description": "Draw a hopscotch grid with chalk outside. Teach them how to throw a stone and hop through the grid avoiding lines.",
            "materials": "Chalk, stone",
            "duration": "20 mins",
            "benefits": "Balance, counting, gross motor coordination"
        },
        {
            "title": "Learn a Phone Number",
            "description": "Turn it into a song or game. Practice dialing it on a play phone or a real phone (unplugged or locked).",
            "materials": "Phone toy",
            "duration": "15 mins",
            "benefits": "Safety, memorization, number recognition"
        },
        {
            "title": "Tie Your Shoes",
            "description": "Practice tying shoelaces. Use a cardboard shoe template with two different colored laces to make it easier to see the steps.",
            "materials": "Shoe or practice board",
            "duration": "15 mins",
            "benefits": "Fine motor skills, persistence, independence"
        },
        {
            "title": "Nature Journal",
            "description": "Go for a walk. Ask them to draw what they see in a notebook (a bird, a flower) and try to label it (with help spelling).",
            "materials": "Notebook, pencil",
            "duration": "30 mins",
            "benefits": "Observation, writing skills, science"
        },
        {
            "title": "Pattern Making",
            "description": "Use beads, lego bricks, or colored pasta. Start a pattern (Red-Blue-Red-Blue) and ask them to finish it. Try A-A-B or A-B-C patterns.",
            "materials": "Small colored objects",
            "duration": "20 mins",
            "benefits": "Math logic, cognitive patterning, fine motor"
        }
    ]
}

def get_milestones(age_group):
    return MILESTONES.get(str(age_group), [])

def get_activity_for_date(day_of_month: int, age_group: str):
    """Returns an activity based on the day of the month for a specific age group."""
    activities = ACTIVITIES_DB.get(str(age_group), ACTIVITIES_DB["3"]) # Default to 3
    # Cycle through activities
    index = (day_of_month - 1) % len(activities)
    return activities[index]

def get_random_activity(age_group: str, exclude_titles=None):
    """Returns a random activity for the age group, excluding specific titles."""
    if exclude_titles is None:
        exclude_titles = []

    activities = ACTIVITIES_DB.get(str(age_group), ACTIVITIES_DB["3"])
    available = [a for a in activities if a["title"] not in exclude_titles]

    if not available:
        return random.choice(activities) # Return anything if all excluded

    return random.choice(available)
