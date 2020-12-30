import json
import os

from django.http import HttpResponse

from answer.models import Answer
from document.models import Document
from language.models import Extension


def get_content(request, document_id):
    if request.is_ajax():
        d = Document.objects.get(id=document_id)
        results = {}
        try:
            f = open(d.path, 'r')
            results['code'] = f.read()
            f.close()
            results['mode'] = d.extension.mode
            results['has_default'] = d.has_default
            results['result'] = True
        except IOError as e:
            results['result'] = False
            results['error'] = e
        return HttpResponse(json.dumps(results))


def set_content(request, document_id):
    if request.is_ajax():
        d = Document.objects.get(id=document_id)
        results = {}
        try:
            f = open(d.path, 'w')
            f.write(request.GET['code'])
            f.close()
            results['result'] = True
        except IOError as e:
            results['result'] = False
            results['error'] = e
        return HttpResponse(json.dumps(results))


def get_default_content(request, document_id):
    if request.is_ajax():
        d = Document.objects.get(id=document_id)
        a = Answer.objects.get(id=request.GET['answer_id'])
        results = {}
        if d.has_default:
            try:
                default_doc = a.refer_question.default_code.get(name=d.name)
                print(default_doc.path)
                f_default = open(default_doc.path, 'r')
                f_answer = open(d.path, 'w')
                data = f_default.read()
                f_answer.write(data)
                results['code'] = data
                print(data)
                f_answer.close()
                f_default.close()
                results['result'] = True
            except IOError as e:
                print(e)
                results['result'] = False
                results['error'] = e
        else:
            results['result'] = False
            results['error'] = "No default code"
        return HttpResponse(json.dumps(results))


def add_file(request, answer_id):
    if request.is_ajax():
        a = Answer.objects.get(id=answer_id)
        results = {}
        try:
            ext = Extension.objects.get(id=request.GET['extension'])
        except:
            ext = None
            results['extension_error'] = True
        if request.GET['filename']:
            filename = "{}.{}".format(request.GET['filename'], ext.name)
        else:
            filename = None
            results['filename_error'] = True
        if ext and filename:
            docs = a.code.filter(name=filename)
            if len(docs):
                results['filename_error'] = True
                results['result'] = False
            else:
                try:
                    path_filename = os.path.join(a.get_relative_path(request.user), filename)
                    with open(path_filename, "w+") as f:
                        f.write("# type your code here")  # TODO lang.default_comment (to add)
                        doc = Document(name=filename, path=path_filename, extension=ext, has_default=False)
                        doc.save()
                    a.code.add(doc)
                    results['filename'] = filename
                    results['filename_id'] = doc.id
                    results['result'] = True
                except:
                    results['result'] = False
        else:
            results['result'] = False
        return HttpResponse(json.dumps(results))
