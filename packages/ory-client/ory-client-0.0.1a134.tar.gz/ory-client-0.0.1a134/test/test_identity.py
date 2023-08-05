"""
    Ory APIs

    Documentation for all public and administrative Ory APIs. Administrative APIs can only be accessed with a valid Personal Access Token. Public APIs are mostly used in browsers.   # noqa: E501

    The version of the OpenAPI document: v0.0.1-alpha.134
    Contact: support@ory.sh
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import ory_client
from ory_client.model.identity_credentials import IdentityCredentials
from ory_client.model.identity_state import IdentityState
from ory_client.model.recovery_address import RecoveryAddress
from ory_client.model.verifiable_identity_address import VerifiableIdentityAddress
globals()['IdentityCredentials'] = IdentityCredentials
globals()['IdentityState'] = IdentityState
globals()['RecoveryAddress'] = RecoveryAddress
globals()['VerifiableIdentityAddress'] = VerifiableIdentityAddress
from ory_client.model.identity import Identity


class TestIdentity(unittest.TestCase):
    """Identity unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testIdentity(self):
        """Test Identity"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Identity()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
