import pytest
import conftest
from task import conftest as package_conftest
from task_manager.tasks.models import Task as PackageModel
from task_manager.statuses.models import Status
from copy import deepcopy
from fixtures.test_tasks_additional import TEST_TASKS as TEST_ITEMS

TESTED_URL_PATTERN = "/tasks/<pk>/update/"
SUCCESS_URL = package_conftest.ITEM_LIST_URL


@pytest.mark.django_db
def test_basic_content(client, base_users):
    client.force_login(base_users[0])
    INITIAL_ITEM = deepcopy(TEST_ITEMS[0])
    pre_response = client.post(
        package_conftest.ITEM_CREATE_URL,
        INITIAL_ITEM,
        follow=True)
    assert package_conftest.CREATE_OK_MESSAGE in pre_response.content.decode()

    TESTED_URL = conftest.get_tested_url_for_max_id(
        TESTED_URL_PATTERN, PackageModel)

    response = client.get(TESTED_URL)
    content = response.content.decode()
    assert response.status_code == 200
    assert "Изменение задачи" in content
    assert "Имя" in content
    assert "Описание" in content
    assert "Статус" in content
    assert "Исполнитель" in content
    # assert "Метки" in content
    assert "Изменить" in content


@pytest.mark.django_db
def test_successfuly_updated_user(client, base_users):
    count_default_items_in_db = PackageModel.objects.all().count()
    author = base_users[0]
    client.force_login(author)

    INITIAL_ITEM = deepcopy(TEST_ITEMS[0])
    initial_status = Status.objects.first()
    INITIAL_ITEM['status'] = initial_status.id
    initial_executor = base_users[1]
    INITIAL_ITEM['executor'] = initial_executor.id

    pre_response = client.post(
        package_conftest.ITEM_CREATE_URL,
        INITIAL_ITEM,
        follow=True)
    assert package_conftest.CREATE_OK_MESSAGE in pre_response.content.decode()

    UPDATED_ITEM = deepcopy(TEST_ITEMS[1])
    updated_status = Status.objects.last()
    UPDATED_ITEM['status'] = updated_status.id
    updated_executor = base_users[2]
    UPDATED_ITEM['executor'] = updated_executor.id

    TESTED_URL = conftest.get_tested_url_for_max_id(
        TESTED_URL_PATTERN, PackageModel)

    response = client.post(TESTED_URL, UPDATED_ITEM, follow=True)
    assert response.redirect_chain == [
        (SUCCESS_URL, 302)
    ]
    response_content = response.content.decode()
    assert "Задача успешно изменена" in response_content

    # Is new item added to the database?
    assert PackageModel.objects.filter(name=UPDATED_ITEM['name']).exists()

    # Is old item removed from the database?
    with pytest.raises(PackageModel.DoesNotExist):
        PackageModel.objects.get(name=INITIAL_ITEM['name'])

    # Is number of items the same as before the update?
    assert PackageModel.objects.all().count() == count_default_items_in_db + 1


@pytest.mark.django_db
def test_with_incorrect_existing_username(client, base_users):
    client.force_login(base_users[0])
    INITIAL_ITEM = deepcopy(TEST_ITEMS[0])
    EXISTING_ITEM = deepcopy(TEST_ITEMS[1])

    pre_response1 = client.post(package_conftest.ITEM_CREATE_URL,
                                EXISTING_ITEM, follow=True)
    assert package_conftest.CREATE_OK_MESSAGE in pre_response1.content.decode()

    pre_response2 = client.post(package_conftest.ITEM_CREATE_URL,
                                INITIAL_ITEM, follow=True)
    assert package_conftest.CREATE_OK_MESSAGE in pre_response2.content.decode()

    TESTED_URL = conftest.get_tested_url_for_max_id(
        TESTED_URL_PATTERN, PackageModel)

    response = client.post(TESTED_URL, EXISTING_ITEM, follow=True)

    assert response.status_code == 200
    assert response.redirect_chain == []
    response_content = response.content.decode()
    assert ("уже существует.") in response_content


@pytest.mark.django_db
def test_with_anonymous_user(client):
    TESTED_URL = conftest.get_tested_url_for_max_id(
        TESTED_URL_PATTERN, PackageModel)
    response = client.get(TESTED_URL, follow=True)
    content = response.content.decode()
    redirect_url_with_query, status_code = response.redirect_chain[0]
    assert status_code == 302
    assert redirect_url_with_query.split('?')[0] == conftest.LOGIN_URL
    assert "Вы не авторизованы! Пожалуйста, выполните вход." in content
