
"""
File: backend/main.py

Project: Python Quiz Application

Purpose:
    Main entry point for the FastAPI backend.

Responsibilities:
    1. Initialize the FastAPI application.
    2. Provide a welcome endpoint.
    3. Provide an API health-check endpoint.
    4. Retrieve all public quiz questions.
    5. Accept quiz submissions.
    6. Return the calculated quiz result.

Dependencies:
    - FastAPI
    - Pydantic
    - question_bank.py
    - quiz_service.py
"""


# --------------------------------------------------
# STEP 1: IMPORT REQUIRED LIBRARIES
# --------------------------------------------------

from fastapi import FastAPI, HTTPException

from backend.quiz_service import (
    calculate_result,
    validate_answers
)

from pydantic import BaseModel

# Import existing question bank functionality.
from backend.question_bank import get_public_questions

# Import existing quiz business logic.
from backend.quiz_service import calculate_result


# --------------------------------------------------
# STEP 2: INITIALIZE FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Quiz Application API",
    description="Backend APIs for the Python Quiz Application",
    version="1.0.0"
)


# --------------------------------------------------
# STEP 3: DEFINE REQUEST MODEL
# --------------------------------------------------

class QuizSubmission(BaseModel):
    """
    Defines the request structure for quiz submission.

    Expected JSON:
    {
        "answers": {
            "1": "New Delhi",
            "2": "Python"
        }
    }

    Pydantic validates the incoming request data.
    Question IDs are represented as integers internally.
    """

    answers: dict[int, str]


# --------------------------------------------------
# STEP 4: HOME API
# --------------------------------------------------

@app.get("/")
def home():
    """
    Welcome endpoint.

    HTTP Method: GET
    URL: /

    Returns a welcome message.
    """

    return {
        "message": "Welcome to Quiz Application API"
    }


# --------------------------------------------------
# STEP 5: HEALTH CHECK API
# --------------------------------------------------

@app.get("/health")
def health_check():
    """
    Checks whether the API is running.

    HTTP Method: GET
    URL: /health
    """

    return {
        "status": "Healthy"
    }


# --------------------------------------------------
# STEP 6: GET ALL QUIZ QUESTIONS
# --------------------------------------------------

@app.get("/questions")
def get_questions():
    """
    Retrieves all quiz questions without correct answers.

    HTTP Method: GET
    URL: /questions

    Uses get_public_questions() to prevent exposing
    correct answers to the frontend.
    """

    return get_public_questions()


# --------------------------------------------------
# STEP 7: SUBMIT QUIZ ANSWERS
# --------------------------------------------------

@app.post("/submit-quiz")
def submit_quiz(submission: QuizSubmission):

    answers = submission.answers

    # Validate submitted answers.
    errors = validate_answers(answers)

    # Reject invalid submissions.
    if errors:
        raise HTTPException(
            status_code=400,
            detail=errors
        )

    # Calculate the final result.
    result = calculate_result(answers)

    return result
