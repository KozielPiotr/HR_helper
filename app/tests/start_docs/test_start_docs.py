import pytest

from app.models import StartDocType
from app.start_docs.forms import NewStartDocTypeForm
from app.start_docs.start_docs_utils import add_start_doc_type


@pytest.mark.usefixtures("db_session", "context")
def test_add_start_doc_type():
    form = NewStartDocTypeForm()
    form.name.data = "sample name"

    assert form.name.data not in [doctype.name for doctype in StartDocType.query.all()]
    assert add_start_doc_type(form) is True

    assert form.name.data in [doctype.name for doctype in StartDocType.query.all()]
    assert add_start_doc_type(form) is False
