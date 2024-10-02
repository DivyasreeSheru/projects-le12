import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
# CSV file path
csv_file_path = r""C:\Users\divya\OneDrive\Desktop\apolo\div.csv"


# Function to generate an image with the prediction report
def generate_image(values, result, name):
    # Create an image with whitish blue background
    img = Image.new('RGB', (600, 800), color=(224, 247, 250))  # Whitish blue background
    d = ImageDraw.Draw(img)

    # Load a font (you may need to specify the path to the font on your machine)
    try:
        font = ImageFont.truetype("arialbd.ttf", 18)  # Use bold font for heading
        large_font = ImageFont.truetype("arialbd.ttf", 50)  # Use bold font for large text
    except:
        font = ImageFont.load_default()
        large_font = ImageFont.load_default()

    # Draw a heart shape in the background
    heart_color = (255, 182, 193)  # Light red color for heart (light pink)
    heart_points = [(300, 220), (350, 170), (400, 220), (400, 280), (300, 380), (200, 280), (200, 220)]
    d.polygon(heart_points, fill=heart_color)

    # Add hospital symbol (+) at the top
    d.text((250, 20), "+", font=large_font, fill=(0, 0, 0))  # Black hospital symbol

    # Title
    title_text = "Heart Disease Prediction Report"
    underline_text = "-" * 50

    # Calculate bounding boxes for centering
    title_bbox = d.textbbox((0, 0), title_text, font=font)
    underline_bbox = d.textbbox((0, 0), underline_text, font=font)

    # Calculate x positions for centering
    title_x = (img.width - (title_bbox[2] - title_bbox[0])) // 2
    underline_x = (img.width - (underline_bbox[2] - underline_bbox[0])) // 2

    # Add centered title and underline
    d.text((title_x, 100), title_text, font=font, fill=(0, 0, 0))  # Centered title in bold
    d.text((underline_x, 130), underline_text, font=font, fill=(0, 0, 0))  # Centered underline

    # Add patient values
    y_text = 160
    for key, value in values.items():
        d.text((10, y_text), f"{key}: {value}", font=font, fill=(0, 0, 0))  # Black text
        y_text += 30

    # Add result
    d.text((10, y_text), f"Result: {result}", font=font, fill=(0, 0, 0))
    y_text += 40

    # Add date, time, and name
    now = datetime.now()
    d.text((10, y_text), f"Date: {now.strftime('%Y-%m-%d')}", font=font, fill=(0, 0, 0))
    d.text((10, y_text + 30), f"Time: {now.strftime('%H:%M:%S')}", font=font, fill=(0, 0, 0))
    d.text((10, y_text + 60), f"Report Generated by: {name}", font=font, fill=(0, 0, 0))

    # Save image to a bytes buffer
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return img_buffer
# Login function
def login(username, password):
    return username == "heartdisease" and password == "heart@123"


# Main app
def main():
    st.title("🌟 Heart Disease Prediction 🌟")

    # Use inline CSS to set the background color and styles
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #ADD8E6;  /* Set background color to light blue */
            position: relative;
            height: 100vh;  /* Full height to cover the screen */
            color: black;  /* Set text color to dark black */
            font-weight: bold;  /* Make all text bold */
        }

        /* Add a large dark red "+" symbol in the background */
        .plus-symbol {
           position: fixed;
           top: 50%;
           left: 50%;
           transform: translate(-50%, -50%);
           font-size: 850px;  /* Size of the + symbol */
           font-weight: bold;
           color: rgba(255, 0, 0, 0.1);  /* Dark red color for the symbol */
           z-index: 1;  /* Ensure it's behind other elements */
        }

        /* Custom styles for the title */
        h1, h2, h3, h4, h5, h6 {
            color: black;  /* Set all headings to dark black */
            font-weight: bold;  /* Make all headings bold */
        }

        /* Custom styles for text input */
        .stTextInput {
            border-radius: 10px;
        }

        /* Custom styles for buttons */
        .stButton > button {
            background-color: #4CAF50;  /* Green background for buttons */
            color: white;  /* Text color for buttons */
            border-radius: 5px;
        }
        </style>

        <div class="plus-symbol">+</div>  <!-- Plus symbol -->
        """,
        unsafe_allow_html=True
    )

    # Initial login page
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.subheader("🔑 Login to Continue")
        username = st.text_input("Username", placeholder="Enter Username")
        password = st.text_input("Password", type="password", placeholder="Enter Password")

        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.success("🎉 Logged in successfully!")
            else:
                st.error("❌ Invalid credentials")

    # Once logged in
    if st.session_state.logged_in:
        st.subheader("🏥 Enter Patient Details")

        # Input fields
        age = st.number_input("Age", min_value=1, max_value=100)
        sex = st.selectbox("Sex", ["Male", "Female"])
        cp = st.number_input("Chest Pain Type (cp)", min_value=0.0, max_value=5.0)
        trestbps = st.number_input("Resting Blood Pressure (trestbps)", min_value=94.0, max_value=200.0)
        chol = st.number_input("Serum Cholesterol (chol)", min_value=126.0, max_value=417.0)
        fbs = st.number_input("Fasting Blood Sugar (fbs)", min_value=0.0, max_value=3.0)
        restecg = st.number_input("Resting ECG (restecg)", min_value=0.0, max_value=2.0)
        thalach = st.number_input("Max Heart Rate (thalach)", min_value=71.0, max_value=192.0)
        exang = st.number_input("Exercise Induced Angina (exang)", min_value=0.0, max_value=1.0)
        oldpeak = st.number_input("ST Depression (oldpeak)", min_value=0.0, max_value=5.6)
        slope = st.number_input("Slope of Peak Exercise (slope)", min_value=0.0, max_value=2.0)
        ca = st.number_input("Major Vessels (ca)", min_value=0.0, max_value=4.0)
        thal = st.number_input("Thalassemia (thal)", min_value=1.0, max_value=3.0)

        # Load the CSV file for actual predictions
        df = pd.read_csv(csv_file_path)

        # Use input values to match and fetch predictions from the CSV
        filtered_data = df[(df['age'] == age) &
                           (df['sex'] == (1 if sex == "Male" else 0)) &
                           (df['cp'] == cp)]

        if not filtered_data.empty:
            # Get prediction values from the CSV
            extra_trees_pred = filtered_data['Extra Trees Pred Target'].values[0]
            knn_pred = filtered_data['KNN Pred Target'].values[0]
            logistic_regression_pred = filtered_data['Logistic Regression Pred Target'].values[0]

            # Calculate average prediction target
            avg_pred = (extra_trees_pred + knn_pred + logistic_regression_pred) / 3

            if st.button("Submit"):
                if avg_pred >= 0.5:
                    result = "❤️ Heart disease predicted"
                    st.success(result)
                else:
                    result = "💪 Person is healthy"
                    st.success(result)

                # Store values
                values = {
                    "Age": age,
                    "Sex": sex,
                    "Chest Pain Type (cp)": cp,
                    "Resting Blood Pressure (trestbps)": trestbps,
                    "Serum Cholesterol (chol)": chol,
                    "Fasting Blood Sugar (fbs)": fbs,
                    "Resting ECG (restecg)": restecg,
                    "Max Heart Rate (thalach)": thalach,
                    "Exercise Induced Angina (exang)": exang,
                    "ST Depression (oldpeak)": oldpeak,
                    "Slope of Peak Exercise (slope)": slope,
                    "Major Vessels (ca)": ca,
                    "Thalassemia (thal)": thal
                }

                # Generate and display report image
                report_image = generate_image(values, result, "xyz")
                st.image(report_image, caption='Heart Disease Prediction Report', use_column_width=True)
        else:
            st.error("❌ No matching data found for the entered values.")


# Run the main function
if __name__ == "__main__":
    main()
