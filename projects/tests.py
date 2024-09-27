from django.test import TestCase
from .models import Project

class ProjectModelTest(TestCase):
    def test_project_creation(self):
        project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            start_date='2023-01-01',
            end_date='2023-12-31',
            project_manager=self.user,
        )
        self.assertTrue(isinstance(project, Project))
        self.assertEqual(project.__str__(), 'Test Project')
