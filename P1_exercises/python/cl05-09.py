names = input("enter names splitted by comma:\n")
names = names.split(",")

assignments = input("enter assignments splitted by comma:\n")
assignments = eval('[%s]' % assignments)

grades = input("enter grades splitted by comma:\n")
grades = eval('[%s]' % grades)


template = """
Hi %s,
This is a reminder that you have %s assignments left to submit before you can graduate. Your current grade is %s and can increase to %s if you submit all assignments before the due date.
"""

for name,assign,grade in zip(names, assignments, grades):
	potential = 2 * assign + grade
	print(template % (name,assign, grade, potential))