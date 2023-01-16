from aliyunsdkcore import client
from aliyunsdkcas.request.v20200407 import UploadUserCertificateRequest
from aliyunsdkcas.request.v20200407 import ListUserCertificateOrderRequest
from aliyunsdkcas.request.v20200407 import DeleteUserCertificateRequest
from aliyunsdkcdn.request.v20180510 import DescribeCdnHttpsDomainListRequest
from aliyunsdkcdn.request.v20180510 import SetDomainServerCertificateRequest
from aliyunsdkcdn.request.v20180510 import DescribeDomainCertificateInfoRequest
from aliyunsdkcore.acs_exception.exceptions import ServerException
from datetime import datetime
import argparse
import json
import os


class AutoSSL:

    def __init__(self, *args, **kwargs):
        self._region = kwargs['region'] if 'region' in kwargs else ''
        self._access_key_id = kwargs['access_key_id'] if 'access_key_id' in kwargs else ''
        self._access_key_secret = kwargs['access_key_secret'] if 'access_key_secret' in kwargs else ''
        self._acs_client = client.AcsClient(
            self._access_key_id, self._access_key_secret, self._region)

    def get_https_domain_list(self):
        try:
            req = DescribeCdnHttpsDomainListRequest.DescribeCdnHttpsDomainListRequest()
            result = self._acs_client.do_action_with_exception(req)
        except ServerException as e:
            print('Error:' + e)

        data = json.loads(result)
        domain_list = data['CertInfos']['CertInfo']
        domain_list

    def get_domain_cert_info(self, domain_name):
        try:
            req = DescribeDomainCertificateInfoRequest.DescribeDomainCertificateInfoRequest()
            req.set_DomainName(domain_name)

            result = self._acs_client.do_action_with_exception(req)
        except ServerException as e:
            print('Error:' + e)
        else:
            return json.loads(result)

    def set_domain_server_cert(self, domain_name, cert_name):
        try:
            req = SetDomainServerCertificateRequest.SetDomainServerCertificateRequest()
            req.set_accept_format('json')
            req.set_DomainName(domain_name)
            req.set_CertName(cert_name)
            req.set_ServerCertificateStatus('on')
            req.set_CertType("cas")
            result = self._acs_client.do_action_with_exception(req)
        except ServerException as e:
            print('Error:' + e)
        else:
            return json.loads(result)

    def upload_user_cert(self, domain, cert_path, key_path):
        try:
            cert_name = domain + '-'+datetime.now().strftime("%Y%m%d")
            req = UploadUserCertificateRequest.UploadUserCertificateRequest()
            req.set_Name(cert_name)

            with open(cert_path, 'r') as f:
                req.set_Cert(f.read())

            with open(key_path, 'r') as f:
                req.set_Key(f.read())

            result = self._acs_client.do_action_with_exception(req)
        except ServerException as e:
            print('Error:' + e)
        else:
            print(result)
            return cert_name

    def delete_user_cert(self, cert_id):
        try:
            req = DeleteUserCertificateRequest.DeleteUserCertificateRequest()
            req.set_CertId(cert_id)
            result = self._acs_client.do_action_with_exception(req)
        except ServerException as e:
            print('Error:' + e)
        else:
            return json.loads(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Auto Aliyun CDN SSL', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-access_key_id", "--access_key_id",
                        help="阿里云access_key_id", required=True)
    parser.add_argument("-access_key_secret",
                        "--access_key_secret", help="阿里云access_key_secret", required=True)
    parser.add_argument("-region", "--region",
                        help="地区", default='cn-hangzhou')
    parser.add_argument("-domain", "--domain", help="域名", required=True)
    parser.add_argument("-cert_path", "--cert_path",
                        required=True, help="cert证书路径")
    parser.add_argument("-key_path", "--key_path",
                        required=True, help="cert key路径")
    parser.add_argument("-reset_days", "--reset_days",
                        default=10, help="证书更新周期")

    args = parser.parse_args()
    AutoSSL(access_key_id=args.access_key_id,
            access_key_secret=args.access_key_secret,
            region=args.region,
            domain=args.domain,
            cert_path=args.cert_path,
            cert_key_path=args.cert_key_path,
            reset_days=args.reset_days)
