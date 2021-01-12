from chapter.models import Chapter
from course.models import Course
from document.models import Document
from language.models import Language, Extension
from question.models import Question
from users.models import User
from year.models import Year
import os

print("Create Extension")
try:
    ext = Extension.objects.get(name="py")
except Extension.DoesNotExist:
    default_code = """
if __name__ == "__main__":
    print("Hello world")
"""
    ext = Extension(name="py", mode="python", default_comment=default_code)
ext.save()
print("Create Language")
try:
    lang = Language.objects.get(name="Python")
except Language.DoesNotExist:
    lang = Language(name="Python")
lang.save()
if ext not in lang.accepted_extensions.all():
    lang.accepted_extensions.add(ext)
print("Create Year")
try:
    y = Year.objects.get(name="2020-2021")
except Year.DoesNotExist:
    y = Year(name="2020-2021")
y.save()
print("Create Course")
try:
    c = Course.objects.get(name="INFO-F-101", year=y)
except Course.DoesNotExist:
    c = Course(name="INFO-F-101", year=y)
c.save()

question_latex = "When \\(a \\ne 0\\), there are two solutions to \\(ax^2 + bx + c = 0\\) and they are \\[x = {-b \\pm \\sqrt{b^2-4ac} \\over 2a}.\\]"

for txt in ["Examen Janvier 2021", "Examen Juin 2021", "Examen aout 2021", ]:
    print(txt)
    try:
        chapter = Chapter(name=txt, refer_course=c)
    except Chapter.DoesNotExist:
        chapter = Chapter(name=txt, refer_course=c)
    chapter.save()
    if chapter not in c.chapters.all():
        c.chapters.add(chapter)

    for txt2 in ["Question 1", "Question 2", "Question 3"]:
        print(txt2)
        try:
            q = Question.objects.get(name="{}-{}".format(txt, txt2), refer_chapter=chapter, can_add_documents=True if "3" in txt2 else False, can_add_code=True if "3" in txt2 else False)
        except Question.DoesNotExist:
            q = Question(name="{}-{}".format(txt, txt2), question="{}-{}:{}".format(txt, txt2, question_latex),
                         refer_chapter=chapter)
        q.save()
        if lang not in q.languages.all():
            q.languages.add(lang)
        q.init_default_code()
        if q not in chapter.questions.all():
            chapter.questions.add(q)
        if "3" in txt2:
            filename = "example.{}".format(ext.name)
            path_filename = os.path.join(q.get_relative_path(), filename)
            with open(path_filename, "w") as f:
                f.write(ext.default_comment)
                doc = Document(name=filename, path=path_filename, extension=ext)
                doc.save()
            q.default_code.add(doc)

print("Add course to user")
u = User.objects.get(id=1)
if c not in u.courses.all():
    u.add_course(c)
print("end")
