from protocols import reports_6_0_0
from protocols import reports_5_0_0
from protocols import reports_4_0_0
from protocols import reports_3_0_0
from protocols.tests.test_migration.base_test_migration import TestCaseMigration
# forward migrations
from protocols.migration.migration_reports_3_0_0_to_reports_4_0_0 import MigrateReports3To4
from protocols.migration.migration_reports_4_0_0_to_reports_5_0_0 import MigrateReports400To500
from protocols.migration.migration_reports_5_0_0_to_reports_6_0_0 import MigrateReports500To600
# reverse migrations
from protocols.migration.migration_reports_6_0_0_to_reports_5_0_0 import MigrateReports600To500
from protocols.migration.migration_reports_5_0_0_to_reports_4_0_0 import MigrateReports500To400
from protocols.migration.migration_reports_4_0_0_to_reports_3_0_0 import MigrateReports400To300


class TestRoundTripMigrateReports300To600(TestCaseMigration):

    def test_migrate_clinical_report_rd(self):
        cr_rd_3 = self.get_valid_object(
            object_type=reports_3_0_0.ClinicalReportRD, version=self.version_3_0_0, fill_nullables=True
        )
        cr_rd_3.interpretationRequestVersion = '42'

        original_json = cr_rd_3.toJsonDict()

        # Forward migration to version 6
        cr_rd_4 = MigrateReports3To4().migrate_clinical_report_rd(old_clinical_report_rd=cr_rd_3)
        self.assertIsInstance(cr_rd_4, reports_4_0_0.ClinicalReportRD)
        self.assertTrue(cr_rd_4.validate(cr_rd_4.toJsonDict()))
        cr_rd_5 = MigrateReports400To500().migrate_clinical_report_rd(old_instance=cr_rd_4, assembly=reports_5_0_0.Assembly.GRCh38)
        self.assertIsInstance(cr_rd_5, reports_5_0_0.ClinicalReportRD)
        self.assertTrue(cr_rd_5.validate(cr_rd_5.toJsonDict()))
        cr_rd_6 = MigrateReports500To600().migrate_clinical_report_rd(old_instance=cr_rd_5)
        self.assertIsInstance(cr_rd_6, reports_6_0_0.ClinicalReport)
        self.assertTrue(cr_rd_6.validate(cr_rd_6.toJsonDict()))

        # Reverse migration back to version 3
        cr_rd_5 = MigrateReports600To500().migrate_clinical_report_rd(old_instance=cr_rd_6)
        self.assertIsInstance(cr_rd_5, reports_5_0_0.ClinicalReportRD)
        self.assertTrue(cr_rd_5.validate(cr_rd_5.toJsonDict()))
        cr_rd_4 = MigrateReports500To400().migrate_clinical_report_rd(old_instance=cr_rd_5)
        self.assertIsInstance(cr_rd_4, reports_4_0_0.ClinicalReportRD)
        self.assertTrue(cr_rd_4.validate(cr_rd_4.toJsonDict()))
        cr_rd_3 = MigrateReports400To300().migrate_clinical_report_rd(old_instance=cr_rd_4)
        self.assertIsInstance(cr_rd_3, reports_3_0_0.ClinicalReportRD)
        self.assertTrue(cr_rd_3.validate(cr_rd_3.toJsonDict()))

        round_trip_json = cr_rd_3.toJsonDict()

        self.assertDictEqual(original_json, round_trip_json)

    # def test_migrate_interpretation_request_rd(self):
    #     self._check_rd(fill_nullables=True)
    #
    # def test_migrate_interpretation_request_cancer(self):
    #     self._check_cancer(fill_nullables=True)
    #
    # def test_migrate_interpretation_request_rd_with_nulls(self):
    #     self._check_rd(fill_nullables=False)
    #
    # def test_migrate_interpretation_request_cancer_with_nulls(self):
    #     self._check_cancer(fill_nullables=False)
    #
    # def _check_cancer(self, fill_nullables):
    #     self._check_round_trip_migration(
    #         MigrateReports500To600().migrate_interpretation_request_cancer,
    #         MigrateReports600To500().migrate_interpretation_request_cancer,
    #         self.old_model.CancerInterpretationRequest,
    #         self.new_model.CancerInterpretationRequest,
    #         fill_nullables=fill_nullables
    #     )
    #
    # def _check_rd(self, fill_nullables):
    #     self._check_round_trip_migration(
    #         MigrateReports500To600().migrate_interpretation_request_rd,
    #         MigrateReports600To500().migrate_interpretation_request_rd,
    #         self.old_model.InterpretationRequestRD,
    #         self.new_model.InterpretationRequestRD,
    #         fill_nullables=fill_nullables
    #     )
    #
    # def _check_round_trip_migration(self, forward, backward, original_type, new_type, fill_nullables):
    #     original = self.get_valid_object(object_type=original_type, version=self.version_6_1, fill_nullables=fill_nullables)
    #
    #     original.versionControl = self.old_model.ReportVersionControl()  # to set the right default
    #
    #     migrated = forward(old_instance=original)
    #     self.assertIsInstance(migrated, new_type)
    #     self.assertTrue(migrated.validate(migrated.toJsonDict()))
    #
    #     round_tripped = backward(old_instance=migrated)
    #     self.assertIsInstance(round_tripped, original_type)
    #     self.assertTrue(round_tripped.validate(migrated.toJsonDict()))
    #     self.assertEqual(round_tripped.toJsonDict(), original.toJsonDict())
