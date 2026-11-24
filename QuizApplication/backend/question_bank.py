
"""
File: question_bank.py

Purpose:
    Maintains the quiz question bank.

Responsibilities:
    1. Store the default quiz questions.
    2. Return all questions for internal backend use.
    3. Retrieve an individual question using its ID.
    4. Return public questions without exposing correct answers.
    5. Validate a user's selected answer.

Important:
    Correct answers must remain on the backend.
    Never send correct_answer to the Streamlit frontend.
"""


# --------------------------------------------------
# STEP 1: QUESTION BANK
# --------------------------------------------------

# A list of dictionaries.
# Each dictionary represents one question.
#
# id             -> Unique question identifier
# question       -> Actual question
# options        -> Available answer choices
# correct_answer -> Correct answer (backend only)

questions = [
    {
        "id": 1,
        "question": "What is the capital of India?",
        "options": ["Chennai", "Mumbai", "New Delhi", "Bangalore"],
        "correct_answer": "New Delhi"
    },
    {
        "id": 2,
        "question": "Which programming language are we using?",
        "options": ["Java", "Python", "C#", "PHP"],
        "correct_answer": "Python"
    },
    {
        "id": 3,
        "question": "Which keyword is used to define a function in Python?",
        "options": ["function", "define", "def", "func"],
        "correct_answer": "def"
    },
    {
        "id": 4,
        "question": "Which data type stores True or False values?",
        "options": ["String", "Integer", "Boolean", "List"],
        "correct_answer": "Boolean"
    },
    {
        "id": 5,
        "question": "Which data structure stores key-value pairs?",
        "options": ["List", "Tuple", "Set", "Dictionary"],
        "correct_answer": "Dictionary"
    },
    {
        "id": 6,
        "question": "Which symbol is used for comments in Python?",
        "options": ["//", "#", "/*", "--"],
        "correct_answer": "#"
    },
    {
        "id": 7,
        "question": "Which method adds an item to the end of a list?",
        "options": ["add()", "insert()", "append()", "extend()"],
        "correct_answer": "append()"
    },
    {
        "id": 8,
        "question": "What is the output of len('Python')?",
        "options": ["5", "6", "7", "8"],
        "correct_answer": "6"
    },
    {
        "id": 9,
        "question": "Which keyword is used to import a Python module?",
        "options": ["include", "using", "import", "require"],
        "correct_answer": "import"
    },
    {
        "id": 10,
        "question": "Which loop is commonly used to iterate over a list?",
        "options": ["for", "switch", "do-while", "goto"],
        "correct_answer": "for"
    }
]


# --------------------------------------------------
# STEP 2: GET ALL QUESTIONS
# --------------------------------------------------

def get_all_questions():
    """
    Returns the complete question bank.

    Used internally by backend services.

    Note:
        This function includes correct answers.
        Do not expose its result directly to the frontend.
    """
    return questions


# --------------------------------------------------
# STEP 3: GET QUESTION BY ID
# --------------------------------------------------

def get_question_by_id(question_id):
    """
    Finds and returns a question using its unique ID.

    Args:
        question_id: Unique question identifier.

    Returns:
        Question dictionary if found.
        None if the question does not exist.
    """

    for question in questions:

        if question["id"] == question_id:
            return question

    return None


# --------------------------------------------------
# STEP 4: GET PUBLIC QUESTIONS
# --------------------------------------------------

def get_public_questions():
    """
    Returns questions without exposing correct answers.

    The frontend only needs:
        - id
        - question
        - options

    The correct_answer field must remain private.

    A new dictionary is created for each question so
    that the original question bank is not modified.
    """

    public_questions = []

    for question in questions:

        public_question = {
            "id": question["id"],
            "question": question["question"],
            "options": question["options"].copy()
        }

        public_questions.append(public_question)

    return public_questions


# --------------------------------------------------
# STEP 5: VALIDATE USER ANSWER
# --------------------------------------------------

def check_answer(question_id, selected_answer):
    """
    Checks whether the user's selected answer is correct.

    Args:
        question_id: ID of the question.
        selected_answer: Answer selected by the user.

    Returns:
        True  -> If the answer is correct.
        False -> If the answer is incorrect or question
                 ID does not exist.
    """

    question = get_question_by_id(question_id)

    # Check whether the question exists.
    if question is None:
        return False

    # Compare selected answer with the stored correct answer.
    return question["correct_answer"] == selected_answer
