
"""
File: quiz_service.py

Purpose:
    Contains the business logic for the quiz application.

Responsibilities:
    1. Calculate the user's quiz score.
    2. Calculate the percentage.
    3. Determine the grade using Grade Manager.
    4. Return the final quiz result.

Dependencies:
    question_bank.py
    grade_manager.py
"""


# --------------------------------------------------
# STEP 1: IMPORT REQUIRED FUNCTIONS
# --------------------------------------------------

# Import question bank functions.
from backend.question_bank import (
    get_all_questions,
    check_answer
)

# Reuse the existing Grade Manager implementation.
from grade_manager import get_grade


# --------------------------------------------------
# STEP 2: CALCULATE QUIZ SCORE
# --------------------------------------------------

def calculate_score(answers):
    """
    Calculates the total number of correct answers.

    Args:
        answers: Dictionary containing question IDs
                 and answers selected by the user.

        Example:
        {
            1: "New Delhi",
            2: "Python"
        }

    Returns:
        Total number of correct answers.
    """

    score = 0

    # Retrieve all questions from the question bank.
    questions = get_all_questions()

    # Iterate through every question.
    for question in questions:

        question_id = question["id"]

        # Retrieve the user's selected answer.
        # Returns None if the user did not answer.
        selected_answer = answers.get(question_id)

        # Validate the selected answer.
        if check_answer(question_id, selected_answer):

            # Increase score by one for each correct answer.
            score += 1

    return score


# --------------------------------------------------
# STEP 3: CALCULATE FINAL QUIZ RESULT
# --------------------------------------------------

def calculate_result(answers):
    """
    Calculates the complete quiz result.

    Processing:
        1. Get the total number of questions.
        2. Calculate the user's score.
        3. Calculate the percentage.
        4. Determine the grade using Grade Manager.
        5. Return the result as a dictionary.

    Args:
        answers: Dictionary containing user responses.

    Returns:
        Dictionary containing score, total questions,
        percentage and grade.
    """

    # Get the total number of questions.
    total_questions = len(get_all_questions())

    # Calculate the number of correct answers.
    score = calculate_score(answers)

    # Calculate percentage.
    percentage = (score / total_questions) * 100

    # Reuse the existing Grade Manager function.
    grade = get_grade(percentage)

    # Return the complete quiz result.
    return {
        "score": score,
        "total_questions": total_questions,
        "percentage": round(percentage, 2),
        "grade": grade
    }


# --------------------------------------------------
# VALIDATE QUIZ SUBMISSION
# --------------------------------------------------

def validate_answers(answers):
    """
    Validates the submitted quiz answers.

    Checks:
        1. All questions have been answered.
        2. No unknown question IDs are submitted.
        3. Selected answers belong to the question options.

    Returns:
        A list of validation errors.
        An empty list means the submission is valid.
    """

    validation_errors = []

    questions = get_all_questions()

    # Collect all valid question IDs.
    expected_ids = {question["id"] for question in questions}

    # Collect submitted question IDs.
    submitted_ids = set(answers.keys())

    # Check for unanswered questions.
    missing_ids = expected_ids - submitted_ids

    if missing_ids:
        validation_errors.append(
            f"Missing answers for question IDs: {sorted(missing_ids)}"
        )

    # Check for unknown question IDs.
    unknown_ids = submitted_ids - expected_ids

    if unknown_ids:
        validation_errors.append(
            f"Invalid question IDs: {sorted(unknown_ids)}"
        )

    # Check whether selected answers are valid options.
    for question in questions:

        question_id = question["id"]

        if question_id in answers:

            selected_answer = answers[question_id]

            if selected_answer not in question["options"]:
                validation_errors.append(
                    f"Invalid answer for question ID: {question_id}"
                )

    return validation_errors
