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

    # List to hold definitions

    yes_list = []

    # Booleans for conditions that need to be met

    answer_found = False
    list_length = False
    out_of_questions = False

    # Variable for number of questions in the list

    num_of_questions = len(questions)

    # Variable for incrementing questions asked

    num_asked = 0

    # Iterate through questions in questions

    for question in questions:

        # Validate user input using inputChoice from pyInputPlus

        user_choice = pyip.inputChoice(["yes", "no"], f"Is the {file_name} you're thinking of {question}? ")

        # Increment number of questions asked

        num_asked += 1

        # If user choice is yes

        if user_choice == "yes":

            # Append list I created earlier

            yes_list.append(question)

        # Once appended list holds 2 facts it breaks the loop

        if len(yes_list) == 2:
            list_length = True
            break

        # If we run out of questions to ask it breaks the loop

        if num_asked == num_of_questions and len(yes_list) < 2:
            out_of_questions = True
            break

    # If application doesn't know what you were thinking it will ask you

    if out_of_questions is True:
        print(f"{name} I have run out of questions, I only had {num_of_questions}")
        key_to_append = pyip.inputStr(f"What {file_name} were you thinking of? ")

        # Ask user for description of item

        append_list(file_name, yes_list, questions, question_file)

        # If there isn't 2 descriptions for the item

        if len(yes_list) < 2:
            append_list(file_name, yes_list, questions, question_file)

        # Append the key and the value list

        add(a_dict, key_to_append, yes_list)

        # Write to file

        writing_file(file_name, a_dict)

        # Print an acknowledgement of appending key/value list

        closing(key_to_append, name)

        # Set boolean to true so it doesn't run code later

        answer_found = True

    # Iterates through value lists matches to keys (if there are multiple keys with the same list it will
    # iterate through them all until it gets the correct one

    if list_length is True:
        for key, value in a_dict.items():
            if value == yes_list:
                user_choice = pyip.inputChoice(["yes", "no"], f"Are you thinking of {key}? ")
                if user_choice == "yes":
                    print(f"It took me {num_asked} questions to guess what you were thinking!")
                    answer_found = True
                else:

                    # increment numbers of questions asked

                    num_asked += 1

    # If the value list is complete it will ask for a key to append

    if answer_found is False:
        key_to_append = pyip.inputStr(f"What {file_name} were you thinking of? ")

        # Adds the key and value list to the dictionary

        add(a_dict, key_to_append, yes_list)

        # Write to file

        writing_file(file_name, a_dict)

        # Prints a statement that key has been added and written

        closing(key_to_append, name)


#   **********************************************************
#                   Main Method
#   **********************************************************
def main():

    # Greet the user and get their name

    name = greet_user_get_name()

    # Checks if the application has been run before, if it has check if user has used it before
    # If it has not been run before it creates the files needed for application to run
    # If it has been run before and user is in the list of names it welcomes them back
    # If it has been run before and its a new user it adds them to the list and informs user

    file_exists("names", name)

    # Loops the game until the player no longer want's to play

    while play_again(name) == "yes":
        file_name = animals_vegetables("What category would you like to choose? (vegetable or animal) ")
        a_dict = reading_file(file_name)
        question_file = animal_vegetables_questions(file_name)
        questions = reading_file(question_file)
        question_user(a_dict, questions, name, file_name, question_file)

    # End of application thanks user for using application

    print(f"Thank you for using my application {name}!")


# Run main function

main()

# EOF

