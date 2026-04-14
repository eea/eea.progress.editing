"""Integration tests for eea.progress.editing REST API views

Uses direct view instantiation to test without RelativeSession.
"""

import unittest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from transaction import commit
from eea.progress.editing.tests.base import FUNCTIONAL_TESTING


class TestEditingProgressSetup(unittest.TestCase):
    """Test eea.progress.editing installation"""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_product_installed(self):
        """Test that eea.progress.editing is installed"""
        from Products.CMFPlone.utils import get_installer

        installer = get_installer(self.portal, self.layer["request"])
        self.assertTrue(installer.is_product_installed("eea.progress.editing"))

    def test_portal_exists(self):
        """Test that portal is set up"""
        self.assertIsNotNone(self.portal)


class TestEditingProgressView(unittest.TestCase):
    """Test editing.progress view classes"""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_editing_progress_adapter_registered(self):
        """Test that EditingProgress adapter class exists"""
        from eea.progress.editing.restapi.get import EditingProgress

        self.assertIsNotNone(EditingProgress)

    def test_editing_progress_on_site_root(self):
        """Test EditingProgress on site root returns basic structure"""
        from eea.progress.editing.restapi.get import EditingProgress

        ep = EditingProgress(self.portal, self.portal.REQUEST)
        result = ep(expand=False)
        self.assertIn("editing.progress", result)
        self.assertIn("@id", result["editing.progress"])

    def test_editing_progress_get_class_exists(self):
        """Test that EditingProgressGet class exists"""
        from eea.progress.editing.restapi.get import EditingProgressGet

        self.assertIsNotNone(EditingProgressGet)


class TestEditingProgressOnDocument(unittest.TestCase):
    """Test editing.progress on content objects"""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "test-doc", title="Test Document")
        commit()

    def test_editing_progress_on_document(self):
        """Test EditingProgress on a Document"""
        from eea.progress.editing.restapi.get import EditingProgress

        doc = self.portal["test-doc"]
        ep = EditingProgress(doc, self.portal.REQUEST)
        result = ep(expand=True)
        self.assertIn("editing.progress", result)

    def test_editing_progress_has_done_on_document(self):
        """Test that EditingProgress on Document has done field"""
        from eea.progress.editing.restapi.get import EditingProgress

        doc = self.portal["test-doc"]
        ep = EditingProgress(doc, self.portal.REQUEST)
        result = ep(expand=True)
        self.assertIn("done", result["editing.progress"])


if __name__ == "__main__":
    unittest.main()
