# StyleSense - AI Fashion Recommender

A modern, AI-powered fashion recommendation system that analyzes your skin tone and provides personalized outfit suggestions based on color theory and style preferences.

## Features

- **Smart Skin Tone Detection**: Advanced image analysis using OpenCV to determine your skin tone from uploaded photos
- **Personalized Color Recommendations**: Tailored color suggestions based on your detected skin tone using color theory
- **Complete Outfit Generation**: Creates full outfit combinations including topwear, bottomwear, and footwear
- **Modern UI**: Clean, responsive design with beautiful gradients and glassmorphism effects
- **Multiple Occasions**: Support for Casual, Formal, Ethnic, and Sports wear
- **Gender-Specific**: Recommendations tailored for Men and Women
- **Real-time Processing**: Instant analysis and recommendation generation

## How It Works

1. **Image Upload**: Users upload a photo (face, hand, or any clear skin area)
2. **Skin Tone Analysis**: The system analyzes the image using OpenCV to detect average skin tone
3. **Color Matching**: Based on your skin tone, it identifies the most flattering colors using color theory
4. **Outfit Generation**: Creates complete outfit combinations (top, bottom, footwear) from the fashion dataset
5. **Personalization**: Filters recommendations by gender and occasion preferences

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Fashion-App
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure you have the required data files:
   - `data/styles.csv` - Fashion dataset with product information (4.1MB)
   - `data/images.csv` - Product image metadata and links (5.0MB)

## Usage

1. Run the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Navigate to the upload page and:
   - Upload a photo of yourself (face, hand, or any clear skin area)
   - Select your gender (Men/Women)
   - Choose your preferred occasion (Casual/Formal/Sports/Ethnic)

4. Get personalized outfit recommendations with color-coordinated combinations!

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Image Processing**: OpenCV for skin tone detection
- **Data Analysis**: Pandas for dataset manipulation
- **Image Handling**: Pillow (PIL) for image processing
- **Frontend**: HTML5, CSS3 with modern styling
- **Styling**: Custom CSS with gradients, glassmorphism, and animations
- **Font**: Inter font family for modern typography

## Project Structure

```
Fashion-App/
├── app.py              # Main Flask application with skin tone detection and recommendation logic
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── data/              # Data files
│   ├── styles.csv     # Fashion dataset with product details (4.1MB)
│   └── images.csv     # Product image metadata and links (5.0MB)
├── static/            # Static files
│   └── uploads/       # User uploaded images storage
└── templates/         # HTML templates
    ├── home.html      # Landing page with features and navigation
    ├── index.html     # Upload and form page
    └── results.html   # Results display page
```

## Key Features

### Skin Tone Detection
- Analyzes uploaded images using OpenCV
- Maps detected colors to 11 predefined skin tone categories
- Provides personalized color recommendations based on color theory

### Outfit Generation
- Generates complete outfit combinations (topwear, bottomwear, footwear)
- Ensures color coordination between outfit pieces
- Filters by gender, occasion, and season preferences

### Modern UI/UX
- Responsive design that works on all devices
- Beautiful gradient backgrounds with glassmorphism effects
- Smooth animations and hover effects
- Consistent design language across all pages

## Data Sources

The application uses a comprehensive fashion dataset containing:
- Product information (name, category, color, usage, season)
- Image metadata and links
- Gender-specific styling data
- Multiple occasion categories

## Contributing

Feel free to submit issues and enhancement requests! This project is open to contributions for:
- Improved skin tone detection algorithms
- Enhanced outfit recommendation logic
- UI/UX improvements
- Additional features and functionality

## License

This project is open source and available under the MIT License. 