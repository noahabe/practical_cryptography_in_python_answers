# generate the key first

openssl genpkey -algorithm RSA -out research_key.pem -pkeyopt rsa_keygen_bits:2048

# create a csr from the key

openssl req -new -key research_key.pem -out research_yn.csr