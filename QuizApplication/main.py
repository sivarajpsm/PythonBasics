
from backend.question_bank import get_public_questions
from backend.quiz_service import calculate_result

# Step 1: Get questions safe to display in frontend.
public_questions = get_public_questions()

print("Total Questions:", len(public_questions))
print("First Question:", public_questions[0])


# Step 2: Simulate answers submitted by a user.
answers = {
    1: "New Delhi",
    2: "Python",
    3: "def",
    4: "Boolean",
    5: "Dictionary",
    6: "#",
    7: "append()",
    8: "6",
    9: "import",
    10: "for"
}


# Step 3: Calculate the final result.
result = calculate_result(answers)

print("\nFinal Quiz Result")
print("-----------------")
print("Score:", result["score"])
print("Total:", result["total_questions"])
print("Percentage:", result["percentage"])
print("Grade:", result["grade"])
