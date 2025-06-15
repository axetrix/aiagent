import json


def run_quiz():
    with open("test/questions.json", "r") as f:
        questions = json.load(f)

    score = 0
    for i, q in enumerate(questions):
        print(f"\nQuestion {i + 1}: {q['question']}")
        for j, option in enumerate(q["options"]):
            print(f"{j + 1}. {option}")

        while True:
            try:
                answer = int(input("Your answer (1-4): "))
                if 1 <= answer <= 4:
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        if q["options"][answer - 1] == q["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct answer is: {q['answer']}")

    print(f"\nQuiz complete! Your score: {score}/{len(questions)}")


if __name__ == "__main__":
    run_quiz()
