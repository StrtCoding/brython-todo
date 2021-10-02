from browser import alert, document, ajax, html
import json

BASE_URL = "https://simple-flask-restapi.herokuapp.com"

task_input = document['task-input']
add_button = document['add-button']
tasks_div = document['tasks']
edit_button = document['edit-button']

def remove_task(event):
    task_div = event.target.parent
    del document[task_div.id]

    delete_task(task_div.id)

def checked_task(event):
    checkbox = event.target
    parent_div = checkbox.parent
    title_span = parent_div.children[1]
    task_id = parent_div.id

    if checkbox.checked:
        title_span.style = {"text-decoration": "line-through"}
        completed_task(task_id, 1)
    else:
        title_span.style = {"text-decoration": ""}
        completed_task(task_id, 0)

global task_id

def edit_task(event):
    title = task_input.value
    update_task(task_id, title)
    refresh_task(task_id, title)

    task_input.value = ""
    edit_button.style = {"visibility": "hidden"}

edit_button.bind("click", edit_task)

def selected_task(event):
    title_span = event.target
    global task_id
    task_id = title_span.parent.id
    task_input.value = title_span.text

    edit_button.style = {'visibility': 'visible'}


def refresh_task(_id, title):
    task_div = document[_id]
    title_span = task_div.children[1]
    title_span.text = title


def create_task_component(data):
    parent_div = html.DIV(Class="mb-5 is-clickable", id=str(data['id']))
    completed_checkbox = html.INPUT(type="checkbox")
    title_span = html.SPAN(data['title'], Class='ml-3')
    delete_icon = html.I(Class="fas fa-trash-alt is-clickable", style={"float": "right"})
    date_div = html.DIV(data['created_date'], Class="ml-5", style={"color": "#898989"})

    completed_checkbox.bind("change", checked_task)
    title_span.bind("click", selected_task)
    delete_icon.bind("click", remove_task)

    parent_div <= completed_checkbox
    parent_div <= title_span
    parent_div <= delete_icon
    parent_div <= date_div

    return parent_div


def add_task(req):
    data = json.loads(req.text)
    tasks_div <= create_task_component(data)
    task_input.value = ""


def load_tasks(req):
    data = json.loads(req.text)['tasks']

    for task in data:
        task_div = create_task_component(task)
        tasks_div <= task_div

        checkbox = task_div.children[0]
        title_span = task_div.children[1]

        if task['completed']:
            checkbox.checked = True
            title_span.style = {"text-decoration": "line-through"}



def post_task(event):
    value = task_input.value
    data = json.dumps({"title": value})

    request = ajax.Ajax()
    request.bind("complete", add_task)
    request.open("POST", BASE_URL + "/tasks")
    request.set_header('content-type', 'application/json')
    request.send(data)

add_button.bind("click", post_task)


def get_tasks():
    request = ajax.Ajax()
    request.bind("complete", load_tasks)
    request.open("GET", BASE_URL + "/tasks")
    request.set_header('content-type', 'application/json')
    request.send()

def completed_task(_id, completed):
    request = ajax.Ajax()
    request.open("PUT", BASE_URL + f"/tasks/completed?id={_id}&completed={completed}")
    request.set_header('content-type', 'application/json')
    request.send()


def update_task(_id, title):
    data = json.dumps({"title": title})
    request = ajax.Ajax()
    request.open("PUT", BASE_URL + f"/tasks?id={_id}")
    request.set_header('content-type', 'application/json')
    request.send(data)

def delete_task(_id):
    request = ajax.Ajax()
    request.open("DELETE", BASE_URL + f"/tasks?id={_id}")
    request.set_header('content-type', 'application/json')
    request.send()

get_tasks()