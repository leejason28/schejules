SCHEJULES

scheduling app intended for use by restaurants/food service businesses
assigns employees to shifts based on business needs and employee availability
shifts are assigned randomly and the user has to ability to increase the odds of a certain employee being assigned a shift

use:
update 'employees.txt' with all employees and whatever shifts they are unavailable for
    format: name,unavailable day,unavailable start-end
update 'priorities.txt' with all employees and their priorities - higher numbers signify higher priority
    format: name,priority
update 'shifts.txt' with all shifts that need to be fulfilled
    format: day,start-end

run 'python3 script.py' or 'python script.py' to create a 'schejule.txt' file with a filled-out schedule