from celery import shared_task
from django.conf import settings
from users.models import User, ProfessionalRequest
from reports.models import AdminDailyReport
import requests
import os
import logging

logger = logging.getLogger(__name__)

@shared_task(name="src.application.tasks.admin_reports.generate_daily_admin_report")
def generate_daily_admin_report():
    """
    Generates a daily summary report of users, projects, and profession requests.
    This task is scheduled to run daily at 09:00 AM.
    """
    logger.info("Starting Daily Admin Report Generation...")

    try:
        # 1. Fetch Local Data (Auth Service)
        total_users = User.objects.count()
        total_profession_requests = ProfessionalRequest.objects.count()

        # 2. Fetch Remote Data (User Service)
        # Default internal URL based on docker-compose service name and port
        user_service_url = os.getenv("USER_SERVICE_OP_STATS_URL", "http://user_service:8001/api/internal/stats/projects/")
        
        total_projects = 0
        try:
            response = requests.get(user_service_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                total_projects = data.get("total_projects", 0)
            else:
                logger.error(f"Failed to fetch project stats. Status: {response.status_code}, Response: {response.text}")
        except requests.RequestException as e:
            logger.error(f"Error connecting to User Service for stats: {e}")

        # 3. Aggregate and Save Report
        report = AdminDailyReport.objects.create(
            total_users=total_users,
            total_projects=total_projects, # Will be 0 if fetch fails, which is safer than breaking the report
            total_profession_requests=total_profession_requests
        )

        logger.info(f"Daily Admin Report Generated Successfully: {report}")
        return f"Report created: Users={total_users}, Projects={total_projects}, Requests={total_profession_requests}"

    except Exception as e:
        logger.exception(f"Critical error generating daily admin report: {e}")
        raise e
