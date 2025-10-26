from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Student, Course
from rest_framework import status

class CourseStudentAPITestCase(APITestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='vineet', password='123', email='vineet@gmail.com')
        self.user2 = User.objects.create_user(username='john', password='123', email='john@gmail.com')

        # Authenticate as user1
        login_url = reverse('token_obtain_pair')
        response = self.client.post(login_url, {"username": "vineet", "password": "123"}, format="json")
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Create initial students for user1
        self.s1 = Student.objects.create(name="A", email="a@example.com", user=self.user1)
        self.s2 = Student.objects.create(name="B", email="b@example.com", user=self.user1)
        self.s3 = Student.objects.create(name="C", email="c@example.com", user=self.user1)

        # Create a student for user2 (to test ownership)
        self.s4 = Student.objects.create(name="D", email="d@example.com", user=self.user2)

    # ------------------------
    # Test creating a student
    # ------------------------
    def test_create_student(self):
        url = reverse('student-list')
        data = {"name": "Vineet", "email": "vineet@gmail.com"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 5)
        self.assertEqual(Student.objects.last().name, "Vineet")

    # ------------------------
    # Test creating a course with one student
    # ------------------------
    def test_create_course(self):
        url = reverse('course-list')
        data = {"title": "Maths", "students": [self.s1.id]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        course = Course.objects.first()
        self.assertEqual(course.title, "Maths")
        self.assertIn(self.s1, course.students.all())

    # ------------------------
    # Test adding multiple students
    # ------------------------
    def test_add_students_to_course(self):
        course = Course.objects.create(title="Science")
        course.students.add(self.s1)

        url = reverse('course-add-student', args=[course.id, f"{self.s2.id},{self.s3.id}"])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(course.students.count(), 3)
        self.assertIn(self.s1, course.students.all())
        self.assertIn(self.s2, course.students.all())
        self.assertIn(self.s3, course.students.all())

    # ------------------------
    # Test removing students
    # ------------------------
    def test_remove_students_from_course(self):
        course = Course.objects.create(title="History")
        course.students.set([self.s1, self.s2, self.s3])

        url = reverse('course-remove-student', args=[course.id, f"{self.s2.id},{self.s3.id}"])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(course.students.count(), 1)
        self.assertIn(self.s1, course.students.all())
        self.assertNotIn(self.s2, course.students.all())
        self.assertNotIn(self.s3, course.students.all())

    # ------------------------
    # Test adding invalid student
    # ------------------------
    def test_add_invalid_student(self):
        course = Course.objects.create(title="Physics")
        invalid_id = 9999
        url = reverse('course-add-student', args=[course.id, str(invalid_id)])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ------------------------
    # Test removing invalid student
    # ------------------------
    def test_remove_invalid_student(self):
        course = Course.objects.create(title="Chemistry")
        course.students.add(self.s1)
        invalid_id = 9999
        url = reverse('course-remove-student', args=[course.id, str(invalid_id)])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ------------------------
    # Test duplicate student add
    # ------------------------
    def test_duplicate_student_add(self):
        course = Course.objects.create(title="Biology")
        course.students.add(self.s1)
        url = reverse('course-add-student', args=[course.id, str(self.s1.id)])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(course.students.count(), 1)  # M2M should remain unique

    # ------------------------
    # Test filtering courses by title
    # ------------------------
    def test_filter_courses_by_title(self):
        c1 = Course.objects.create(title="Maths")
        c2 = Course.objects.create(title="Physics")
        url = reverse('course-list') + "?title=Maths"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Maths")

