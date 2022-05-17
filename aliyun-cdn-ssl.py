from aliyunsdkcore import client
from aliyunsdkcdn.request.v20180510 import SetDomainServerCertificateRequest
from aliyunsdkcdn.request.v20180510 import DescribeDomainCertificateInfoRequest
from aliyunsdkcore.acs_exception.exceptions import ServerException
from datetime import datetime
import json
import argparse


def auto_ssl(access_key_id='', access_key_secret='', region='cn-hangzhou', domain='', cert_path='', cert_key_path='',  reset_days=10):
    acs_client = client.AcsClient(access_key_id, access_key_secret, region)
    try:
        req = DescribeDomainCertificateInfoRequest.DescribeDomainCertificateInfoRequest()
        req.set_DomainName(domain)
        result = acs_client.do_action_with_exception(req)
        json_res = json.loads(result)
        # print(jsonRes)
        info = json_res['CertInfos']['CertInfo'][0] if len(
            json_res['CertInfos']['CertInfo']) > 0 else {}
        print(info['CertExpireTime'])

        current_time = datetime.now()
        if info['CertExpireTime'] != '':
            expired_time = datetime.strptime(
                info['CertExpireTime'], "%Y-%m-%dT%H:%M:%SZ")

            left_days = (expired_time - current_time).days
            if left_days > reset_days:
                print("证书剩余%d天，剩余时间充足，不更新证书" % left_days)
                return
            print("证书剩余%d天，开始更新证书..." % left_days)
        else:
            print("无法获取证书信息，开始更新证书...")

        req = SetDomainServerCertificateRequest.SetDomainServerCertificateRequest()
        req.set_accept_format('json')
        req.set_DomainName(domain)
        req.set_CertName(domain + '-' + current_time.strftime("%Y%m%d"))
        req.set_ServerCertificateStatus('on')

        with open(cert_path, 'r') as f:
            req.set_ServerCertificate(f.read())

        with open(cert_key_path, 'r') as f:
            req.set_PrivateKey(f.read())

        result = acs_client.do_action_with_exception(req)
        print(result)
    except ServerException as e:
        print('Error:' + e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Auto Aliyun CDN SSL', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-access_key_id", "--access_key_id",
                        help="阿里云access_key_id", required=True)
    parser.add_argument("-access_key_secret",
                        "--access_key_secret", help="阿里云access_key_secret", required=True)
    parser.add_argument("-region", "--region", help="地区", default='cn-hangzhou')
    parser.add_argument("-domain", "--domain", help="域名", required=True)
    parser.add_argument("-cert_path", "--cert_path",
                        required=True, help="cert证书路径")
    parser.add_argument("-cert_key_path", "--cert_key_path",
                        required=True, help="cert key路径")
    parser.add_argument("-reset_days", "--reset_days",
                        default=10, help="证书更新周期")

    args = parser.parse_args()
    auto_ssl(access_key_id=args.access_key_id,
             access_key_secret=args.access_key_secret,
             region=args.region,
             domain=args.domain,
             cert_path=args.cert_path,
             cert_key_path=args.cert_key_path,
             reset_days=args.reset_days)
