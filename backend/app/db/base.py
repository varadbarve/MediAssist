# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.patient import Patient  # noqa
from app.models.report import Report  # noqa
from app.models.prescription import Prescription  # noqa
from app.models.user import User  # noqa
from app.models.audit_log import AuditLog  # noqa
