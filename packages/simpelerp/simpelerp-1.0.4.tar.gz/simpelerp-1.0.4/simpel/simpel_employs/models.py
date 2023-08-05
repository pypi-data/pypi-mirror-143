from django.db import models
from django.utils import timezone

# from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from simpel.simpel_core.models import NumeratorMixin

from .managers import DepartmentManager, PositionManager


class Department(MPTTModel):

    objects = DepartmentManager()
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    parent = TreeForeignKey(
        "Department",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="department_upline",
        verbose_name=_("Upline"),
    )
    code = models.CharField(
        unique=False,
        max_length=255,
        verbose_name=_("Code"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )

    class Meta:
        db_table = "simpel_employs_department"
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return self.name

    def get_manager_position(self):
        staffs = getattr(self, "staffs", None)
        return None if not staffs else staffs.filter(is_manager=True).first()

    def get_co_manager_position(self):
        staffs = getattr(self, "staffs", None)
        return None if not staffs else staffs.filter(is_co_manager=True).first()


class Position(MPTTModel):

    objects = PositionManager()
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    parent = TreeForeignKey(
        "Position",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="chair_upline",
        verbose_name=_("Upline"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )
    department = TreeForeignKey(
        Department,
        related_name="staffs",
        on_delete=models.PROTECT,
        verbose_name=_("Department"),
    )
    is_manager = models.BooleanField(
        default=False,
        verbose_name=_("Is Manager"),
    )
    is_co_manager = models.BooleanField(
        default=False,
        verbose_name=_("Is Co-Manager"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
    )
    employee_required = models.IntegerField(
        default=1,
        verbose_name=_("Employee required"),
    )
    # TODO File Management
    # attachment = models.ForeignKey(
    #     Document, null=True, blank=True,
    #     on_delete=models.SET_NULL)

    class Meta:
        db_table = "simpel_employs_position"
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")

    def get_strips(self):
        return "---" * self.level

    def get_active_chairman(self, max_person=5):
        chairmans = getattr(self, "chairmans", None)
        if not chairmans:
            return None
        if self.is_manager or self.is_co_manager:
            return chairmans.filter(is_active=True).first()
        else:
            return chairmans.filter(is_active=True)[0:max_person]

    def __str__(self):
        return self.name


class Employment(models.Model):

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )
    note = models.TextField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_("Note"),
    )

    class Meta:
        db_table = "simpel_employs_employment"
        verbose_name = _("Employment")
        verbose_name_plural = _("Employments")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Employment, self).save(*args, **kwargs)


class Employee(NumeratorMixin):

    doc_prefix = "EMP"

    eid = models.CharField(
        null=True,
        blank=False,
        max_length=255,
        verbose_name=_("Employee ID"),
    )
    employment = models.ForeignKey(
        Employment,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_("Employment"),
    )
    date_registered = models.DateField(
        default=timezone.now,
        verbose_name=_("Date registered"),
    )
    # TODO File Management
    # attachment = models.ForeignKey(
    #     Document, on_delete=models.SET_NULL, null=True, blank=True,
    #     verbose_name=_('Attachment'), help_text=_('Contract Document'))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
    )

    class Meta:
        db_table = "simpel_employs_employee"
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return str(self.person)

    def natural_key(self):
        natural_key = (self.eid,)
        return natural_key

    def get_anchestors(self, ascending=True):
        return self.position.get_ancestors(ascending=ascending)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Chair(models.Model):
    STRUCTURAL = "struct"
    FUNCTIONAL = "func"
    GROUP = (
        (STRUCTURAL, _("Structural")),
        (FUNCTIONAL, _("Functional")),
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    group = models.CharField(
        choices=GROUP,
        default=STRUCTURAL,
        max_length=6,
        db_index=True,
    )
    employee = models.ForeignKey(
        Employee,
        related_name="positions",
        on_delete=models.CASCADE,
        verbose_name=_("Employee"),
    )
    position = TreeForeignKey(
        Position,
        related_name="chairmans",
        on_delete=models.CASCADE,
        verbose_name=_("Position"),
    )
    from_date = models.DateField(
        default=timezone.now,
        editable=True,
    )
    to_date = models.DateField(
        default=timezone.now,
        null=True,
        blank=True,
        editable=True,
    )
    active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
    )

    class Meta:
        db_table = "simpel_employs_chair"
        verbose_name = _("Chair")
        verbose_name_plural = _("Chairs")
