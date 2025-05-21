import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report

# Sidebar Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "DDoS Classification"])

if menu == "Home":
    st.title("Welcome to the DDoS Attack Prediction App")
    st.write("Use this application to classify and predict DDoS attack types based on input features.")
    st.write("Navigate to 'DDoS Classification' from the sidebar to begin.")

elif menu == "DDoS Classification":
    st.title("DDoS Attack Classification & Prediction")
    
    uploaded_file = st.file_uploader("Upload DDoS Attack Dataset (CSV)", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Dataset Preview:")
        st.write(df.head())
        
        # Handle missing values
        df = df.dropna()  # Dropping rows with missing values
        
        # Basic Data Summary
        st.subheader("Data Summary")
        st.write(df.describe())
        st.write("Class Distribution:")
        st.bar_chart(df.iloc[:, -1].value_counts())
        
        # Feature Selection (Selecting only first 6 features for input)
        X = df.iloc[:, :6]  # Taking first 6 columns as features
        y = df.iloc[:, -1]
        
        # Impute missing values
        imputer = SimpleImputer(strategy='mean')
        X = imputer.fit_transform(X)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        st.subheader("Model Performance")
        st.write(f"Accuracy: {accuracy:.2f}")
        st.text("Classification Report:")
        st.text(classification_report(y_test, y_pred))
        
        # Prediction Section
        st.subheader("Make a Prediction")
        input_data = []
        for col in df.columns[:6]:
            val = st.number_input(f"{col}", float(df[col].min()), float(df[col].max()))
            input_data.append(val)
        
        if st.button("Predict DDoS Attack Type"):
            prediction = model.predict([input_data])
            st.write(f"Predicted Attack Type: {prediction[0]}")