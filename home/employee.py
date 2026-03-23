#Justin-Kenneth Denault
#261296919

import utils

MIN_AGE = 0
MAX_AGE = 120
VALID_GENDERS = ['m', 'f', 'x']
VALID_EDUCATION_LEVELS = ['none','high school','bachelors','masters','phd']

#2

#2.1.1
class Employee:
    """
    A class to represent an employee with personal and professional details.

    Attributes:
        name (str): Employee's full name.
        age (int): Employee's age, must be between MIN_AGE and MAX_AGE
                   inclusive.
        gender (str): Employee's gender; must be in VALID_GENDERS.
        education (str): Highest education level; must be in 
                         VALID_EDUCATION_LEVELS.
        prev_jobs (str): String representation of previous jobs, 
                         separated by '-'.
        skills (str): String representation of skills, separated by '-'.
        cur_job (str or None): Current job title, or None if unemployed.
    """

#2.1.2.1
    def __init__(self, name, age, gender, education, prev_jobs,
                 skills, cur_job=None):
        """ (Employee, str, int, str, str, str, str, str or None) -> None

        Initialize a new Employee instance with validated attributes. Validates age,
        gender, and education, normalizing gender and education to lowercase.

        >>> cl = Employee('James Bond', 35, 'M', 'high school', 'Spy',
        ...               'Martial artist-Knife mastery-spy-driver-card player')
        >>> cl.name
        'James Bond'

        >>> lbj = Employee('LeBron James', 39, 'm', 'bachelors', 'athlete-analyst',
        ...                'basketball-leadership-marketing', 'Philanthropist')
        >>> lbj.education
        'bachelors'

        >>> sc = Employee('Stephen Curry', 36, 'm', 'masters', 'athlete-entrepreneur',
        ...               'shooting-branding', 'Basketball Player')
        >>> sc.age
        36
        """
        self.name = name

        if not (MIN_AGE <= age <= MAX_AGE):
            raise ValueError("Age is not in the valid range [" + str(MIN_AGE) + "," + str(MAX_AGE) + "]")
        self.age = age

        gender_lower = gender.lower()
        if gender_lower not in VALID_GENDERS:
            raise ValueError("Gender must be one of: " + ', '.join(VALID_GENDERS))
        self.gender = gender_lower

        education_lower = education.lower()
        if education_lower not in VALID_EDUCATION_LEVELS:
            raise ValueError("Education must be one of: " +
                             ', '.join(VALID_EDUCATION_LEVELS))
        self.education = education_lower

        self.prev_jobs = prev_jobs
        self.skills = skills
        self.cur_job = cur_job

#2.1.2.2
    def __str__(self):
        """ (Employee) -> str

        Return a readable multi-line summary of the employee that prints
        normalized fields and lists.

        >>> cl = Employee('James Bond', 35, 'M', 'high school', 'Spy',
        ...               'Martial artist-Knife mastery-spy-driver-card player')
        >>> print(cl)
        Name: James Bond
        Age: 35
        Gender: m
        Highest education: high school
        Skills: ['martial artist', 'knife mastery', 'spy', 'driver', 'card player']
        Previous jobs: ['spy']
        Current job: None

        >>> mj = Employee('Michael Jordan', 61, 'm', 'bachelors', 'athlete-owner',
        ...               'basketball-business-strategy', 'NBA Owner')
        >>> print(mj)
        Name: Michael Jordan
        Age: 61
        Gender: m
        Highest education: bachelors
        Skills: ['basketball', 'business', 'strategy']
        Previous jobs: ['athlete', 'owner']
        Current job: NBA Owner

        >>> kd = Employee('Kevin Durant', 35, 'm', 'none', 'athlete',
        ...               'scoring-business-investing', 'Basketball Player')
        >>> print(kd)
        Name: Kevin Durant
        Age: 35
        Gender: m
        Highest education: none
        Skills: ['scoring', 'business', 'investing']
        Previous jobs: ['athlete']
        Current job: Basketball Player
        """
        result = "Name: " + self.name + "\n"
        result += "Age: " + str(self.age) + "\n"
        result += "Gender: " + self.gender + "\n"
        result += "Highest education: " + self.education + "\n"
        result += "Skills: " + str(utils.get_list(self.skills)) + "\n"
        result += "Previous jobs: " + str(utils.get_list(self.prev_jobs)) + "\n"
        result += "Current job: " + str(self.cur_job)
        return result

#2.1.2.3
    def add_prev_job(self, job):
        """ (Employee, str) -> None

        Append a new past job title to the employee's dash separated history
        in lowercase. If the employee already has previous jobs, appends with
        hyphen separator.

        >>> c1 = Employee('James Bond', 35, 'M', 'high school', 'Spy',
        ...               'Martial artist-Knife mastery-spy-driver-card player')
        >>> c1.add_prev_job('Security Analyst')
        >>> print(c1)
        Name: James Bond
        Age: 35
        Gender: m
        Highest education: high school
        Skills: ['martial artist', 'knife mastery', 'spy', 'driver', 'card player']
        Previous jobs: ['spy', 'security analyst']
        Current job: None

        >>> kobe = Employee('Kobe Bryant', 41, 'm', 'high school', 'athlete',
        ...                 'basketball-leadership', 'Producer')
        >>> kobe.add_prev_job('Oscar Winner')
        >>> kobe.prev_jobs
        'athlete-oscar winner'

        >>> giannis = Employee('Giannis Antetokounmpo', 29, 'm', 'high school',
        ...                    'athlete', 'basketball-philanthropy', 'NBA Player')
        >>> giannis.add_prev_job('Restaurant Owner')
        >>> giannis.add_prev_job('Investor')
        >>> giannis.prev_jobs
        'athlete-restaurant owner-investor'
        """
        if not isinstance(job, str):
            raise TypeError('Error in Class Employee: The input job should be a string')

        if self.prev_jobs:
            self.prev_jobs = self.prev_jobs + '-' + job.lower()
        else:
            self.prev_jobs = job.lower()

        return None
