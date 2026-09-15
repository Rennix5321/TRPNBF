import pytest
from storage import load_incidents, save_incidents

def test_save_and_load(tmp_path):
    filename = tmp_path / "data" / "incidents.json"
    data = [{"id": 1, "title": "Сбой"}]
    save_incidents(filename, data)
    assert load_incidents(filename) == data

def test_missing_file(tmp_path):
    assert load_incidents(tmp_path / "missing.json") == []

def test_invalid_json(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("{broken", encoding="utf-8")
    with pytest.raises(ValueError):
        load_incidents(filename)
