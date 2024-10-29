openssl x509 -req\
 -days 365\
 -in solar_yn.csr\
 -CAkey data53_private_key.pem\
 -CA data53_root_cert.crt\
 -out solar_yn.crt\
 -set_serial 123456789\
 -extfile v3.ext