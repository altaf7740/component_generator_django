from django.shortcuts import render
from django.contrib import messages
import json
import textwrap

# Create your views here.

def generate_html(json_data):
    if 'tag' not in json_data:
        return ''

    tag = json_data['tag']
    html = f'<{tag}'

    if 'attributes' in json_data:
        attributes = json_data['attributes']
        if 'style' in attributes:
            style = attributes['style']
            style_string = '; '.join([f'{k}:{v}' for k, v in style.items()])
            html += f' style="{style_string}"'
            del attributes['style']

        for key, value in attributes.items():
            if isinstance(value, dict):
                value = ' '.join([f'{k}:{v}' for k, v in value.items()])
            html += f' {key}="{value}"'

    if 'content' in json_data:
        html += f'>{json_data["content"]}</{tag}>'
    elif json_data.get('is_self_closing_tag', False):
        html += ' />'
    else:
        html += '>'

        if 'children' in json_data and isinstance(json_data['children'], list):
            for child in json_data['children']:
                html += generate_html(child)

        html += f'</{tag}>'
    print(html)
    return html




def home(requests):
    context = {
        "generated_html": "",
        "form_data": "",
        "sample_data": textwrap.dedent("""Sample JSON generate components:
        {
            "tag":"h1",
            "is_self_closing_tag":false,
            "attributes":{},
            "children":[]
        }
        """)
    }

    if requests.method == "POST":
        try:
            json_query = json.loads(requests.POST["query"])
            context["generated_html"] = generate_html(json_query)
        except json.decoder.JSONDecodeError as msg:
            messages.error(requests, f"Invalid JSON: {msg}")
            context["form_data"] = requests.POST["query"]
    return render(requests, 'home.html', context)