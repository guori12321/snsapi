# -*- coding: utf-8 -*-

__author__ = 'hupili'
__copyright__ = 'Unlicensed'
__license__ = 'Unlicensed'
__version__ = '0.1'
__maintainer__ = 'hupili'
__email__ = 'hpl1989@gmail.com'
__status__ = 'development'

from nose.tools import ok_
from nose.tools import eq_
from test_config import *
from test_utils import *
from snsapi.snsbase import SNSBase

sys.path = [DIR_TEST] + sys.path

class TestSNSBase(TestBase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_snsbase_new_channel_normal(self):
        nc = SNSBase.new_channel()
        eq_(2, len(nc), WRONG_RESULT_ERROR)
        in_('channel_name', nc)
        in_('open', nc)

    def test_snsbase_new_channel_full(self):
        nc = SNSBase.new_channel(full=True)
        eq_(4, len(nc), WRONG_RESULT_ERROR)
        in_('channel_name', nc)
        in_('open', nc)
        in_('description', nc)
        in_('methods', nc)

    def _build_sns_with_token(self, seconds_after_current_time):
        from snsapi.utils import JsonDict
        import time
        token = JsonDict()
        token.expires_in = time.time() + seconds_after_current_time
        sns = SNSBase()
        sns.token = token
        return sns

    def test_snsbase_expire_after_1(self):
        # Before expiration
        gt_(self._build_sns_with_token(2).expire_after(), 1.5)
        gt_(self._build_sns_with_token(20).expire_after(), 19.5)

    def test_snsbase_expire_after_2(self):
        # On or after expiration
        eq_(self._build_sns_with_token(0).expire_after(), 0)
        eq_(self._build_sns_with_token(-2).expire_after(), 0)
        eq_(self._build_sns_with_token(-20).expire_after(), 0)

    def test_snsbase_expire_after_3(self):
        # Token not exist, consider as expired. 
        eq_(SNSBase().expire_after(), 0)

    def test_snsbase_is_expired(self):
        nok_(self._build_sns_with_token(2).is_expired())
        ok_(self._build_sns_with_token(-2).is_expired())

    def test_snsbase_is_authed(self):
        ok_(self._build_sns_with_token(2).is_authed())
        nok_(self._build_sns_with_token(-2).is_authed())

