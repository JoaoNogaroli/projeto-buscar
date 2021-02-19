import os
imports = ('task')
task_ignore_result = False
broker_host = 'ec2-52-3-18-175.compute-1.amazonaws.com'
broker_port = 13519 
CELERY_BROKER_BACKEND  = 'redis://:p03b1f0e8fe4c2b0ae8300f4acf09f1f8ddbbcfdb9904856716d1f89554adaf38@ec2-52-3-18-175.compute-1.amazonaws.com:13519'
result_backend  = 'redis://:p03b1f0e8fe4c2b0ae8300f4acf09f1f8ddbbcfdb9904856716d1f89554adaf38@ec2-52-3-18-175.compute-1.amazonaws.com:13519'
