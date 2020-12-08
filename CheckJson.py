## -*- coding: utf-8 -*-
from jsonschema import Draft7Validator
import json
import jsonschema
import os
import jinja2

abs_path = os.path.abspath("event")
fds = (os.listdir(abs_path))
error_table=[]
template = jinja2.Template('''
<table cellspacing="2" border="1" cellpadding="5">
    {% for row in table %}
    <tr>
        {% for value in row %}
        <td width="20%">{{ value }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
</table>
''')
open("error.html","w").close()

def writeHTML(template,table):
    text = template.render(table=table)
    html_file = open('error.html', "a")
    html_file.write(text)
    html_file.close()

def prepapeScheme(name):
    name = 'schema/'+ name
    with open(name, 'r') as f:
        data_value = f.read()
        data_json = json.loads(data_value)
        f.close()
    return data_json

def preparJson(fds):
    for temp in fds:
        error_table=[]
        json_path='event/'+temp
        try:
           with open(json_path, 'r') as f:
                data_value = f.read()
                data_json = json.loads(data_value)
                f.close()
           name_schema=data_json["event"] + '.schema'
           schema_value = prepapeScheme(name_schema)
           Draft7Validator.check_schema(schema_value)
           v = Draft7Validator(schema_value)
           errors = sorted(v.iter_errors(data_json), key=lambda e: e.path)
           for err in errors:
                 error_path=' '+' '.join(list(err.relative_path))
                 error = [temp, 'Необходимо исправить  ' + err.validator +  error_path +  '. Ошибка:' +  err.message]
                 error_table.append(error)
           writeHTML(template, error_table)
        except jsonschema.exceptions.SchemaError:
            error = [name_schema , 'Не правильно составлена схема']
            error_table.append(error)
            writeHTML(template, error_table)
        except TypeError:
            error = [temp , 'Пустой JSON. Отсутствует объявление JSON-схемы']
            error_table.append(error)
            writeHTML(template,error_table)
        except KeyError:
            error = [temp, 'Отсутствует объявление JSON-схемы. Необходимо добавить "event":"имя_схемы",']
            error_table.append(error)
            writeHTML(template,error_table)
        except FileNotFoundError:
            error = [temp, 'Не существует JSON-схемы с именем: '+name_schema]
            error_table.append(error)
            writeHTML(template,error_table)
        except json.decoder.JSONDecodeError as err:
            error = [temp, "JSON не валидный. Проверьте строку: "+str(err.lineno) + ', столбец '+str(err.colno)+". Ошибка:"+err.msg]
            error_table.append(error)
            writeHTML(template, error_table)
preparJson(fds)
