import pytest

from app.models import StartDocType
from app.start_docs.forms import NewStartDocTypeForm
from app.start_docs.start_docs_utils import add_start_doc_type, change_start_doc_type_name
from app.tests.utils import create


@pytest.mark.usefixtures("db_session", "context")
def test_add_start_doc_type():
    form = NewStartDocTypeForm()
    form.name.data = "sample name"

    assert form.name.data not in [doctype.name for doctype in StartDocType.query.all()]
    assert add_start_doc_type(form) is True

    assert form.name.data in [doctype.name for doctype in StartDocType.query.all()]
    assert add_start_doc_type(form) is False


def test_change_start_doc_type_name(sample_start_doc_type):
    name = sample_start_doc_type.name
    changed = "changed name"
    data = {
        "name": name,
        "changed": changed
    }

    assert change_start_doc_type_name(data) is True
    assert sample_start_doc_type.name == changed

    another_type = StartDocType(name="another name")
    create(another_type)

    data["name"] = changed
    data["changed"] = another_type.name
    assert change_start_doc_type_name(data) is False
