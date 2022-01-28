import numpy as np
import math
import pandas as pd
import os

#Currently works for Schoology Gradebook. Not optimized for MiStar Gradebook yet

def grade_mode(standard:list):
    """This function finds the mode of the grades in our standards based grading
    I created this function because the statistics.mode function will not return
    an error if there is no unique mode. This function will return None if there is
    no unique mode in the data set, which will help make sure that an actual mode is found."""
    count_0 = 0
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0

    # This counts each of the entries to find the total of each value
    for i in standard:
        if i == 0:
            count_0 += 1
        elif i == 1:
            count_1 += 1
        elif i == 2:
            count_2 += 1
        elif i == 3:
            count_3 += 1
        elif i == 4:
            count_4 += 1
    
    # This logic chain will return the mode, if there is one. Or return None if there isn't
    if count_0 > count_1 and count_0 > count_2 and count_0 > count_3 and count_0 > count_4:
        return 0
    elif count_1 > count_0 and count_1 > count_2 and count_1 > count_3 and count_1 > count_4:
        return 1
    elif count_2 > count_0 and count_2 > count_1 and count_2 > count_3 and count_2 > count_4:
        return 2
    elif count_3 > count_0 and count_3 > count_1 and count_3 > count_2 and count_3 > count_4:
        return 3
    elif count_4 > count_1 and count_4 > count_2 and count_4 > count_3 and count_4 > count_0:
        return 4
    else:
        return None



class Student:
    """Stores data from csv spreadsheet in this object for use later"""

    def __init__(self, first_name, last_name, model:list, solve:list, analyze:list):
        self.first_name = first_name
        self.last_name = last_name
        self.model = model
        self.solve = solve
        self.analyze = analyze
        self.letter_grade = None
        self.honors = False
        

    
class Final_Grades:
    """This class take a student object into it, and uses the list of standard scores
    from the student object to find their overall standard score using either the mode,
    average, and trends. Trend grade later?"""
    def __init__(self, student:Student):
        self.model_final = None
        self.solve_final = None
        self.analyze_final = None
        self.letter = None
    
    a = ([4,4,4], [4,4,3], [4,3,3], [3,3,3])
    b_plus = ([4,4,2], [4,3,2])
    b = ([4,2,2], [3,3,2])
    b_minus = ([3,2,2])
    c_plus = ([4,4,1], [4,3,1], [3,3,1])
    c = ([4,2,1], [3,2,1], [2,2,2])
    c_minus = ([2,2,1])
    d_plus = ([4,1,1], [3,1,1])
    d = ([2,1,1])
    d_minus = ([1,1,1])
    grades_list = [a, b_plus, b, b_minus, c_plus, c, c_minus, d_plus, d, d_minus]
    grade_letters = ["A", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"]



    # The following 3 functions will set their final scores to the appropriate property
    # once they are calculated

    def set_final_model(self, score):
        self.model_final = score
        return self.model_final

    def set_final_solve(self, score):
        self.solve_final = score
        return self.solve_final

    def set_final_analyze(self, score):
        self.analyze_final = score
        return self.analyze_final

    
    def calculate_final_grades(self, grades:list, standard:str):
        """Pass in the list of grades for a standard and that standard's name.
        The final grade for that standard will be set based on the mode or average,
        whichever one is higher, and using the trend to round up or down."""

        # Gets average
        avg = 0
        for i in grades:
            avg += i
        avg = avg/len(grades)

        # Gets mode
        final_mode = grade_mode(grades)

        # Gets trend using linear regression coefficient
        x = np.arange(0, len(grades))
        y = np.array(grades)
        z = np.polyfit(x, y, 1)

        # Sets final grade for modeling
        if standard == "modeling":    
            if z[0].round(4) > 0:
                if final_mode == None:
                    self.set_final_model(math.ceil(avg))
                elif avg>final_mode:
                    self.set_final_model(math.ceil(avg))
                elif avg<final_mode:
                    self.set_final_model(final_mode)
                elif avg == final_mode:
                    self.set_final_model(math.ceil(avg))
            # elif z[0].round(4) < 0:
            #     if final_mode == None:
            #         self.set_final_model(math.floor(avg))
            #     elif avg>final_mode:
            #         self.set_final_model(math.floor(avg))
            #     elif avg<final_mode:
            #         self.set_final_model(final_mode)
            #     elif avg == final_mode:
            #         self.set_final_model(math.floor(avg))
            else:
                if final_mode == None:
                    self.set_final_model(round(avg))
                elif avg>final_mode:
                    self.set_final_model(round(avg))
                elif avg<final_mode:
                    self.set_final_model(final_mode)
                elif avg == final_mode:
                    self.set_final_model(round(avg))

        # Sets final grade for Solve/Explain
        elif standard == "solve":
            if z[0].round(4) > 0:
                if final_mode == None:
                    self.set_final_solve(math.ceil(avg))
                elif avg>final_mode:
                    self.set_final_solve(math.ceil(avg))
                elif avg<final_mode:
                    self.set_final_solve(final_mode)
                elif avg == final_mode:
                    self.set_final_solve(math.ceil(avg))
            # elif z[0].round(4) < 0:
            #     if final_mode == None:
            #         self.set_final_solve(math.floor(avg))
            #     elif avg>final_mode:
            #         self.set_final_solve(math.floor(avg))
            #     elif avg<final_mode:
            #         self.set_final_solve(final_mode)
            #     elif avg == final_mode:
            #         self.set_final_solve(math.floor(avg))
            else:
                if final_mode == None:
                    self.set_final_solve(round(avg))
                elif avg>final_mode:
                    self.set_final_solve(round(avg))
                elif avg<final_mode:
                    self.set_final_solve(final_mode)
                elif avg == final_mode:
                    self.set_final_solve(round(avg))

        # Sets final grade for Analyze
        elif standard == "analyze":
            if z[0].round(4) > 0:
                if final_mode == None:
                    self.set_final_analyze(math.ceil(avg))
                elif avg>final_mode:
                    self.set_final_analyze(math.ceil(avg))
                elif avg<final_mode:
                    self.set_final_analyze(final_mode)
                elif avg == final_mode:
                    self.set_final_analyze(math.ceil(avg))
            # elif z[0].round(4) < 0:
            #     if final_mode == None:
            #         self.set_final_analyze(math.floor(avg))
            #     elif avg>final_mode:
            #         self.set_final_analyze(math.floor(avg))
            #     elif avg<final_mode:
            #         self.set_final_analyze(final_mode)
            #     elif avg == final_mode:
            #         self.set_final_analyze(math.floor(avg))
            else:
                if final_mode == None:
                    self.set_final_analyze(round(avg))
                elif avg>final_mode:
                    self.set_final_analyze(round(avg))
                elif avg<final_mode:
                    self.set_final_analyze(final_mode)
                elif avg == final_mode:
                    self.set_final_analyze(round(avg))

    def set_honors(self, student:Student):
        """This sets the honors property to True if they have achieved the requirements for honors"""
        student.honors = True
        return student.honors


    def get_letter_grade(self, student:Student):
        """This takes all of the overall standard scores from the 
        calculate_final_grades function and sorts them. It then compares it
        to the table of letter grades based on those scores to assign a letter grade"""
        student_grades = [self.model_final, self.solve_final, self.analyze_final]
        student_grades.sort(reverse=True)
        
        if student_grades == [4,4,4] or student_grades == [4,4,3]:
            self.set_honors(student)
        
        count = 0
        for i in self.grades_list:
            if student_grades in i or student_grades == i:
                self.letter = self.grade_letters[count]
                return self.letter
            count += 1
        self.letter = "E"
        return self.letter

    def final_scores(self, student:Student):
        """This function returns the students letter grade"""
        # Mostly just runs the above functions
        self.calculate_final_grades(student.model, "modeling")
        self.calculate_final_grades(student.solve, "solve")
        self.calculate_final_grades(student.analyze, "analyze")
        self.get_letter_grade(student)
        student.letter_grade = self.letter
        return student.letter_grade


# Finds path of where the folder is on this computer
path_name = os.getcwd()

# Finds the name of the file with the correct path for the rest of the program
for file in os.listdir(path_name):
    if file.endswith(".csv"):
        file_name = os.path.join(path_name, file)


        # Create a blank list for student objects to be passed into
        students = []

        # Creates the data sheet from a csv file
        grade_doc = pd.read_csv(file_name)

        # Blank lists for the number of grades in each standard
        model_columns = []
        solve_columns = []
        analyze_columns = []

        final_doc_columns = ["First Name", "Last Name"]

        # Loops through columns and appends them to the correct list to work for any number of standard grades
        for col in grade_doc:
            if ("model" in col.lower() and "unit" in col.lower()) or ("model" in col.lower() and "midterm" in col.lower()) or ("model" in col.lower() and "final" in col.lower()):
                model_columns.append(col)
                final_doc_columns.append(col)
            elif ("solve" in col.lower() and "unit" in col.lower()) or ("solve" in col.lower() and "midterm" in col.lower()) or ("model" in col.lower() and "final" in col.lower()):
                solve_columns.append(col)
                final_doc_columns.append(col)
            elif ("analyze" in col.lower() and "unit" in col.lower()) or ("analyze" in col.lower() and "midterm" in col.lower()) or ("model" in col.lower() and "final" in col.lower()):
                analyze_columns.append(col)
                final_doc_columns.append(col)

        # Create individual dataframes for references so the data can be added to a list.
        student_first_names = pd.DataFrame(grade_doc, columns=["First Name"])
        student_last_names = pd.DataFrame(grade_doc, columns=["Last Name"])
        grade_doc_model = pd.DataFrame(grade_doc, columns=model_columns)
        grade_doc_solve = pd.DataFrame(grade_doc, columns=solve_columns)
        grade_doc_analyze = pd.DataFrame(grade_doc, columns=analyze_columns)

        # Turns the individual dataframes into lists
        all_first_names = student_first_names.values.tolist()
        all_last_names = student_last_names.values.tolist()
        all_model_lists = grade_doc_model.values.tolist()
        all_solve_lists = grade_doc_solve.values.tolist()
        all_analyze_lists = grade_doc_analyze.values.tolist()

        # This takes the list of names and turns them into strings for reference later
        first_names = []
        for i in all_first_names:
            string = ''.join(i)
            first_names.append(string)

        last_names = []
        for i in all_last_names:
            string = ''.join(i)
            last_names.append(string)


        # Itterates through the rows of the files to make a list of all of the standard scores for every student
        for index, row in grade_doc.iterrows():
            model = all_model_lists[index]
            solve = all_solve_lists[index]
            analyze = all_analyze_lists[index]

            # Takes all of the information from the datasheet and creates a Student object
            a = Student(first_names[index], last_names[index], model, solve, analyze)

            # Adds the student object to a list of students
            students.append(a)

        # Blank list of all of the students letter grades and honors designations
        all_student_letter_grades = []
        all_student_honors = []

        # Itterates through all of the student objects, creates a Final Grade object, and uses it to
        # calculate their final letter grade and add it to the above list.
        for student in students:     
            grade_checker = Final_Grades(student)
            student_grade = grade_checker.final_scores(student)
            all_student_letter_grades.append(student_grade)
            
            if student.honors == True:
                all_student_honors.append("Yes")
            else:
                all_student_honors.append("")

        # Adds a new column to the document and writes in all of the student's letter grades
        df = pd.DataFrame(grade_doc, columns=final_doc_columns)
        df["Final Grade"] = all_student_letter_grades
        df["Honors?"] = all_student_honors

        new_file_base = os.path.splitext(file)[0]

        # Saves the csv file to the documents folder
        new_file_name = "".join([path_name, '\\', new_file_base, ' Final Grades.csv'])

        df.to_csv(new_file_name, index=False)