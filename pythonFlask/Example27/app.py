from werkzeug.security import generate_password_hash,check_password_hash

hash=generate_password_hash("1234")
print(hash)


print(check_password_hash(hash,"1234"))   # True
print(check_password_hash(hash,"9999"))   # False