# Generated by Django 5.2.1 on 2025-07-04 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_remove_tasks_task_image_task_detail_task_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task_detail',
            name='task_image',
            field=models.ImageField(blank=True, default='task_images/default_img.jpg', null=True, upload_to='task_images'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')], default='PENDING', max_length=20),
        ),
    ]
