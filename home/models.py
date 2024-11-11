import os
import random
import string
from django.db import models
from django.utils import tree


def get_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    random_filename = f"{get_random_string(10)}.{ext}"
    return os.path.join('images/', random_filename)


class Unit(models.Model):
    ACADEMIC = 'Academic'
    ADMINISTRATIVE = 'Administrative'
    TYPE = (
        (ACADEMIC, 'Academic'), (ADMINISTRATIVE, 'Adminisrative'),
    )
    unit_name = models.CharField(max_length=255)
    unit_short_name = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50, choices=TYPE, default=ACADEMIC)

    def __str__(self) -> str:
        return self.unit_short_name

    class Meta:
        ordering = ['unit_name',]


class Department(models.Model):
    department_name = models.CharField(max_length=255)
    department_short_name = models.CharField(max_length=50)
    unit_id = models.ForeignKey(
        Unit, related_name="unit_department", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.department_short_name

    class Meta:
        ordering = ['department_name',]


class Position(models.Model):
    position_name = models.CharField(max_length=200, unique=True)
    position_short_name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.position_short_name

    class Meta:
        ordering = ['position_name',]


class Item(models.Model):
    pass
    # position_id = models.ForeignKey(
    #     Position, related_name="position_item", on_delete=models.CASCADE)
    # item_no = models.CharField(max_length=100, unique=True)
    # item_description = models.CharField(max_length=255)

    # def __str__(self) -> str:
    #     return f"{self.item_no} - ( {self.position_id} )"

    # class Meta:
    #     ordering = ['item_no',]


class Faculty(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    SEX = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    ELEMENTARY = 'Elementary'
    SECONDARY = 'Secondary'
    COLLEGE = 'College'
    MASTER = 'Master'
    DOCTOR = 'Doctor'
    EDUCATION = (
        (ELEMENTARY, 'Elementary'),
        (SECONDARY, 'Secondary'),
        (COLLEGE, 'College'),
        (MASTER, 'Master'),
        (DOCTOR, 'Doctor'),
    )
    COS = 'COS'
    PERMANENT = 'Permanent'
    VACANT = 'Vacant'
    JO = 'JO'
    STATUS = (
        (COS, 'COS'), (JO, 'JO'), (PERMANENT, 'Permanent'), (VACANT, 'Vacant'),
    )

    TEACHING = 'Teaching'
    NONE_TEACHING = 'Non-Teaching'
    WORK_STATUS = (
        (TEACHING, 'Teaching'),
        (NONE_TEACHING, 'Non-Teaching'),
    )

    RETIRED = 'Retired'
    RESIGNED = 'Resigned'
    AWOL = 'AWOL'
    STUDY = 'Study'
    INDEFINITE = 'Indefinite'
    TERMINATED = 'Terminated'
    OTHERS = 'Others'
    EMP_STATUS = (
        (RETIRED, 'Retired'), (RESIGNED, 'Resigned'), (AWOL, 'AWOL'),
        (STUDY, 'Study'), (INDEFINITE, 'Indefinite'),
        (TERMINATED, 'Terminated'), (OTHERS, 'Others'),
    )

    department_id = models.ForeignKey(
        Department, related_name="department_faculty", on_delete=models.CASCADE, blank=True, null=True)
    position_id = models.ForeignKey(
        Position, related_name="position_item", on_delete=models.CASCADE, blank=True, null=True)
    faculty_no = models.CharField(
        max_length=50, blank=True, null=True, unique=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    ext_name = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=SEX, null=True, blank=True)
    education = models.CharField(
        max_length=50, choices=EDUCATION, null=True, blank=True)
    date_hired = models.DateTimeField()
    email_address = models.CharField(max_length=200, blank=True, null=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_promoted = models.BooleanField(default=False)
    picture = models.ImageField(upload_to=upload_to, null=True, blank=True)
    remarks = models.CharField(max_length=255, blank=True,  null=True)
    contact_no = models.CharField(max_length=50, blank=True, null=True)
    date_promoted = models.DateTimeField(null=True, blank=True)
    date_started = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    item_status = models.CharField(
        choices=STATUS, max_length=50)
    employment_status = models.CharField(
        max_length=20, choices=EMP_STATUS, blank=True, null=True)
    employment_type = models.CharField(
        choices=WORK_STATUS, max_length=50, default=TEACHING)
    item_no = models.CharField(
        max_length=100, unique=True, blank=True, null=True)

    def __str__(self) -> str:
        if not self.ext_name and not self.middle_name:
            return f"{self.last_name}, {self.first_name}"
        elif not self.ext_name:
            return f"{self.last_name}, {self.first_name} {self.middle_name[0]}"
        else:
            return f"{self.last_name}, {self.first_name} {self.middle_name[0]} {self.ext_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class AcademicRank(models.Model):
    pass
    # COS = 'COS'
    # PERMANENT = 'Permanent'
    # VACANT = 'Vacant'
    # STATUS = (
    #     (COS, 'COS'), (PERMANENT, 'Permanent'), (VACANT, 'Vacant'),
    # )
    # # faculty_id = models.ForeignKey(
    # #     Faculty, related_name="faculty_academicRank", on_delete=models.CASCADE)
    # # rank_id = models.ForeignKey(
    # #     Item, related_name="rank_academicRank", on_delete=models.CASCADE)
    # date_promoted = models.DateTimeField(null=True, blank=True)
    # date_started = models.DateTimeField(null=True, blank=True)
    # date_end = models.DateTimeField(null=True, blank=True)
    # item_status = models.CharField(choices=STATUS, max_length=50, default=COS)
    # is_active = models.BooleanField()
