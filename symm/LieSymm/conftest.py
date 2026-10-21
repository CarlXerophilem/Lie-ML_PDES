"""Archived tests are evidence inputs, not a second executable test tree."""


def pytest_ignore_collect(collection_path, config):
    return collection_path.name == "_snapshot"
