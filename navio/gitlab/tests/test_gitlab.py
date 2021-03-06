import pytest
import os
import sys


class TestImport:

    def test_import(self):
        import navio.gitlab
        from navio.gitlab import Gitlab


class Test:

    def test_is_gitlab(self):
        from navio.gitlab import Gitlab

        os.environ.pop('CI', None)
        assert not Gitlab('', private_token='...').is_gitlab()

        os.environ['CI'] = 'true'
        assert Gitlab('', private_token='...').is_gitlab()

        os.environ['CI'] = 'false'
        assert not Gitlab('', private_token='...').is_gitlab()

        os.environ['CI'] = '???'
        assert not Gitlab('', private_token='...').is_gitlab()

    def test_is_pull_request(self):
        from navio.gitlab import Gitlab

        os.environ.pop('CI_MERGE_REQUEST_ID', None)
        assert not Gitlab('', private_token='...').is_pull_request()

        os.environ['CI'] = 'true'

        os.environ['CI_MERGE_REQUEST_ID'] = '123'
        assert Gitlab('', private_token='...').is_pull_request()

        os.environ['CI_MERGE_REQUEST_ID'] = '456'
        assert Gitlab('', private_token='...').is_pull_request()

        os.environ['CI_MERGE_REQUEST_ID'] = '???'
        assert Gitlab('', private_token='...').is_pull_request()

    def test_branch(self):
        from navio.gitlab import Gitlab

        os.environ['CI'] = 'true'
        os.environ.pop('CI_COMMIT_BRANCH', None)

        assert Gitlab('', private_token='...').branch() is None

        os.environ['CI_COMMIT_BRANCH'] = 'master'
        assert 'master' == Gitlab('', private_token='...').branch()

        os.environ['CI_COMMIT_BRANCH'] = 'prod'
        assert 'prod' == Gitlab('', private_token='...').branch()

    def test_commit_hash(self):
        from navio.gitlab import Gitlab

        os.environ['CI'] = 'true'
        os.environ.pop('CI_COMMIT_SHA', None)

        assert '000000000000000000000000000000' == Gitlab('', private_token='...').commit_hash()

        os.environ['CI_COMMIT_SHA'] = '1f510ab451bb4'
        assert '1f510ab451bb4' == Gitlab('', private_token='...').commit_hash()

        os.environ['CI_COMMIT_SHA'] = '04124124bcb131'
        assert '04124124bcb131' == Gitlab('', private_token='...').commit_hash()

    def test_short_commit_hash(self):
        from navio.gitlab import Gitlab

        os.environ['CI'] = 'true'
        os.environ.pop('CI_COMMIT_SHA', None)

        assert '0000000' == Gitlab('', private_token='...').short_commit_hash()

        os.environ['CI_COMMIT_SHA'] = '1f510ab451bb4'
        assert '1f510ab' == Gitlab('', private_token='...').short_commit_hash()

        os.environ['CI_COMMIT_SHA'] = '04124124bcb131'
        assert '0412412' == Gitlab('', private_token='...').short_commit_hash()
