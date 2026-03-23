# Justin-Kenneth Denault
# 261296919

import network
import utils
from employee import Employee
from job import Job

EDUCATION_LEVELS = ['none', 'high school', 'bachelors', 'masters', 'phd']
SKILLS_WEIGHT = 0.8
EDUCATION_WEIGHT = 0.2
NO_EMPLOYEE_SCORE = 0.0
ROUNDING_PRECISION = 2
INITIAL_BEST_SCORE = -1.0


# 2.3

# 2.3.1
class Company:
    """A class to represent a company at the career fair.

    Attributes:
        name (str): Company name.
        location (str): Company location.
        employees (list of Employee): List of employees currently at
                                      the company.
        job_csv (str or None): Path to CSV file with job postings.
        jobs (list of Job): List of job postings loaded from CSV.
    """

    # 2.3.1.1
    def __init__(self, name, location, employees, jobs_csv=None):
        """ (Company, str, str, list of Employee, str or None)--> None

        Initialize a new Company with name, location, employees, and
        optionally load jobs from a CSV file using network.create_job_list().

        >>> comp = Company("nova cafe", "toronto", [], "jobs.csv")
        >>> comp.name
        'nova cafe'
        >>> comp.location
        'toronto'

        >>> nba_company = Company("NBA Team", "Los Angeles", [])
        >>> nba_company.name
        'NBA Team'

        >>> big_company = Company("Big Corp", "New York", [], "jobs_test.csv")
        >>> big_company.jobs
        []
        """
        self.name = name
        self.location = location
        self.employees = employees
        self.job_csv = jobs_csv
        self.jobs = []

        if jobs_csv:
            self.jobs = network.create_job_list(jobs_csv)

    # 2.3.1.2
    def __str__(self):
        """ (Company)--> str

        Return a multi-line summary with company name, location, number of
        employees,and number of available jobs for quick booth status boards.

        >>> comp = Company("Happy Tails Academy", "Montreal", [], "jobs.csv")
        >>> print(comp)
        Name: Happy Tails Academy
        Location: Montreal
        Number of employees: 0
        Number of available jobs: 3

        >>> nba_co = Company("NBA Franchise", "Chicago", [])
        >>> print(nba_co)
        Name: NBA Franchise
        Location: Chicago
        Number of employees: 0
        Number of available jobs: 0

        >>> big_co = Company("Tech Giant", "San Francisco", [Employee("Alex", 
        ...                   30, 'm','bachelors', '', '', None)],
        ...                  "jobs_test.csv")
        >>> print(big_co)
        Name: Tech Giant
        Location: San Francisco
        Number of employees: 1
        Number of available jobs: 3
        """
        num_employees = len(self.employees)
        num_jobs = len(self.jobs)

        result = "Name: " + self.name + "\n"
        result += "Location: " + self.location + "\n"
        result += "Number of employees: " + str(num_employees) + "\n"
        result += "Number of available jobs: " + str(num_jobs)

        return result

# 2.3.1.3
    def skills_similarity(self, job, employee):
        """ (Company, Job, Employee) -> float

        Calculate the cosine similarity between an employee's skills and a
        job's keywords. Both are tokenized and converted to count vectors 
        using a shared vocabulary.

        >>> comp = Company("Happy Tails Academy", "Montreal", [], "jobs.csv")
        >>> job = Job("Trainer", "entry-level-dog-trainer", 43000)
        >>> emp1 = Employee("James", 0, "M", "high school", "Spy",
        ...                 "pet-trainer")
        >>> comp.skills_similarity(job, emp1)
        0.35

        >>> nba_job = Job("Coach", "leadership-training-strategy", 100000)
        >>> player = Employee("LeBron", 39, 'm', 'high school', 'player',
        ...                   'leadership-basketball-strategy')
        >>> nba_co = Company("NBA Team", "LA", [])
        >>> nba_co.skills_similarity(nba_job, player)
        0.67

        >>> tech_job = Job("Developer", "python-java-sql", 80000)
        >>> dev = Employee("Sarah", 30, 'f', 'bachelors', 'intern',
        ...                'python-sql')
        >>> tech_co = Company("Tech Corp", "SF", [])
        >>> tech_co.skills_similarity(tech_job, dev)
        0.82
        """
        emp_tokens = utils.get_list(employee.skills) #turns to formatted list
        job_tokens = utils.get_list(job.keywords)

        vocab = utils.make_vocabulary([emp_tokens, job_tokens])

        emp_vector = utils.vectorize(emp_tokens, vocab) #turns into vectors
        job_vector = utils.vectorize(job_tokens, vocab)

        return utils.cosine_similarity(emp_vector, job_vector)

    # 2.3.1.4
    def education_similarity(self, employee):
        """ (Company, Employee) -> float

        Calculate education similarity between an employee and the company's
        existing employees. Uses one-hot encoding for education levels and
        zeros out company counts below employee's level.

        >>> comp = Company("Happy Tails Academy", "Montreal", [], "jobs.csv")
        >>> job = comp.jobs[0]
        >>> empl = Employee("James", 0, "M", "high school", "Spy",
        ...                 "pet-trainer")
        >>> comp.jobs[1].employee = empl
        >>> empl = Employee("Jamy", 45, "M", "phd", "Spy", "pet-trainer")
        >>> comp.jobs[0].employee = empl
        >>> empl2 = Employee("Martin", 0, "M", "high school", "vet",
        ...                  "pet-veterenarian")
        >>> comp.education_similarity(empl2)
        0.71

        >>> nba_co = Company("NBA Team", "LA", [])
        >>> player = Employee("Kobe", 41, 'm', 'high school', 'player',
        ...                   'scoring')
        >>> nba_co.education_similarity(player)
        0.0

        >>> mixed_co = Company("Mixed", "NY", [Employee("A", 30, 'm', 
        ...                    'bachelors','', '', None), Employee("B", 35,
        ...                    'f', 'masters', '', '', None)])
        >>> new_emp = Employee("C", 40, 'f', 'masters', '', '', None)
        >>> mixed_co.education_similarity(new_emp)
        0.0
        """

        employee_vector = [0] * 5 #creates fix domain
        for i in range(len(EDUCATION_LEVELS)):
            if employee.education == EDUCATION_LEVELS[i]:
                employee_vector[i] = 1

        company_vector = [0] * 5
        for job in self.jobs:
            if job.employee:
                for i in range(len(EDUCATION_LEVELS)):
                    if job.employee.education == EDUCATION_LEVELS[i]:
                        company_vector[i] += 1

        employee_index = 0 #finds at what index the '1' is at
        for i in range(len(EDUCATION_LEVELS)):
            if employee.education == EDUCATION_LEVELS[i]:
                employee_index = i

        #turns all preceding numbers to '0' before employee index
        for i in range(employee_index): 
            company_vector[i] = 0

        return utils.cosine_similarity(employee_vector, company_vector)

    # 2.3.1.5
    def estimate_hire_success(self, job, employee):
        """ (Company, Job, Employee) -> float

        Estimate hire success score as weighted average of skills
        similarity (80%) and education similarity (20%). Returns 
        0.0 if job already has an employee.

        >>> comp = Company("Happy Tails Academy", "Montreal", [], "jobs.csv")
        >>> job = comp.jobs[1]
        >>> empl = Employee("James", 0, "M", "high school", "Spy",
        ...                 "pet-trainer")
        >>> comp.jobs[0].employee = empl
        >>> empl2 = Employee("Martin", 0, "M", "bachelors", "vet",
        ...                  "pet-veterenarian")
        >>> comp.estimate_hire_success(job, empl2)
        0.28

        >>> nba_job = Job("Coach", "leadership", 50000)
        >>> nba_co = Company("NBA", "LA", [])
        >>> coach = Employee("Phil", 65, 'm', 'bachelors', 'coach',
        ...                  'leadership-strategy')
        >>> nba_co.estimate_hire_success(nba_job, coach)
        0.57

        >>> tech_job = Job("Dev", "python", 60000)
        >>> tech_co = Company("Tech", "SF", [Employee("A", 30, 'm', 
        ...                   'masters', '', '', None)], "jobs_test.csv")
        >>> dev = Employee("B", 25, 'f', 'bachelors', 'intern', 'python')
        >>> tech_co.estimate_hire_success(tech_job, dev)
        0.8
        """
        if job.employee is not None:
            return NO_EMPLOYEE_SCORE

        s_skills = self.skills_similarity(job, employee)
        s_education = self.education_similarity(employee)

        score = SKILLS_WEIGHT * s_skills + EDUCATION_WEIGHT * s_education
        return round(score, ROUNDING_PRECISION)

    # 2.3.1.6
    def hire(self, job_candidates):
        """ (Company, dict: list of Employee) -> dict: Employee or None

        Hire the best eligible candidate for each job reference. Processes
        jobs in dictionary order. Returns dictionary mapping job references
        to hired employees.

        >>> comp = Company("Happy Tails Academy", "Montreal", [], "jobs.csv")
        >>> r_train, r_recep, r_handle = comp.jobs[0].ref, comp.jobs[1].ref,
        ...                              comp.jobs[2].ref
        >>> e_tri = Employee("sam", 25, "f", "bachelors", "trainer-writer",
        ...                  "entry-level-dog-trainer")
        >>> e_tr2 = Employee("mike", 28, "m", "masters", "trainer-vet",
        ...                  "sql-excel")
        >>> e_reci = Employee("alex", 22, "m", "high school", 
        ...                   "receptionist-Secretary", 
        ...                    "front-desk--pet-clinic")
        >>> e_rec2 = Employee("taylor", 23, "f", "bachelors", "receptionist",
        ...                   "scheduling-front-desk")
        >>> e_hand1 = Employee("jordan", 21, "m", "high school", "writer",
        ...                    "daycare-playroom-handler")
        >>> e_hand2 = Employee("casey", 27, "f", "bachelors", 
        ...                    "handler-bouncer", "kennel-maintenance")
        >>> result = comp.hire({r_train: [e_tr2, e_tri], r_recep:
        ...                    [e_rec2, e_reci], r_handle: 
        ...                    [e_hand2, e_hand1]})
        >>> result[r_train].name
        'sam'

        >>> nba_co = Company("NBA", "LA", [], "jobs_test.csv")
        Exception caught: could not convert string to float: 'forty-thousand'
        >>> nba_job = Job("Coach", "basketball", 100000)
        >>> nba_co.jobs = [nba_job]
        >>> coach1 = Employee("Coach A", 50, 'm', 'bachelors', 'coach',
        ...                   'basketball')
        >>> coach2 = Employee("Coach B", 55, 'm', 'masters', 'coach', 
        ...                   'basketball-leadership')
        >>> result = nba_co.hire({nba_job.ref: [coach1, coach2]})
        >>> result[nba_job.ref].name
        'Coach A'

        >>> empty_co = Company("Empty", "NY", [], "jobs_test.csv")
        >>> empty_result = empty_co.hire({1: []})
        >>> empty_result[1]
        """
        result = {}
        hired_in_this_call = []

        for job_ref in job_candidates:
            job = None
            for j in self.jobs: #finds corresponding job reference
                if j.ref == job_ref:
                    job = j

            if job is None: #job not found
                result[job_ref] = None

            elif job.employee is not None: #job already has employee
                result[job_ref] = job.employee

            else: #job is available for hiring
                candidates = job_candidates[job_ref]
                best_candidate = None
                best_score = INITIAL_BEST_SCORE


            #checks if hired for another job in call
                for candidate in candidates:
                    already_hired = False 
                    for hired in hired_in_this_call:
                        if candidate == hired:
                            already_hired = True

                    if not already_hired and candidate.cur_job is None:
                        score = self.estimate_hire_success(job, candidate)

                        if score > best_score: #updates to best score
                            best_score = score
                            best_candidate = candidate

                if best_candidate is not None: #hires best candidate
                    best_candidate.cur_job = job.title
                    job.employee = best_candidate

                    #check if candidate already employee for company
                    candidate_in_company = False 
                    for emp in self.employees:
                        if emp == best_candidate:
                            candidate_in_company = True

                    if not candidate_in_company:
                        self.employees.append(best_candidate)

                    hired_in_this_call.append(best_candidate)
                    result[job_ref] = best_candidate
                else:
                    result[job_ref] = None

        return result

    # 2.3.1.7
    def fire(self, employee):
        """ (Company, Employee) -> None

        Remove an employee from their current job at the company.
        Clears job assignment and removes employee from company's
        employee list.

        >>> comp = Company("Test", "NY", [])
        >>> emp = Employee("John", 30, 'm', 'bachelors', '', '', None)
        >>> comp.fire(emp)
        Traceback (most recent call last):
        ...
        AssertionError: Employee isn't a part of the organization

        >>> nba_co = Company("NBA", "LA", [])
        >>> coach = Employee("Coach", 50, 'm', 'bachelors', 'coach',
        ...                  'basketball')
        >>> nba_job = Job("Coach", "basketball", 100000, coach)
        >>> nba_co.jobs = [nba_job]
        >>> nba_co.employees = [coach]
        >>> coach.cur_job = "Coach"
        >>> nba_co.fire(coach)
        >>> coach.cur_job

        >>> simple_co = Company("Simple", "SF", [Employee("A", 30, 'm',
        ...                     'bachelors', '', '', None)])
        >>> simple_co.fire(simple_co.employees[0])
        >>> len(simple_co.employees)
        0
        """
        employee_in_company = False
        for emp in self.employees: #checks if employee in company
            if emp == employee:
                employee_in_company = True

        if not employee_in_company:
            raise AssertionError("Employee isn't a part of the organization")

        for job in self.jobs: #Remove employee from their assigned job
            if job.employee == employee:
                job.employee = None

        employee.cur_job = None #Clear employee's current job reference

        new_employees = [] #Remove employee from company's employee list
        for emp in self.employees:
            if emp != employee:
                new_employees.append(emp)
        self.employees = new_employees
