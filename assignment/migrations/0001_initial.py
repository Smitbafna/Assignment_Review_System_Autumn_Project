# Generated by Django 3.2.12 on 2024-10-14 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignment_id', models.AutoField(primary_key=True, serialize=False)),
                ('assignment_name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('assignment_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentSubtask',
            fields=[
                ('subtask_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('subtask_end_date', models.DateField()),
                ('subtask_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('attachment_id', models.AutoField(primary_key=True, serialize=False)),
                ('attachment_type', models.CharField(choices=[('document', 'Document'), ('image', 'Image'), ('video', 'Video'), ('other', 'Other')], max_length=50)),
                ('attachment_name', models.CharField(max_length=255)),
                ('iteration', models.PositiveIntegerField(default=1, editable=False)),
                ('date_of_submission', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedback_id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('submission_id', models.AutoField(primary_key=True, serialize=False)),
                ('isCompleted', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('submission_status', models.CharField(choices=[('submitted', 'Submitted'), ('under_review', 'Under Review'), ('completed', 'Completed'), ('rejected', 'Rejected')], default='submitted', max_length=50)),
                ('reviewer_id_FK', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='assignment.assignmentsubtask')),
                ('subtask_id_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='assignment.assignmentsubtask')),
            ],
        ),
    ]
