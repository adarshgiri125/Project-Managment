# api/tasks.py
from celery import shared_task
from django.contrib.auth.models import User
from .models import Task
import time

@shared_task
def send_assignment_notification(task_id, assigned_by_user_id, assignee_id):
    """
    A Celery task to send an email notification.
    """
    try:
        task = Task.objects.get(id=task_id)
        assigned_by = User.objects.get(id=assigned_by_user_id)
        assignee = User.objects.get(id=assignee_id)

        # Simulate a slow email sending process
        print("Sending email...")
        time.sleep(5) # Pretend this takes 5 seconds

        subject = f"You have been assigned a new task: {task.title}"
        message = (
            f"Hi {assignee.username},\n\n"
            f"You have been assigned a new task '{task.title}' in the project '{task.project.title}' "
            f"by {assigned_by.username}.\n\n"
            "Thank you,\nThe KanbanFlow Team"
        )
        recipient = assignee.email

        print("--- EMAIL SIMULATION ---")
        print(f"To: {recipient}")
        print(f"Subject: {subject}")
        print(f"Body:\n{message}")
        print("------------------------")
        print("Email sent successfully!")

        return f"Email sent to {recipient} for task {task_id}"

    except (Task.DoesNotExist, User.DoesNotExist) as e:
        print(f"Could not send email. Task or User not found. Error: {e}")
        return "Failed to send email: Object not found"
