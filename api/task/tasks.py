from collections import defaultdict

from celery import shared_task
from django.core.mail import send_mail
from apps.task.models import Task


@shared_task
def send_status_change_email(task_id, previous_status, new_status, recipient_email):
    subject = f'Изменение статуса задачи {task_id.title}'
    message = f'Статус вашей задачи {task_id.title} изменен с {previous_status} на {new_status}.'
    send_mail(subject, message, 'from@example.com', [recipient_email])


@shared_task
def send_daily_reports():
    user_tasks = defaultdict(list)
    print('dastan')
    # Собираем задачи для каждого пользователя
    for task in Task.objects.all().select_related('assignee'):
        if task.assignee:  # Убедитесь, что у задачи есть исполнитель
            user_tasks[task.assignee].append(task)

    # Отправляем письмо каждому пользователю с его задачами
    for user, tasks in user_tasks.items():
        subject = 'Ваши задачи'
        message = 'У вас есть следующие задачи:\n' + '\n'.join(
            [f'ID задачи {task.id} - {task.title}' for task in tasks])
        recipient_list = [user.email]

        send_mail(subject, message, 'from@example.com', recipient_list)
