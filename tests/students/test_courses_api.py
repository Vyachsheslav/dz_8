import pytest
from django.urls import reverse
from students.models import Course


@pytest.mark.django_db
def test_course_retrieve(client, course_factory):
    course_factory(_quantity=10)
    course = Course.objects.latest('id')
    detail_course = reverse('courses-detail', args=[course.id])
    url_course = client.get(detail_course)
    detail_course = url_course.json()
    assert url_course.status_code == 200
    assert detail_course['name'] == course.name


@pytest.mark.django_db
def test_course_list(client, course_factory):
    course_factory(_quantity=10)
    course_url = reverse('courses-list')
    url_course = client.get(course_url)
    detail_course = url_course.json()
    assert url_course.status_code == 200
    assert len(detail_course) == 10


@pytest.mark.django_db
def test_filter_id(client, course_factory):
    course_factory(_quantity=10)
    course = Course.objects.first()
    course_url = reverse('courses-list') + '?id={}'.format(course.id)
    url_course = client.get(course_url)
    course_list = url_course.json()
    assert url_course.status_code == 200
    assert course_list[0]['id'] == course.id


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    course_factory(_quantity=10)
    course = Course.objects.latest('id')
    course_url = reverse('courses-list') + '?name={}'.format(course.name)
    url_course = client.get(course_url)
    course_list = url_course.json()
    assert url_course.status_code == 200
    assert course_list[0]['name'] == course.name


@pytest.mark.django_db
def test_create_course(client, student_factory):
    course_url = reverse('courses-list')
    student_factory(_quantity=25)
    new_course = client.post(course_url, {'name': 'python', 'students': []})
    assert new_course.status_code == 201


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course_factory(_quantity=10)
    course = Course.objects.first()
    course_url = reverse('courses-detail', args=[course.id])
    update_course = client.patch(course_url, {'name': 'java'})
    assert update_course.status_code == 200


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course_factory(_quantity=10)
    course = Course.objects.latest('id')
    course_url = reverse('courses-detail', args=[course.id])
    print(course.name)
    delete_course = client.delete(course_url, {'name': course.name})
    assert delete_course.status_code == 204