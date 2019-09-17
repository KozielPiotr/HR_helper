import pytest

from hr_helper.models import StartDocType, StartDoc
from hr_helper.start_docs.forms import NewStartDocTypeForm
from hr_helper.start_docs.start_docs_utils import add_start_doc_type, change_start_doc_type_name, remove_start_doctype
from hr_helper.tests.utils import create


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

    data["name"] = another_type.name
    data["changed"] = changed
    assert change_start_doc_type_name(data) is False


def test_delete_doctype(sample_worker, sample_start_doc, sample_start_doc_type):
    sample_start_doc.start_doc_type = sample_start_doc_type.id
    assert sample_start_doc in sample_start_doc_type.docs
    sample_start_doc.worker_id = sample_worker.id
    assert sample_start_doc in sample_worker.start_docs

    remove_start_doctype(sample_start_doc_type.id)

    assert sample_start_doc_type not in StartDocType.query.all()
    assert sample_start_doc not in StartDoc.query.all()
    assert sample_start_doc not in sample_worker.start_docs
