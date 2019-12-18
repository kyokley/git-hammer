import os

from githammer import iter_sources_and_tests

from .hammer_test import HammerTest


class HammerRepositoryTest(HammerTest):

    def setUp(self):
        super().setUp()
        self.hammer.add_repository(os.path.join(self.current_directory, 'data', 'repository'),
                                   os.path.join(self.current_directory, 'data', 'repo-config.json'))

    def test_project_name_is_property_of_hammer_object(self):
        self.assertEqual(self.hammer.project_name, 'test')

    def test_repository_is_processed_into_database_after_adding(self):
        self.assertIsNotNone(self.hammer.head_commit())

    def test_commit_timestamps_have_correct_time(self):
        initial_commit = self._fetch_commit(HammerRepositoryTest._main_repo_initial_commit_hexsha)
        print(initial_commit.commit_time_tz())
        self.assertEqual(initial_commit.commit_time_tz().hour, 11)

    def test_initial_commit_line_counts_are_correct(self):
        initial_commit = self._fetch_commit(HammerRepositoryTest._main_repo_initial_commit_hexsha)
        author = initial_commit.author
        self.assertEqual(initial_commit.line_counts[author], 14)

    def test_second_commit_line_counts_are_correct(self):
        initial_commit = self._fetch_commit(HammerRepositoryTest._main_repo_initial_commit_hexsha)
        second_commit = self._fetch_commit(HammerRepositoryTest._main_repo_second_commit_hexsha)
        self.assertEqual(second_commit.line_counts[initial_commit.author], 10)
        self.assertEqual(second_commit.line_counts[second_commit.author], 4)

    def test_sources_are_iterated_based_on_configuration(self):
        repository_path = os.path.join(self.current_directory, 'data', 'repository')
        configuration_path = os.path.join(self.current_directory, 'data', 'repo-config.json')
        files = list(iter_sources_and_tests(repository_path, configuration_path))
        file_names = [name for (file_type, name) in files]
        self.assertIn(('source-file', 'file1.txt'), files)
        self.assertNotIn('file.dat', file_names)
