# -*- coding: utf-8 -*-
from konoha import KonohaError
from konoha.models import Page
from django.db import DatabaseError
from django.core.urlresolvers import reverse
from bs4 import BeautifulSoup
import pytest
from konoha.tests.datasources import colors
from konoha.tests.helpers import response_template_names, assert_redirects_to


__author__ = 'mikhailturilin'


@pytest.fixture(autouse=True)
def pages(settings):
    """
    We have 2 pages - index and about.
    """
    Page.objects.create(name="index", data="title: 'Index page title'", template='tests/index.html', path="") \
        .publish()
    Page.objects.create(name="filters", data="title: 'Filters page title'", template='tests/filters.html',
                        path="filters").publish()
    Page.objects.create(name="about", data="title: 'About page title'", template='tests/about.html',
                        path="about").publish()
    Page.objects.create(name="datasources", data="title: 'Datasource page title'",
                        template='tests/datasources.html', path="datasources").publish()


@pytest.mark.django_db
def test_404(client, settings):
    response = client.get('/trololololo')
    assert 404 == response.status_code


@pytest.mark.django_db
def test_pages_display_root(client):
    """ test page displayed by path"""
    index_response = client.get('/')
    assert 'tests/index.html' in response_template_names(index_response)

    index_response = client.get('')
    assert 'tests/index.html' in response_template_names(index_response)


@pytest.mark.django_db
def test_duplication_path(client):
    u"""
    Нельзя создать Page с существующим path
    """
    try:
        Page.objects.create(name="index2", data="", template='tests/index.html', path="")
        assert False, 'Can not create duplication path'
    except DatabaseError:
        pass

    try:
        Page.objects.create(name="index", data="", template='tests/index.html', path="sd")
        assert False, 'Can not create duplication name'
    except DatabaseError:
        pass


@pytest.mark.django_db
def test_data(client):
    u"""
    Отображение data в шаблоне
    """
    response = client.get('/')
    assert 'Index page title' in response.content


@pytest.mark.django_db
def test_datasources(client):
    """
    DATASOURCES is added to template context with the context processor
    """
    response = client.get('/datasources')

    for color in colors():
        assert color in response.content

    assert 'BLOBLOBLO' in response.content


@pytest.mark.django_db
def test_filters_markdown(client):
    response = client.get('/filters')
    soup = BeautifulSoup(response.content)
    assert any('Title 1' in str(h1) for h1 in soup.find_all('h1'))


@pytest.mark.django_db
def test_test_has_attribute(client):
    """
    Jinja has a concept if tests, a filter that returns true or false and could be called using
    'is' operator.
    """
    response = client.get('/filter_tests2')
    soup = BeautifulSoup(response.content)
    assert any('has_attribute works' in str(h2) for h2 in soup.find_all('h2'))


@pytest.mark.django_db
def test_save_new_version(client):
    """
    When we save a new version it should increase version count.
    """
    page = Page.objects.get(name="index")
    number_of_versions = page.versions.count()

    page.data = "title: Index page new title"
    page.save()

    assert number_of_versions != page.versions.count()


@pytest.mark.django_db
def test_invalid_version(client):
    """
    When the new version breaks the template - it should create a new version that is invalid
    """
    page = Page.objects.create(name="complex", data="title: 'some title'", template='tests/complex.html',
                               path="complex")

    assert not page.latest_version.valid


@pytest.mark.django_db
def test_cant_publish_invalid_version(client):
    page = Page.objects.create(name="complex", data="title: 'some title'", template='tests/complex.html',
                               path="complex")
    with pytest.raises(KonohaError):
        page.publish()


@pytest.mark.django_db
def test_display_version(client, admin_client):
    """
    1. When we publish a new version it's displayed.
    2. We can display previous version using version parameter.
    3. When we publish previous version it's displayed
    """

    page = Page.objects.get(name="index")
    page.data = "title: 'New index title'"
    page.save()
    page.publish()

    index_response1 = client.get('/')
    assert 'New index title' in index_response1.content

    # we are not logged in -> should be redirect
    index_response2 = client.get('/?version=1')
    assert index_response2.status_code in [301, 302]

    index_response2b = admin_client.get('/?version=1')
    assert 200 == index_response2b.status_code
    assert 'Index page title' in index_response2b.content

    page.publish(page.versions.get(version=1))
    index_response3 = admin_client.get('/')
    assert 'Index page title' in index_response3.content


@pytest.mark.django_db
def test_dont_display_unpublished_page(client):
    page = Page.objects.get(name="index")
    page.unpublish()

    response = client.get('/')
    assert 404 == response.status_code


@pytest.mark.django_db
def test_dont_display_unpublished_page_with_version(client, admin_client):
    page = Page.objects.get(name="index")
    page.data = "title: 'New index title'"
    page.save()
    page.publish()
    page.unpublish()

    # we don't display unpublished page with version
    response = client.get('/?version=1')
    assert 404 == response.status_code

    # however if we are an admin and we provided preview=true param - the page could be displayed
    response = admin_client.get('/?version=1&preview=true')
    assert 200 == response.status_code


@pytest.mark.django_db
def test_admin_works(admin_client):
    response = admin_client.get("/admin/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_pages_list(admin_client):
    response = admin_client.get("/admin/konoha/page/")
    assert response.status_code == 200

    # we should have several pages to test the list
    assert Page.objects.count() >= 4

    for page in Page.objects.all():
        assert page.name in response.content
        assert page.path in response.content

    soup = BeautifulSoup(response.content)
    soup_table = soup.find(id="result_list")
    soup_thead = soup_table.find("thead")
    soup_spans = soup_thead.find_all('span')
    headings = [(item.string or '').strip() for item in soup_spans]

    assert 'Name' in headings
    assert 'Path' in headings
    assert 'Published' in headings
    assert 'Versions' in headings


# noinspection PyUnresolvedReferences
@pytest.mark.django_db
def test_admin_new_page(admin_client):
    response = admin_client.get(reverse('admin:konoha_page_add'))

    # test controls
    check_admin_controls(response.content)

    # test save
    post_reponse = admin_client.post(reverse('admin:konoha_page_add'),
                               {
                                   'container': '',
                                   'name': 'new_index',
                                   'path': 'new_index',
                                   'data': 'title: privet',
                                   'template': 'tests/index.html',
                                   'login_required': 'off',
                                   'content_type': 'text/html',
                                   '_continue': 'Save and continue editing'
                               })

    assert post_reponse.status_code == 302


@pytest.mark.django_db
def test_admin_edit_page(admin_client):
    # open index page for edit
    page = Page.objects.get(name='index')
    start_num_versions = page.versions.count()

    admin_page_url = reverse('admin:konoha_page_change', args=[page.pk])

    # checking the admin page is working
    response = admin_client.get(admin_page_url)
    assert response.status_code == 200
    check_admin_controls(response.content)

    # change template
    post_reponse = admin_client.post(admin_page_url,
                               {
                                   'container': '',
                                   'name': 'index',
                                   'path': 'index',
                                   'data': page.data,
                                   'template': 'tests/about.html',
                                   'login_required': 'off',
                                   'content_type': 'text/html',
                                   '_continue': 'Save and continue editing'
                               }, follow=True)

    assert_redirects_to(post_reponse, admin_page_url)

    # check new version is not created
    assert page.versions.count() == start_num_versions

    # change data
    post_reponse2 = admin_client.post(admin_page_url,
                                {
                                    'container': '',
                                    'name': 'index',
                                    'path': 'index',
                                    'data': 'title: Very new title',
                                    'template': 'tests/about.html',
                                    'login_required': 'off',
                                    'content_type': 'text/html',
                                    '_continue': 'Save and continue editing'
                                })


    assert_redirects_to(post_reponse2, admin_page_url)


    # check new version is created
    assert page.versions.count() >= start_num_versions


@pytest.mark.django_db
def test_admin_publish(admin_client):
    # creating a new version
    page = Page.objects.get(name='index')
    page.data = "title: blabla"
    page.save()
    assert page.published_version.version == 1

    response = admin_client.get(reverse('admin:konoha_page_publish_version', args=[page.pk, 2]))

    page = Page.objects.get(name='index')
    assert page.published_version.version == 2


@pytest.mark.django_db
def test_admin_unpublish(admin_client):

    # creating a new version
    page = Page.objects.get(name='index')
    assert page.published

    response = admin_client.get(reverse('admin:konoha_page_unpublish', args=[page.pk]))
    assert response.status_code == 302

    page = Page.objects.get(name='index')
    assert not page.published



def check_admin_controls(content):
    soup = BeautifulSoup(content)
    input_names = {input['name'] for input in soup.find_all('input')}

    assert {'name', 'path', 'content_type'} <= input_names

    assert 'template' in {select['name'] for select in soup.find_all('select')}


