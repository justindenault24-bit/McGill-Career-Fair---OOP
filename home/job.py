#Justin-Kenneth Denault
#261296919

from employee import Employee
import utils

MIN_SALARY = 0

#2.2

#2.2.1
class Job:
    """A class to represent a job posting at a career fair booth.

    Attributes:
        nb_jobs (class int): Counter for total jobs created.
        ref (int): Unique reference number assigned to each job.
        title (str): Job title.
        keywords (str): Dash-separated skills required for the job.
        salary (float): Salary for the job, must be non-negative.
        employee (Employee or None): Employee currently assigned to the job.
    """
    nb_jobs = 0

#2.2.1.1
    def __init__(self, title, keywords, salary, employee=None):
        """ (Job, str, str, float, Employee or None) -> None

        Initialize a new Job instance with title, keywords, salary, and
        optional employee. Increments the class counter and assigns a 
        unique reference number.

        >>> description = 'optimize-fraud-detection-software-poker'
        >>> job1 = Job('Fraud Analytics Manager', description, 120000)
        >>> job1.title
        'Fraud Analytics Manager'
        >>> job1.salary
        120000
        >>> job1.ref
        1

        >>> basketball_desc = 'coaching-player-development-strategy'
        >>> job2 = Job('Head Coach', basketball_desc, 8000000.0)
        >>> job2.title
        'Head Coach'
        >>> job2.ref
        2

        >>> lebron = Employee('LeBron James', 39, 'm', 'bachelors',
        ...                   'athlete-analyst', 'basketball-leadership')
        >>> job3 = Job('Player Development', 'mentoring-training', 500000,
        ...             lebron)
        >>> job3.employee.name
        'LeBron James'
        >>> job3.ref
        3
        """
        if salary < MIN_SALARY:
            raise ValueError("Salary must be non-negative")

        self.title = title
        self.keywords = keywords
        self.salary = salary
        self.employee = employee

        Job.nb_jobs += 1
        self.ref = Job.nb_jobs

#2.2.1.2
    def __str__(self):
        """ (Job) -> str

        Return a formatted string representation of the job with reference
        number, title, keywords as list, salary, and employee name or 'None'.

        >>> description = 'optimize-fraud-detection-software-poker'
        >>> job1 = Job('Fraud Analytics Manager', description, 120000)
        >>> print(job1)
        Reference: 4
        Title: Fraud Analytics Manager
        Keywords: ['optimize', 'fraud', 'detection', 'software', 'poker']
        Salary: 120000
        Employee: None

        >>> coaching_desc = 'leadership-strategy-player-development'
        >>> job2 = Job('Assistant Coach', coaching_desc, 1500000.0)
        >>> print(job2)
        Reference: 5
        Title: Assistant Coach
        Keywords: ['leadership', 'strategy', 'player', 'development']
        Salary: 1500000.0
        Employee: None

        >>> curry = Employee('Stephen Curry', 36, 'm', 'masters',
        ...                  'athlete-entrepreneur', 'shooting-marketing')
        >>> job3 = Job('Brand Ambassador', 'marketing-community-outreach',
        ...            750000, curry)
        >>> print(job3)
        Reference: 6
        Title: Brand Ambassador
        Keywords: ['marketing', 'community', 'outreach']
        Salary: 750000
        Employee: Stephen Curry
        """
        result = "Reference: " + str(self.ref) + "\n"
        result += "Title: " + self.title + "\n"
        result += "Keywords: " + str(utils.get_list(self.keywords)) + "\n"
        result += "Salary: " + str(self.salary) + "\n"
        result += "Employee: " + (self.employee.name if self.employee else "None")
        return result
