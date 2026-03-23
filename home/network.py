#Justin-Kenneth Denault
#261296919

from job import Job

REQUIRED_FIELDS = 3

#3

#3.1
def create_job_list(csv_filename):
    """ (str) -> list

    Load open roles from a CSV file and return a list of Job objects with
    no employee assigned. Reads file line by line, splits on commas, and
    processes rows with exactly three fields. Rows with invalid salary values
    or incorrect field count are skipped.

    >>> jobs = create_job_list("jobs.csv")
    >>> len(jobs)
    3
    >>> jobs[0].title
    'trainer'

    >>> jobs = create_job_list("jobs_test.csv")
    >>> len(jobs)
    3
    >>> jobs[1].title
    'receptionist'

    >>> test_jobs = create_job_list("test_jobs.csv")
    Exception caught: could not convert string to float: 'one-million'
    >>> len(test_jobs)
    1
    """
    jobs = []

    file = open(csv_filename, 'r')

    for line in file:
        line = line.strip()
        info = line.split(',')

        if len(info) == REQUIRED_FIELDS:
            title = info[0].strip()
            keywords = info[1].strip()
            salary_str = info[2].strip()

            try:
                salary = float(salary_str)
                job = Job(title, keywords, salary, None)
                jobs.append(job)
            except Exception as e:
                print("Exception caught: " + str(e))

    file.close()
    return jobs
