if option == "Heart Disease Prediction":
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.subheader("Login to Continue")
        username = st.text_input("Username", placeholder="Enter Username")
        password = st.text_input("Password", type="password", placeholder="Enter Password")

        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
            else:
                st.error("❌Invalid credentials")
    else:
        st.subheader("Enter Patient Details")
        name = st.text_input("Patient Name", placeholder="Enter patient's full name")
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

        if st.button("Submit"):
            # Prepare the input data for prediction
            input_data = pd.DataFrame({
                'age': [age],
                'sex': [1 if sex == "Male" else 0],
                'cp': [cp],
                'trestbps': [trestbps],
                'chol': [chol],
                'fbs': [fbs],
                'restecg': [restecg],
                'thalach': [thalach],
                'exang': [exang],
                'oldpeak': [oldpeak],
                'slope': [slope],
                'ca': [ca],
                'thal': [thal]
            })

            # Preprocess the input data
            input_processed = process_pipeline.transform(input_data)

            # Make predictions using the models
            extra_trees_pred = extra_trees_model.predict(input_processed)[0]
            knn_pred = knn_model.predict(input_processed)[0]
            logistic_regression_pred = logistic_model.predict(input_processed)[0]

            # Average the predictions
            avg_pred = (extra_trees_pred + knn_pred + logistic _regression_pred) / 3

            result = "◻ Heart disease predicted, Please consult a Cardiologist" if avg_pred >= 0.5 else "◻ Person is healthy"
            st.success(result)

            values = {
                "Name": name,
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
            report_image = generate_image(values, result, "User  Input")
            st.image(report_image, caption='Heart Disease Prediction Report', use_column_width=True)

            # Add a download button for the report
            st.download_button(
                label="Download Report",
                data=report_image,
                file_name='heart_disease_prediction_report.png',
                mime='image/png'
            )
