from boto.s3.connection import S3Connection

with open('passwords.txt', 'r') as f:
    access = f.readline().strip()
    password = f.readline().strip()
    print(access)
    print(password)
    
conn = S3Connection(access, password)
bucket = conn.get_bucket('emrec')
for key in bucket.list():
    try:
        res = key.get_contents_to_filename(key.name)
    except:
        logging.info(key.name+":"+"FAILED")
