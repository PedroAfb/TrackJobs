from trackJobs.controller.api_job_controller import APIJobController
from trackJobs.model.job_model import JobModel


def get_job_controller() -> APIJobController:
    job_model = JobModel()
    return APIJobController(job_model)
