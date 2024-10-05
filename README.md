## 自动更新阿里云CDN https证书

符合下面任意一个条件，则更新证书：
- 通过阿里云SDK，查询到证书过期时间，如果剩余时间小于10天，则自动更新证书。
- 如果cert_path的证书最近30天内有修改，且阿里云查询的证书剩余时间小于60天，则自动更新证书。

### 安装依赖

pip install -r requirements.txt


### 更新证书

请把{access_key_id},{access_key_secret},{region},{domain},{cert_path},{cert_key_path}替换为你自己的配置

```
python aliyun-cdn-ssl.py -access_key_id {access_key_id} -access_key_secret {access_key_secret} -region {region} -domain {domain} -cert_path {cert_path} -cert_key_path {cert_key_path} 
```



