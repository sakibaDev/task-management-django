import os
import django
import random
from faker import Faker
from django.db import connection

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

from tasks.models import Employee, Project, Task, TaskDetail


def reset_sequences():
    """Reset primary key sequences for PostgreSQL."""
    with connection.cursor() as cursor:
        tables = ['tasks_taskdetail', 'tasks_task', 'tasks_employee', 'tasks_project']
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
        print("🔄 Sequences reset for all tables.")


def populate_db():
    fake = Faker()

    # Create Projects
    projects = [
        Project.objects.create(
            name=fake.bs().capitalize(),
            description=fake.paragraph(),
            start_date=fake.date_this_year()
        )
        for _ in range(5)
    ]
    print(f"✅ Created {len(projects)} projects.")

    # Create Employees
    employees = [
        Employee.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        for _ in range(10)
    ]
    print(f"✅ Created {len(employees)} employees.")

    # Create Tasks
    tasks = []
    for _ in range(20):
        task = Task.objects.create(
            project=random.choice(projects),
            title=fake.sentence(nb_words=5),
            description=fake.paragraph(),
            status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
            completed=random.choice([True, False])
        )
        task.assigned_to.set(random.sample(employees, random.randint(1, 3)))
        tasks.append(task)
    print(f"✅ Created {len(tasks)} tasks.")

    # Create Task Details
    for task in tasks:
        TaskDetail.objects.create(
            task=task,
            priority=random.choice(['H', 'M', 'L']),
            notes=fake.paragraph()
        )
    print("✅ Populated TaskDetails for all tasks.")
    print("🎉 Database populated successfully!")


if __name__ == "__main__":
    reset_sequences()  # Truncate & reset IDs
    populate_db()      # Populate with new data
