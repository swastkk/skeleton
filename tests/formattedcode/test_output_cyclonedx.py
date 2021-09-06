# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import os

from commoncode.testcase import FileDrivenTesting
from formattedcode.output_cyclonedx import *
from scancode.cli_test_utils import run_scan_click

test_env = FileDrivenTesting()
test_env.test_data_dir = os.path.join(os.path.dirname(__file__), 'data')


def test_can_encode_component():
    purl = "pkg:generic/test@1"
    hashes = [CycloneDxHashObject(alg="MD5", content="not-a-hash")]
    licenses = [
        CycloneDxLicenseEntry(expression="MIT or Apache-2.0"),
        CycloneDxLicenseEntry(license=CycloneDxLicense(id="MIT"))
    ]
    component = CycloneDxComponent(name="test", version="1", purl=purl,
                                   bom_ref=purl, hashes=hashes, licenses=licenses)
    json_repr = CycloneDxEncoder().encode(component)
    expected_json_repr = '{"name": "test", "version": "1", ' \
                         '"purl": "pkg:generic/test@1", ' \
                         '"hashes": [{"alg": "MD5", "content": "not-a-hash"}], ' \
                         '"licenses": [{"expression": "MIT or Apache-2.0"}, ' \
                         '{"license": {"id": "MIT"}}], ' \
                         '"type": "library", "bom-ref": "pkg:generic/test@1"}'
    assert json_repr == expected_json_repr


def test_get_author_from_parties():
    parties = [
        {
            "type": "person",
            "role": "author",
            "name": "the author"
        }
    ]
    author = get_author_from_parties(parties)
    assert author == "the author"


def test_get_author_from_parties_default_none():
    parties = [
        {
            "type": "person",
            "role": "maintainer",
            "name": "the maintainer"
        }
    ]
    assert get_author_from_parties(parties) is None


def test_get_licenses_from_package():
    package = {
        "license_expression": "mit",
        "declared_license": ["MIT"]
    }
    licenses = get_licenses(package)
    # check if duplicate entries are removed
    assert len(licenses) == 1
    assert licenses[0].license.id == "MIT"


def test_can_get_hashes_from_package():
    package = {
        "md5": "cc5ea2445954a282f622042252a6eef9",
        "sha1": "b754cee9a3d3501d32ae200e07f4e518cd8294b8",
        "sha256": "4795dae6518d60e4e5bd7103f50f5f86f8c07cbdc36aa76f410a0d534edc8ec5",
        "sha512": "f385a335b20e0bd933b3d59abc41e9b05f4333db6cd948b579b2562" +
                  "d617a6fa35e13ffa0c2eceae031afcf73c5fb7e1660fade207ddf2a0e312e006eb115e9b0"}
    hashes = get_hashes_list(package=package)
    assert len(hashes) == 4
    for hash_entry in hashes:
        assert hash_entry.content is not None


def test_cyclonedx_json():
    test_dir = test_env.get_test_loc('json/simple')
    result_file = test_env.get_temp_file('cyclonedx')
    args = ['-p', test_dir, '--cyclonedx-json', result_file]
    run_scan_click(args)

def test_cyclonedx_xml():
    pass