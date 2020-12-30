# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re
import shutil

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models
from django.utils import timezone

from answer.models import Answer
from document.models import Document


class CustomUserManager(UserManager):
    PATTERN = re.compile('[\W_]+')

    def _create_user(self, netid, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not netid:
            raise ValueError('The given netid must be set')
        email = self.normalize_email(email)
        user = self.model(netid=netid, email=email, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, netid, email=None, password=None, **extra_fields):
        return self._create_user(netid, email, password, **extra_fields)

    def create_superuser(self, netid, email, password, **extra_fields):
        return self._create_user(netid, email, password, is_staff=True, **extra_fields)


class User(AbstractBaseUser):
    USERNAME_FIELD = 'netid'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    objects = CustomUserManager()
    netid = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    email = models.CharField(max_length=255, unique=True)
    registration = models.CharField(max_length=80, blank=True)
    welcome = models.BooleanField(default=True)
    comment = models.TextField(blank=True, default='')

    inferred_faculty = models.TextField(blank=True)
    inscription_faculty = models.TextField(blank=True)

    is_staff = models.BooleanField(default=False)
    is_academic = models.BooleanField(default=False)
    is_representative = models.BooleanField(default=False)

    moderated_courses = models.ManyToManyField('course.Course', blank=True, related_name='moderated_courses')
    courses = models.ManyToManyField('course.Course', blank=True, related_name='courses')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    @property
    def name(self):
        return "{0.first_name} {0.last_name}".format(self)

    def get_courses(self):
        return self.courses.all()

    def add_course(self, course):
        if course not in self.courses.all():
            self.courses.add(course)
        #path_course = os.path.join(self.get_relative_path(), course.slug)
        path_course = course.get_user_relative_path(self)
        if not os.path.isdir(path_course):
            os.mkdir(path_course, settings.RIGHTS_DIR)
        for chapter in course.chapters.all():
            #path_chapter = os.path.join(path_course, course.slug)
            path_chapter = chapter.get_user_relative_path(self)
            if not os.path.isdir(path_chapter):
                os.mkdir(path_chapter, settings.RIGHTS_DIR)
            for question in chapter.questions.all():
                #path_question = os.path.join(path_chapter, question.slug)
                path_question = question.get_user_relative_path(self)
                if not os.path.isdir(path_question):
                    os.mkdir(path_question, settings.RIGHTS_DIR)
                answer = Answer(refer_question=question, user=self, path=path_question)
                answer.save()
                for code in question.default_code.all():
                    answer_path = os.path.join(path_question, code.name)
                    shutil.copy(code.path, answer_path)
                    doc = Document(name=code.name, path=answer_path, has_default=True, extension=code.extension)
                    doc.save()
                    answer.code.add(doc)
                question.answers.add(answer)

    def has_module_perms(self, *args, **kwargs):
        return True  # TODO : is this a good idea ?

    def has_perm(self, perm_list, obj=None):
        return self.is_staff

    def write_perm(self, obj):
        if self.is_staff:
            return True

        if obj is None:
            return False

        if self._moderated_courses is None:
            ids = [course.id for course in self.moderated_courses.only('id')]
            self._moderated_courses = ids

        return obj.write_perm(self, self._moderated_courses)

    def fullname(self):
        return self.name

    def get_short_name(self):
        return self.netid

    def get_absolute_students_path(self):
        return os.path.join(settings.MEDIA_DIR, settings.STUDENTS_DIR)

    def get_relative_students_path(self):
        return os.path.join(settings.MEDIA_DIR, settings.STUDENTS_DIR)

    def get_absolute_path(self):
        return os.path.join(self.get_absolute_students_path(), self.netid)

    def get_relative_path(self):
        return os.path.join(self.get_relative_students_path(), self.netid)

    def save(self, *args, **kwargs):
        if not os.path.isdir(self.get_relative_path()):
            if not os.path.isdir(settings.MEDIA_DIR):
                os.mkdir(settings.MEDIA_DIR, settings.RIGHTS_DIR)
            if not os.path.isdir(self.get_relative_students_path()):
                os.mkdir(self.get_relative_students_path(), settings.RIGHTS_DIR)
            os.mkdir(self.get_relative_path(), settings.RIGHTS_DIR)
        super(AbstractBaseUser, self).save(*args, **kwargs)
