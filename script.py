import sys
import csv
import datetime
import random



# needs to read from 'shifts' file - which has shift information
# needs to read from 'employees' file - which has employee information
# needs to write new CSV file - schedule output for given week
def main():

    # read employee (un)availability
    employees = {}
    with open('employees.txt') as employees_file:
        employees_reader = csv.reader(employees_file)
        line_index = 0
        for row in employees_reader:
            if line_index > 0:
                unavailable_date_time = " ".join(row[1:])
                if row[0] in employees.keys():
                    employees[row[0]].append(unavailable_date_time)
                else:
                    employees[row[0]] = [unavailable_date_time]
            line_index += 1
    
    # read employee priorities
    priorities = {}
    with open('priorities.txt') as priorities_file:
        priorities_reader = csv.reader(priorities_file)
        line_index = 0
        for row in priorities_reader:
            if line_index > 0:
                priorities[row[0]] = row[1]
            line_index += 1
    
    # read shift necesseties
    shifts = []
    with open('shifts.txt') as shifts_file:
        shifts_reader = csv.reader(shifts_file)
        line_index = 0
        for row in shifts_reader:
            if line_index > 0:
                shifts.append(" ".join(row))
            line_index += 1

    # {shift: [list of available employees]}
    possible_shifts = {}
    for shift in shifts:
        possible_shifts[shift] = []
        for employee in employees.keys():
            unavailabilities = employees[employee]
            if available(unavailabilities, shift):
                possible_shifts[shift].append(employee)

    # output the assigned shifts - in form of csv/excel file
        # could also include for which shifts there is another possible employee to work
        # should also include for which shifts there is no possible employee to work
        # return blank for a given shift if no option found
    output = schejules(possible_shifts, employees, priorities)
    
    ordered_output = []
    for shift in shifts:
        shift_covered = False
        for out in output:
            if out.split(" ")[0] + " " + out.split(" ")[1] == shift:
                shift_covered = True
                ordered_output.append(out)
        if shift_covered == False:
            ordered_output.append(" ")

    with open("schejule.txt", "w") as out_file:
        out_file.write("day,shift,employee \n")
        out_file.writelines(" \n".join(ordered_output))

    print("Schejuled.")

    
# reduces the possible_shifts into a possible schedule
# employees should be limited to 1 shift per day - possible_shifts dictionary should change when a shift gets assigned
# gpt for ideas
# output should be in format [shift: employee, ...]
def schejules(possible_shifts, employees, priorities, schejule=[]):
    if all_shifts_assigned(possible_shifts):
        return schejule
    else:
        shift = select_shift(possible_shifts)
        employee = select_employee(possible_shifts, shift, employees, priorities)
        schejule.append(" ".join([shift, employee]))
        popped = possible_shifts.pop(shift)
        remove_employee(possible_shifts, shift, employee)
        if all_shifts_assigned(schejules(possible_shifts, employees, priorities, schejule)):
            return schejule
        possible_shifts[shift] = popped
        possible_shifts[shift].append(employee)
    return schejule

# select next shift to assign - can choose shift with least availabile employees
#returns last shift for now - which technically prioritizes weekends
def select_shift(possible_shifts):
    min = list(possible_shifts.keys())[0]
    for shift in possible_shifts.keys():
        if len(possible_shifts[shift]) <= len(possible_shifts[min]):
            min = shift
    return min

# select employee on random that selects employee based off their weighted priorities
def select_employee(possible_shifts, shift, employees, priorities):
    availables = []
    for employee in possible_shifts[shift]:
        if available(employees[employee], shift):
            availables.append(employee)
        if employee in priorities.keys():
            for i in range(int(priorities[employee])):
                availables.append(employee)
    return random.choice(availables)

# checks if unavailabilities includes this particular shift
# returns true if shift is able to be fulfilled
def available(unavailabilities, shift):
    if unavailabilities == ['None']:
        return True
    shift_dt = shift.split()
    for unavailable in unavailabilities:
        unavailable_dt = unavailable.split()
        if shift_dt[0] == unavailable_dt[0]:
            shift_range = shift_dt[1].split("-")
            shift_start = datetime.datetime.strptime(shift_range[0], '%H:%M').time()
            shift_end = datetime.datetime.strptime(shift_range[1], '%H:%M').time()
            unavailable_range = unavailable_dt[1].split("-")
            unavailable_start = datetime.datetime.strptime(unavailable_range[0], '%H:%M').time()
            unavailable_end = datetime.datetime.strptime(unavailable_range[1], '%H:%M').time()
            if unavailable_end <= shift_start:
                return True
            elif unavailable_end >= shift_start and unavailable_start >= shift_end:
                return True
            elif unavailable_start >= shift_end:
                return True
            elif unavailable_start <= shift_end and unavailable_end <= shift_start:
                return True
            else:
                return False
    return True

def all_shifts_assigned(possible_shifts):
    if len(possible_shifts) == 0:
        return True
    return False

def remove_employee(possible_shifts, shift, employee):
    for possible_shift in possible_shifts.keys():
        if shift.split(" ")[0] == possible_shift.split(" ")[0]:
            possible_shifts[possible_shift].remove(employee)



# run script
main()