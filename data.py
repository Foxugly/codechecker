from chapter.models import Chapter
from course.models import Course
from document.models import Document
from language.models import Language, Extension
from question.models import Question, QuestionTests
from users.models import User
from year.models import Year
from codecheck.settings import BASE_DIR, MEDIA_DIR
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
question_tests = """
import code

def test_delta_zero():
    print("Doing delta zero")
    x1, x2 = code.compute(1, 2, 1)
    assert x1 == x2


def test_delta_negative():
    assert code.compute(1, 2, 10) is None


def test_basic():
    x1, x2 = code.compute(2, 5, 2)
    print("x1=", x1, "x2=", x2)
    assert x1 == -0.5
    assert x2 == -2
"""
for txt in ["Examen Janvier 2021", "Examen Juin 2021", "Examen aout 2021", ]:
    print(txt)
    try:
        chapter = Chapter.objects.get(name=txt, refer_course=c)
    except Chapter.DoesNotExist:
        chapter = Chapter(name=txt, refer_course=c)
    chapter.save()
    if chapter not in c.chapters.all():
        c.chapters.add(chapter)

    for txt2 in ["Question 1", "Question 2", "Question 3"]:
        print(txt2)
        try:
            q = Question.objects.get(name="{}-{}".format(txt, txt2), refer_chapter=chapter,
                                     can_add_documents=True if "3" in txt2 else False, can_add_code=True if "3" in txt2 else False)
        except Question.DoesNotExist:
            q = Question(name="{}-{}".format(txt, txt2), question="{}-{}:{}".format(txt, txt2, question_latex),
                         refer_chapter=chapter)
        q.save()
        try:
            tests = QuestionTests.objects.get(refer_question=q)
        except QuestionTests.DoesNotExist:
            path = os.path.join(
                MEDIA_DIR, "courses", q.refer_chapter.refer_course.slug, q.refer_chapter.slug, q.slug, "tests.py")
            f = open(path, "w")
            f.write(question_tests)
            f.close()
            tests = QuestionTests(
                path=path,
                refer_question=q,
                command_execute="python -m pytest --verbose",
                command_list="python -m pytest --co"
            )
            tests.save()
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
                doc = Document(
                    name=filename, path=path_filename, extension=ext)
                doc.save()
            q.default_code.add(doc)

print("Add course to user")
u = User.objects.get(id=1)
if c not in u.courses.all():
    u.add_course(c)


print("end")
