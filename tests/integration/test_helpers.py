import json
import os
import unittest

from pathlib import Path
from unittest import mock

from secator.utils_test import load_fixture, FIXTURES_DIR, clear_modules
from secator.tasks._categories import Vuln
from secator.config import CONFIG


class TestHelpers(unittest.TestCase):

	def test_lookup_cve_circle(self):
		fixture = json.dumps(load_fixture('cve_circle_output', FIXTURES_DIR), sort_keys=True)
		cve_path = f'{CONFIG.dirs.data}/cves/CVE-2023-5568.json'
		if Path(cve_path).exists():
			Path(cve_path).unlink()  # make sure we don't use cache data
		actual = json.dumps(Vuln.lookup_cve_from_cve_circle('CVE-2023-5568'), sort_keys=True)
		self.assertEqual(actual, fixture)

	def test_lookup_cve_from_ghsa_no_cve_id(self):
		actual = Vuln.lookup_cve_from_ghsa('GHSA-ggpf-24jw-3fcw')
		self.assertIsNone(actual)

	@mock.patch.dict(os.environ, {'SECATOR_RUNNERS_SKIP_CVE_SEARCH': '0'})
	def test_lookup_cve_from_ghsa(self):
		clear_modules()
		from secator.tasks._categories import Vuln
		actual = Vuln.lookup_cve_from_ghsa('GHSA-w596-4wvx-j9j6')
		self.assertIsNotNone(actual)
		self.assertEqual(actual['id'], 'CVE-2022-42969')
