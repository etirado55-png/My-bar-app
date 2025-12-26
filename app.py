import streamlit as st
import cloudinary
import cloudinary.uploader
from database import create_tables, add_recipe, update_inventory, get_available_drinks, connect_db

# 1. Setup & Configuration
create_tables()

# Configure Cloudinary (Keys will be stored in Streamlit Secrets later)
cloudinary.config(
    cloud_name = st.secrets["CLOUDINARY_NAME"],
    api_key = st.secrets["CLOUDINARY_KEY"],
    api_secret = st.secrets["CLOUDINARY_SECRET"]
)

st.title("🍸 Show Tech Bar")

tabs = st.tabs(["📖 Menu", "🍺 My Bar", "➕ Add Recipe"])

# --- TAB 1: MENU ---
with tabs[0]:
    st.header("What you can make:")
    drinks = get_available_drinks()
    if not drinks:
        st.info("No full matches found. Update your 'My Bar' list!")
    else:
        for drink in drinks:
            with st.expander(f"{drink[1]}"):
                if drink[4]: # Image URL
                    st.image(drink[4])
                st.write(f"**Ingredients:** {drink[2]}")
                st.write(f"**Instructions:** {drink[3]}")

# --- TAB 2: MY BAR ---
with tabs[1]:
    st.header("Inventory")
    # A master list of ingredients to pick from
    master_list = ["Vodka", "Gin", "Tequila", "Rum", "Lime Juice", "Lemon Juice", "Simple Syrup", "Soda Water", "Triple Sec"]
    
    # Check what's currently in the DB to pre-fill the UI
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ingredient FROM inventory")
    current_stock = [row[0] for row in cursor.fetchall()]
    conn.close()

    on_hand = st.multiselect("Select what's on the shelf:", master_list, default=current_stock)
    
    if st.button("Update Bar"):
        update_inventory(on_hand)
        st.success("Inventory Updated!")

# --- TAB 3: ADD RECIPE ---
with tabs[2]:
    st.header("New Drink")
    name = st.text_input("Drink Name")
    ingredients = st.text_area("Ingredients (comma separated)")
    instructions = st.text_area("Instructions")
    photo = st.file_uploader("Take a photo", type=['jpg', 'png', 'jpeg'])

    if st.button("Save Recipe"):
        img_url = ""
        if photo:
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(photo)
            img_url = upload_result['secure_url']
        
        add_recipe(name, ingredients, instructions, img_url)
        st.success(f"Added {name}!")