from django.db import models




from django.conf import settings

# Create your models here.

class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    is_assign_creator_FK = models.ForeignKey('organization.OrgMember', on_delete=models.CASCADE, related_name='creator_of_assignments')
    assignment_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    assignment_description = models.TextField()
   
    assigned_teams_FK = models.ManyToManyField('organization.Team', related_name='assignments')
    assign_reviewer_FK = models.ManyToManyField('organization.OrgMember', related_name='reviewed_assignments', blank=True)

    def __str__(self):
        return self.assignment_name
    
    











class AssignmentSubtask(models.Model):
    subtask_id = models.AutoField(primary_key=True)
    ass_to_subtask_FK = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='assignment_subtasks')
    description = models.TextField()
    subtask_end_date = models.DateField()
    assign_subtask_status_FK=models.OneToOneField('Submission', on_delete=models.CASCADE, related_name='status_subtasks')
    subtask_status = models.BooleanField(default=False)
    assign_subtask_reviewer_FK = models.ManyToManyField(Assignment, related_name='assignment_subtasks_reviewer')


    def __str__(self):
        return f"Subtask {self.subtask_id} of Assignment {self.assignment.title}"













class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    subtask_id_FK = models.ForeignKey(AssignmentSubtask, on_delete=models.CASCADE, related_name='submissions')
    isCompleted = models.BooleanField(default=False)
    reviewer_id_FK = models.OneToOneField(AssignmentSubtask, on_delete=models.CASCADE, related_name='reviews')
    team_leader_id_FK = models.ForeignKey('organization.Team', on_delete=models.CASCADE, related_name='team_lead_submissions')
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    submission_status = models.CharField(max_length=50, choices=[
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected')
    ], default='submitted')

    def __str__(self):
        return f'Submission {self.submission_id} for Subtask {self.subtask_id}'












class Attachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    attachment_type = models.CharField(max_length=50, choices=[
        ('document', 'Document'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('other', 'Other')
    ])
    attachment_name = models.CharField(max_length=255)
    iteration = models.PositiveIntegerField(default=1, editable=False)  
    date_of_submission = models.DateField(auto_now_add=True)  
    submission_id_FK=models.ForeignKey(Submission,on_delete=models.CASCADE, related_name='attachments_related')


    def save(self, *args, **kwargs):
        # Automatically set the iteration number based on the number of previous attachments for the same submission
        if not self.pk:  # Check if it's a new attachment (not yet saved to the database)
            previous_attachments = Attachment.objects.filter(submission=self.submission).count()
            self.iteration = previous_attachments + 1  # Set iteration based on existing attachments
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.attachment_name} ({self.attachment_type})'
    





class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    attach_feed_FK = models.OneToOneField(Attachment, on_delete=models.CASCADE, related_name='feedbacks')
    feedback = models.TextField()

    def __str__(self):
        return f'Feedback for {self.attachment.attachment_name}'