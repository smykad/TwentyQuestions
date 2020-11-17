#   **********************************************************
#       Name:  Doug Smyka
#       Application:  Twenty Questions
#       Date Created:  11.12.2020
#       Date Revised:  11.17.2020
#   **********************************************************
import pyinputplus as pyip
import ast
import pathlib


#   **********************************************************
#                   File Creation
#   **********************************************************
def file_creation():
    a_dict = {"bird": ["have feathers", "fly"],
              "dog": ["have fur", "bark"],
              "cat": ["have fur", "meow"]
              }
    a_questions = ["have feathers",
                   "fly", "have fur",
                   "bark", "meow"]
    v_dict = {"carrot": ["crunchy", "orange"],
              "celery": ["crunchy", "green"]}
    v_questions = ["crunchy",
                   "orange",
                   "green"]

    writing_file("animal", a_dict)
    writing_file("animal_questions", a_questions)
    writing_file("vegetable", v_dict)
    writing_file("vegetable_questions", v_questions)


#   **********************************************************
#                   Get User Name
#   **********************************************************
def greet_user_get_name():
    ret = pyip.inputStr("Welcome to 20 questions, what is your name? ")
    return ret


#   **********************************************************
#                   Check if returning user
#   **********************************************************
def file_exists(filename, name):
    f = pathlib.Path(f"{filename}.txt")
    if f.exists():
        ret = reading_file(filename)
        if name in ret:
            print(f"Welcome back {name}")
        else:
            print(f"It looks like this is your first time here {name}")
            ret.append(name)
            writing_file(filename, ret)
    else:
        print(f"Looks like this is your first time running the application {name}")
        names = [name]
        writing_file("names", names)
        file_creation()


#   **********************************************************
#                   Choose File to Open
#   **********************************************************
def animals_vegetables(prompt):
    ret = pyip.inputChoice(['animal', 'vegetable'], prompt)
    return ret


#   **********************************************************
#                   Choose Question File to Open
#   **********************************************************
def animal_vegetables_questions(filename):
    if filename == "animal":
        ret = "animal_questions"
    else:
        ret = "vegetable_questions"
    return ret


#   **********************************************************
#                   Append Questions List
#   **********************************************************
def append_list(file_name, yes_list, questions, question_file):
    user_response = pyip.inputStr(
        f"What is a word that would identify the {file_name} you are looking for? ")
    yes_list.append(user_response)
    questions.append(user_response)
    writing_file(question_file, questions)


#   **********************************************************
#                   Reading File
#   **********************************************************
def reading_file(filename):
    with open(f"{filename}.txt", "r") as f:
        data = f.read()
    ret = ast.literal_eval(data)
    return ret


#   **********************************************************
#                   Writing to File
#   **********************************************************
def writing_file(filename, a_dict):
    with open(f"{filename}.txt", "w+") as f:
        f.write(str(a_dict))


#   **********************************************************
#                   Printing Dictionary
#   **********************************************************
def print_dictionary_of_lists(a_dict):
    for key, value in a_dict.items():
        print(key, end=": ")
        iteration = range(len(value))
        limit = len(value)
        for i in iteration:
            if i < limit-1:
                print(f"{value[i]}", end=f", ")
            else:
                print(f"{value[i]}")


#   **********************************************************
#                   Append Dictionary
#   **********************************************************
def add(a_dict, key, value):
    a_dict[key] = value


#   **********************************************************
#                   Play Again
#   **********************************************************
def play_again(name):
    ret = pyip.inputChoice(["yes", "no"], f"{name} do you want to play? ")
    return ret


#   **********************************************************
#                   Closing Message
#   **********************************************************
def closing(key_to_append, name):
    print(f"I did not know about {key_to_append}, I have appended it to my memory and will "
          f"remember it next time {name}")


#   **********************************************************
#                   Question User
#   **********************************************************
def question_user(a_dict, questions, name, file_name, question_file):
    yes_list = []
    answer_found = False
    list_length = False
    out_of_questions = False
    num_of_questions = len(questions)
    num_asked = 0

    for question in questions:
        user_choice = pyip.inputChoice(["yes", "no"], f"Is the {file_name} you're thinking of {question}? ")
        num_asked += 1
        if user_choice == "yes":
            yes_list.append(question)
        if len(yes_list) == 2:
            list_length = True
            break
        if num_asked == num_of_questions and len(yes_list) < 2:
            out_of_questions = True
            break

    if out_of_questions is True:
        print(f"{name} I have run out of questions, I only had {num_of_questions}")
        key_to_append = pyip.inputStr(f"What {file_name} were you thinking of? ")
        append_list(file_name, yes_list, questions, question_file)
        if len(yes_list) < 2:
            append_list(file_name, yes_list, questions, question_file)
        add(a_dict, key_to_append, yes_list)
        writing_file(file_name, a_dict)
        closing(key_to_append, name)
        answer_found = True

    if list_length is True:
        for key, value in a_dict.items():
            if value == yes_list:
                user_choice = pyip.inputChoice(["yes", "no"], f"Are you thinking of {key}? ")
                if user_choice == "yes":
                    print(f"It took me {num_asked} questions to guess what you were thinking!")
                    answer_found = True

    if answer_found is False:
        key_to_append = pyip.inputStr(f"What {file_name} were you thinking of? ")
        add(a_dict, key_to_append, yes_list)
        writing_file(file_name, a_dict)
        closing(key_to_append, name)


#   **********************************************************
#                   Main Method
#   **********************************************************
def main():

    name = greet_user_get_name()
    file_exists("names", name)
    while play_again(name) == "yes":
        file_name = animals_vegetables("What category would you like to choose? (vegetable or animal) ")
        a_dict = reading_file(file_name)
        question_file = animal_vegetables_questions(file_name)
        questions = reading_file(question_file)
        question_user(a_dict, questions, name, file_name, question_file)

    print(f"Thank you for using my application {name}!")


main()

# EOF

