import streamlit as st

def get_recommendations(age_group, interest):
    """
    Simple dummy recommendation logic.
    In a real app, this would query a database or an LLM.
    """
    recommendations = {
        "3-5": {
            "Science": [
                "Baking Soda Volcano: Mix baking soda and vinegar for a fizzy explosion.",
                "Nature Walk: Collect leaves and stones to learn about shapes and textures.",
                "Sink or Float: Test different household items in a bowl of water."
            ],
            "Arts": [
                "Finger Painting: Use non-toxic paints to create messy art.",
                "Playdough Sculpting: Build animals or shapes with playdough.",
                "Macaroni Art: Glue dry pasta onto paper to make pictures."
            ],
            "Reading": [
                "The Very Hungry Caterpillar by Eric Carle",
                "Goodnight Moon by Margaret Wise Brown",
                "Where the Wild Things Are by Maurice Sendak"
            ]
        },
        "6-8": {
            "Science": [
                "Build a Solar Oven: Use a pizza box and foil to melt s'mores.",
                "Grow Crystals: Use salt or sugar water to grow crystals on a string.",
                "Magnet Hunt: Use a magnet to find magnetic items around the house."
            ],
            "Arts": [
                "Origami: Learn to fold paper cranes and frogs.",
                "Recycled Robots: Build robots out of old cardboard boxes and bottles.",
                "Comic Book Creation: Draw and write a short comic story."
            ],
            "Reading": [
                "Charlotte's Web by E.B. White",
                "Magic Tree House series by Mary Pope Osborne",
                "Matilda by Roald Dahl"
            ]
        },
        "9-12": {
            "Science": [
                "Lemon Battery: create electricity using a lemon.",
                "Coding: Start with Scratch or Python for beginners.",
                "Stargazing: Identify constellations and planets."
            ],
            "Arts": [
                "Stop Motion Animation: Create a movie using a phone and toys.",
                "Photography: Learn about angles and lighting.",
                "Sewing: Stitch a simple pillow or bag."
            ],
            "Reading": [
                "Harry Potter series by J.K. Rowling",
                "Percy Jackson & The Olympians by Rick Riordan",
                "Wonder by R.J. Palacio"
            ]
        }
    }
    
    return recommendations.get(age_group, {}).get(interest, ["Try exploring the library or a local park!"])

def main():
    st.set_page_config(page_title="Kids Activity Recommender", page_icon="🎈")
    
    st.title("🎈 Kids Activity Helper")
    st.write("Find the perfect activity, book, or experiment for your child!")
    
    # Sidebar inputs
    st.sidebar.header("Your Child's Info")
    age_group = st.sidebar.selectbox(
        "Select Age Group",
        ("3-5", "6-8", "9-12")
    )
    
    interest = st.sidebar.selectbox(
        "Select Interest",
        ("Science", "Arts", "Reading")
    )
    
    if st.button("Get Ideas!"):
        st.subheader(f"Suggestions for {interest} (Age {age_group})")
        ideas = get_recommendations(age_group, interest)
        
        for idea in ideas:
            st.info(idea)

    st.markdown("---")
    st.write("Built with Streamlit & Python 🐍")

if __name__ == "__main__":
    main()
