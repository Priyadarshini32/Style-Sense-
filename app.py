# app.py
import os
import cv2
import numpy as np
from flask import Flask, request, render_template
from PIL import ImageColor, Image
import pandas as pd
from collections import Counter
import urllib.request
import random

# Load styles and images data
try:
    print("Loading styles and images data...")
    styles = pd.read_csv('data/styles.csv', on_bad_lines='skip', low_memory=False)
    styles.columns = styles.columns.str.lower()
    styles['id'] = styles['id'].astype(str)
    images_df = pd.read_csv('data/images.csv', on_bad_lines='skip', low_memory=False)
    images_df['filename'] = images_df['filename'].astype(str)
    print(f"Loaded {len(styles)} style records and {len(images_df)} image records")
except FileNotFoundError:
    print("Warning: data/styles.csv or data/images.csv not found. Creating empty DataFrames.")
    styles = pd.DataFrame()
    images_df = pd.DataFrame()
except Exception as e:
    print(f"Error loading styles/images data: {e}")
    styles = pd.DataFrame()
    images_df = pd.DataFrame()

# Skin tone mapping
SKIN_TONES = {
    "#373028": "Deepest Skin",
    "#422811": "Very Deep",
    "#513B2E": "Deep Brown",
    "#6F503C": "Medium Brown",
    "#81654F": "Tan",
    "#9D7A54": "Light Tan",
    "#BEA07E": "Medium Fair",
    "#E5C8A6": "Light Fair",
    "#E7C1B8": "Warm Fair",
    "#F3DAD6": "Very Fair",
    "#FBF2F3": "Pale",
}

SKIN_TONE_TO_COLOR = {
    "#373028": ["Navy Blue", "Black", "Charcoal", "Burgundy", "Maroon", "Olive", "Rust", "Gold", "Cream", "Peach"],
    "#422811": ["Navy Blue", "Brown", "Khaki", "Olive", "Maroon", "Mustard", "Teal", "Tan", "Rust", "Burgundy"],
    "#513B2E": ["Cream", "Beige", "Olive", "Burgundy", "Red", "Orange", "Mustard", "Bronze", "Teal", "Peach"],
    "#6F503C": ["Beige", "Brown", "Green", "Khaki", "Cream", "Peach", "Lime Green", "Olive", "Maroon", "Rust", "Mustard"],
    "#81654F": ["Beige", "Off White", "Sea Green", "Cream", "Lavender", "Mauve", "Burgundy", "Yellow", "Lime Green"],
    "#9D7A54": ["Olive", "Khaki", "Yellow", "Sea Green", "Turquoise Blue", "Coral", "White", "Gold", "Peach"],
    "#BEA07E": ["Coral", "Sea Green", "Turquoise Blue", "Pink", "Lavender", "Rose", "White", "Peach", "Teal", "Fluorescent Green"],
    "#E5C8A6": ["Turquoise Blue", "Peach", "Teal", "Pink", "Red", "Rose", "Off White", "White", "Cream", "Gold", "Yellow"],
    "#E7C1B8": ["Pink", "Rose", "Peach", "White", "Off White", "Beige", "Lavender", "Teal", "Fluorescent Green"],
    "#F3DAD6": ["White", "Cream", "Peach", "Pink", "Rose", "Lavender", "Mustard", "Lime Green", "Light Blue", "Fluorescent Green"],
    "#FBF2F3": ["Soft Pastels (Peach, Lavender, Pink)", "White", "Off White", "Rose", "Light Blue", "Sea Green", "Fluorescent Green", "Silver", "Cream", "Tan"]
}

NEUTRALS = ["Black", "White", "Beige", "Cream", "Off White", "Grey", "Charcoal"]

def detect_skin_tone(image):
    """Detect skin tone from image"""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(image, (200, 200))
    average_color = resized_image.mean(axis=0).mean(axis=0)
    avg_color_hex = "#{:02x}{:02x}{:02x}".format(int(average_color[0]), int(average_color[1]), int(average_color[2]))
    
    # Find closest skin tone
    avg_color_rgb = np.array(ImageColor.getrgb(avg_color_hex))
    closest_tone_hex = min(
        SKIN_TONES.keys(),
        key=lambda hex_code: np.linalg.norm(avg_color_rgb - np.array(ImageColor.getrgb(hex_code)))
    )
    return closest_tone_hex, SKIN_TONES[closest_tone_hex]

def recommend_outfits(styles_df, skin_tone_hex, gender, usage):
    """Generate outfit recommendations based on skin tone and preferences"""
    if styles_df.empty:
        return []
    
    # Get recommended colors
    recommended_colors = SKIN_TONE_TO_COLOR.get(skin_tone_hex, []) + NEUTRALS
    
    # Filter dataset
    filtered = styles_df.copy()
    if 'gender' in filtered.columns:
        filtered = filtered[filtered['gender'].str.lower() == gender.lower()]
    
    if 'basecolour' in filtered.columns:
        filtered = filtered[filtered['basecolour'].isin(recommended_colors)]
    
    # Separate by category
    topwear = filtered[filtered['subcategory'] == 'Topwear'] if 'subcategory' in filtered.columns else pd.DataFrame()
    bottomwear = filtered[filtered['subcategory'] == 'Bottomwear'] if 'subcategory' in filtered.columns else pd.DataFrame()
    footwear = filtered[filtered['mastercategory'] == 'Footwear'] if 'mastercategory' in filtered.columns else pd.DataFrame()
    
    # Filter by usage if available
    if 'usage' in filtered.columns:
        topwear = topwear[topwear['usage'].isin(usage)]
        bottomwear = bottomwear[bottomwear['usage'].isin(usage)]
    
    # Generate combinations
    outfit_combinations = []
    if not topwear.empty and not bottomwear.empty and not footwear.empty:
        for top in topwear.head(10).itertuples():
            for bottom in bottomwear.head(10).itertuples():
                for foot in footwear.head(10).itertuples():
                    if hasattr(top, 'basecolour') and hasattr(bottom, 'id') and hasattr(foot, 'id'):
                        bottom_color = random.choice([c for c in recommended_colors if c != top.basecolour]) if len(recommended_colors) > 1 else top.basecolour
                        footwear_color = random.choice([random.choice([c for c in recommended_colors if c != bottom_color]), random.choice([c for c in recommended_colors if c in NEUTRALS])])
                        
                        outfit_combinations.append({
                            "Topwear": top.id,
                            "Bottomwear": bottom.id,
                            "Footwear": foot.id,
                            "Topwear Color": top.basecolour,
                            "Bottomwear Color": bottom_color,
                            "Footwear Color": footwear_color
                        })
    
    # Return 5 random combinations
    if outfit_combinations:
        return random.sample(outfit_combinations, min(5, len(outfit_combinations)))
    return []

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def home():
    """Home page route"""
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded'
        file = request.files['file']
        if file.filename == '':
            return 'No file selected'
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
        gender = request.form.get('gender', 'Men')
        usage = request.form.getlist('usage') or ['Casual']
        img = cv2.imread(filename)
        if img is None:
            return 'Error reading image'
        skin_hex, skin_name = detect_skin_tone(img)
        outfits_raw = recommend_outfits(styles, skin_hex, gender, usage)
        outfits = []
        for outfit in outfits_raw:
            if styles.empty:
                continue
            top_id = str(outfit['Topwear'])
            bottom_id = str(outfit['Bottomwear'])
            foot_id = str(outfit['Footwear'])
            top_row = styles[styles['id'] == top_id].head(1) if 'id' in styles.columns else pd.DataFrame()
            bottom_row = styles[styles['id'] == bottom_id].head(1) if 'id' in styles.columns else pd.DataFrame()
            foot_row = styles[styles['id'] == foot_id].head(1) if 'id' in styles.columns else pd.DataFrame()
            # Exclude NA/blanks
            def valid_usage(row):
                u = row['usage'].strip().upper() if 'usage' in row and pd.notnull(row['usage']) else ''
                return u not in ('NA', '', '(BLANKS)')
            if (not top_row.empty and not valid_usage(top_row.iloc[0])) or (not bottom_row.empty and not valid_usage(bottom_row.iloc[0])) or (not foot_row.empty and not valid_usage(foot_row.iloc[0])):
                continue
            top_name = top_row['productdisplayname'].values[0] if not top_row.empty and 'productdisplayname' in top_row.columns else f"Topwear {top_id}"
            bottom_name = bottom_row['productdisplayname'].values[0] if not bottom_row.empty and 'productdisplayname' in bottom_row.columns else f"Bottomwear {bottom_id}"
            foot_name = foot_row['productdisplayname'].values[0] if not foot_row.empty and 'productdisplayname' in foot_row.columns else f"Footwear {foot_id}"
            # Get extra columns
            def get_col(row, col):
                return row[col].values[0] if not row.empty and col in row.columns else ''
            top_usage = get_col(top_row, 'usage')
            bottom_usage = get_col(bottom_row, 'usage')
            foot_usage = get_col(foot_row, 'usage')
            top_type = get_col(top_row, 'articletype')
            bottom_type = get_col(bottom_row, 'articletype')
            foot_type = get_col(foot_row, 'articletype')
            top_season = get_col(top_row, 'season')
            bottom_season = get_col(bottom_row, 'season')
            foot_season = get_col(foot_row, 'season')
            # Get image links from images_df using exact filename match
            print(f"Looking for images: {top_id}.jpg, {bottom_id}.jpg, {foot_id}.jpg")
            top_img_row = images_df[images_df['filename'] == f"{top_id}.jpg"]
            bottom_img_row = images_df[images_df['filename'] == f"{bottom_id}.jpg"]
            foot_img_row = images_df[images_df['filename'] == f"{foot_id}.jpg"]
            top_img = top_img_row['link'].values[0] if not top_img_row.empty else ''
            bottom_img = bottom_img_row['link'].values[0] if not bottom_img_row.empty else ''
            foot_img = foot_img_row['link'].values[0] if not foot_img_row.empty else ''
            print(f"Found images: {top_img}, {bottom_img}, {foot_img}")
            outfits.append({
                'top': {
                    'id': top_id,
                    'name': top_name,
                    'color': outfit['Topwear Color'],
                    'img': top_img,
                    'usage': top_usage,
                    'articletype': top_type,
                    'season': top_season
                },
                'bottom': {
                    'id': bottom_id,
                    'name': bottom_name,
                    'color': outfit['Bottomwear Color'],
                    'img': bottom_img,
                    'usage': bottom_usage,
                    'articletype': bottom_type,
                    'season': bottom_season
                },
                'foot': {
                    'id': foot_id,
                    'name': foot_name,
                    'color': outfit['Footwear Color'],
                    'img': foot_img,
                    'usage': foot_usage,
                    'articletype': foot_type,
                    'season': foot_season
                }
            })
        return render_template(
            'results.html',
            skin_tone=skin_name,
            skin_hex=skin_hex,
            skin_tone_color=skin_hex,
            outfits=outfits,
            image_file=file.filename,
            gender=gender,
            usage=usage
        )
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)