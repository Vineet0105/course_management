# from django.contrib.auth.models import User
# from rest_framework.test import APITestCase
# from django.urls import reverse
# from .models import Student,Course
# from rest_framework import status
# class CourseTestCase(APITestCase):
#     def setUp(self):
#         self.user =  User.objects.create_user(username='vineet',password='123',email='vineet@gmail.com')
#         login_url = reverse('token_obtain_pair')
#         response  = self.client.post(login_url,{"username": "vineet", "password":"123"},format="json")
#         self.token = response.data['access']
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         s1 = Student.objects.create(name="A", email="a@example.com", user=self.user)
#         s2 = Student.objects.create(name="B", email="b@example.com", user=self.user)
#         s3 = Student.objects.create(name="C", email="c@example.com", user=self.user)

#     def test_student(self):
#         url = reverse('student-list')
#         data  = {
#             "name": "Vineet",
#             "email": "vineet@gmail.com"
#             }
        
#         response = self.client.post(url,data,format='json')
#         self.assertEqual(Student.objects.all().count(),4)
#         self.assertEqual(Student.objects.last().name,"Vineet")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


#     def test_course(self):
#         url = reverse('student-list')
#         data  = {
#             "name": "Vineet",
#             "email": "vineet@gmail.com"
#             }
        
#         response = self.client.post(url,data,format='json')
#         self.assertEqual(Student.objects.all().count(),4)

#         url = reverse('course-list')
#         data  ={
#             "students": [1],
#             "title": "Maths"
#             }
        
#         response = self.client.post(url,data,format='json')
#         self.assertEqual(Course.objects.all().count(),1)
#         self.assertEqual(Course.objects.first().title,"Maths")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


#     def test_add(self):
#         url = reverse('course-list')
#         data  ={
#             "students": [1],
#             "title": "Maths"
#             }
        
#         response = self.client.post(url,data,format='json')
#         url = reverse('course-add-student', args=[1, f"{self.s2.id},{self.s3.id}"])
#         response = self.client.post(url)
#         course = Course.objects.first()
#         self.assertEqual(course.students.count(),3)


from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Student, Course
from rest_framework import status

class CourseTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='vineet', password='123', email='vineet@gmail.com'
        )

        # Authenticate user via JWT
        login_url = reverse('token_obtain_pair')
        response = self.client.post(
            login_url,
            {"username": "vineet", "password": "123"},
            format="json"
        )
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Create initial students and assign to self for later reference
        self.s1 = Student.objects.create(name="A", email="a@example.com", user=self.user)
        self.s2 = Student.objects.create(name="B", email="b@example.com", user=self.user)
        self.s3 = Student.objects.create(name="C", email="c@example.com", user=self.user)

    # ------------------------
    # Test creating a new student
    # ------------------------
    def test_create_student(self):
        url = reverse('student-list')
        data = {"name": "Vineet", "email": "vineet@gmail.com"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 4)
        self.assertEqual(Student.objects.last().name, "Vineet")

    # ------------------------
    # Test creating a course with one student
    # ------------------------
    def test_create_course(self):
        url = reverse('course-list')
        data = {
            "title": "Maths",
            "students": [self.s1.id]  # Use object ID, not hardcoded
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        course = Course.objects.first()
        self.assertEqual(course.title, "Maths")
        self.assertIn(self.s1, course.students.all())  # Verify M2M link

    # ------------------------
    # Test adding multiple students using custom action
    # ------------------------
    def test_add_students_to_course(self):
        # First, create a course
        course = Course.objects.create(title="Science")
        course.students.add(self.s1)  # Initially one student

        # Build URL for custom add-student action
        url = reverse('course-add-student', args=[course.id, f"{self.s2.id},{self.s3.id}"])
        response = self.client.post(url)

        # Verify API response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that all three students are linked
        self.assertEqual(course.students.count(), 3)
        self.assertIn(self.s1, course.students.all())
        self.assertIn(self.s2, course.students.all())
        self.assertIn(self.s3, course.students.all())

    # ------------------------
    # Test removing students using custom action
    # ------------------------
    def test_remove_students_from_course(self):
        # Create course with all three students
        course = Course.objects.create(title="History")
        course.students.set([self.s1, self.s2, self.s3])

        # Build URL for custom remove-student action
        url = reverse('course-remove-student', args=[course.id, f"{self.s2.id},{self.s3.id}"])
        response = self.client.post(url)

        # Verify API response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Only s1 should remain
        self.assertEqual(course.students.count(), 1)
        self.assertIn(self.s1, course.students.all())
        self.assertNotIn(self.s2, course.students.all())
        self.assertNotIn(self.s3, course.students.all())
