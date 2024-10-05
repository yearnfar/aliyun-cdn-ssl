#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aliyunsdkcore import client
from aliyunsdkcdn.request.v20180510 import SetDomainServerCertificateRequest
from aliyunsdkcdn.request.v20180510 import DescribeDomainCertificateInfoRequest
from aliyunsdkcore.acs_exception.exceptions import ServerException
from datetime import datetime
import json
import argparse
import os
import yaml
import time


def auto_ssl(access_key_id, access_key_secret, region, domain, cert_path, cert_key_path):
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

        is_ok = False    
        if 'CertExpireTime' in info: 
            current_time = datetime.now()
            expired_time = datetime.strptime(info['CertExpireTime'], "%Y-%m-%dT%H:%M:%SZ")

            left_days = (expired_time - current_time).days
            if left_days < 10:
               is_ok=True 
               print("证书剩余%d天，更新证书..." % left_days)
            elif left_days < 60:
                cert_time=time.localtime(os.path.getmtime(cert_path))
                if (current_time-cert_time).days <= 30:
                    is_ok=True
                    print("本地证书文件有变动，开始更新证书...")
            else:
                print("证书剩余%d天，剩余时间充足，不更新证书" % left_days)
        else:
            is_ok=True
            print("无法获取证书信息，开始更新证书...")

        if is_ok==False:
            return

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
    parser = argparse.ArgumentParser(description='Auto Aliyun CDN SSL', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-config", "--config", help="配置文件", default='/app/config.yaml')

    args = parser.parse_args()
    cfg_file = args.config
    cfg_path = os.path.dirname(cfg_file)

    with open(cfg_file, 'r', encoding='utf-8') as f:
        cdn_cfg = yaml.load(f, Loader=yaml.FullLoader)
        for cfg in cdn_cfg:
            for domain in cfg['domains']:
                cert_path= os.path.join(cfg_path, cfg['cert_path'])
                cert_key_path = os.path.join(cfg_path, cfg['cert_key_path'])
                auto_ssl(cfg['access_key_id'], cfg['access_key_secret'], cfg['region'], domain, cert_path, cert_key_path)      

