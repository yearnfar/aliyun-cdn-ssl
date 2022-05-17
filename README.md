## 自动更新阿里云CDN https证书

### 安装依赖

pip install -r requirements.txt


### 更新证书

请把{access_key_id},{access_key_secret},{region},{domain},{cert_path},{cert_key_path}替换为你自己的配置

```
python aliyun-cdn-ssl.py -access_key_id {access_key_id} -access_key_secret {access_key_secret} -region {region} -domain {domain} -cert_path {cert_path} -cert_key_path {cert_key_path} 
```



