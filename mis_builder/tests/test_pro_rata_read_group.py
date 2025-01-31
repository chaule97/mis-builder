# Copyright 2025 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo_test_helper import FakeModelLoader

from odoo.tests import TransactionCase


class TestProrataReadGroup(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .fake_models import ProrataReadGroupThing

        cls.loader.update_registry((ProrataReadGroupThing,))
        cls.addClassCleanup(cls.loader.restore_registry)

        cls.thing_model = cls.env["prorata.read.group.thing"]
        cls.thing_model.create(
            {
                "date_from": "2024-01-01",
                "date_to": "2024-01-05",
                "account_code": "A1",
                "debit": 7,
                "credit": 0,
            }
        )
        cls.thing_model.create(
            {
                "date_from": "2024-01-01",
                "date_to": "2024-01-20",
                "account_code": "A1",
                "debit": 200,
                "credit": 0,
            }
        )
        cls.thing_model.create(
            {
                "date_from": "2024-01-15",
                "date_to": "2024-01-20",
                "account_code": "A1",
                "debit": 11,
                "credit": 0,
            }
        )

    def test_create(self):
        data = self.thing_model.read_group(
            [("date", ">=", "2024-01-11"), ("date", "<=", "2024-01-20")],
            fields=["debit", "credit", "account_code"],
            groupby=["account_code"],
        )[0]
        self.assertEqual(data["debit"], 111)
        self.assertEqual(data["credit"], 0)
        self.assertEqual(data["account_code"], "A1")
