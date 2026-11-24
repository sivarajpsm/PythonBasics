
"""
File: app.py

Project: Python Quiz Application

Purpose:
    Provides the user interface using Streamlit.

Responsibilities:
    1. Connect to FastAPI.
    2. Retrieve quiz questions.
    3. Display questions and answer options.
    4. Collect user answers.
    5. Submit answers to FastAPI.
    6. Display the final quiz result.
"""

# --------------------------------------------------
# STEP 1: IMPORT REQUIRED LIBRARIES
# --------------------------------------------------

import streamlit as st
import requests


# --------------------------------------------------
# STEP 2: CONFIGURATION
# --------------------------------------------------

# Base URL of the FastAPI backend.
API_BASE_URL = "http://127.0.0.1:8000"


# --------------------------------------------------
# STEP 3: STREAMLIT PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Python Quiz Application",
    page_icon="📝",
    layout="centered"
)

st.title("Python Quiz Application")
st.write("Test your Python knowledge!")


# --------------------------------------------------
# STEP 4: FETCH QUESTIONS FROM FASTAPI
# --------------------------------------------------

try:

    response = requests.get(
        f"{API_BASE_URL}/questions",
        timeout=10
    )

    # Raise an error if the API returns an unsuccessful status.
    response.raise_for_status()

    # Convert JSON response into Python data.
    questions = response.json()

except requests.exceptions.RequestException as error:

    st.error("Unable to connect to the Quiz API.")
    st.write("Please make sure the FastAPI server is running.")
    st.caption(str(error))

    st.stop()


# --------------------------------------------------
# STEP 5: DISPLAY QUESTIONS AND COLLECT ANSWERS
# --------------------------------------------------

answers = {}

# A form groups all questions and submits them together.
with st.form("quiz_form"):

    st.subheader("Answer the following questions")

    for question in questions:

        question_id = question["id"]

        st.write(
            f"**Question {question_id}:** "
            f"{question['question']}"
        )

        # Display answer options.
        selected_answer = st.radio(
            "Choose your answer:",
            options=question["options"],
            index=None,
            key=f"question_{question_id}",
            label_visibility="collapsed"
        )

        # Store the selected answer.
        if selected_answer is not None:
            answers[question_id] = selected_answer

        st.divider()

    # Submit all answers together.
    submitted = st.form_submit_button("Submit Quiz")


# --------------------------------------------------
# STEP 6: SUBMIT ANSWERS TO FASTAPI
# --------------------------------------------------

if submitted:

    # Ensure the user has answered every question.
    if len(answers) != len(questions):

        st.warning("Please answer all questions before submitting.")

    else:

        try:

            response = requests.post(
                f"{API_BASE_URL}/submit-quiz",
                json={"answers": answers},
                timeout=10
            )

            response.raise_for_status()

            # Convert API response into Python dictionary.
            result = response.json()

            # Display final quiz result.
            st.success("Quiz submitted successfully!")

            st.subheader("Your Quiz Result")

            st.metric(
                "Score",
                f"{result['score']} / {result['total_questions']}"
            )

            st.metric(
                "Percentage",
                f"{result['percentage']}%"
            )

            st.subheader(f"Grade: {result['grade']}")

        except requests.exceptions.RequestException as error:

            st.error("Unable to submit the quiz.")
            st.caption(str(error))
