under construction


first jobgate api has been deployed 

here's how to use it:

via curl
```

curl -X 'GET' \
  'https://jobgate.onrender.com/get_linkedin_jobs?job_title=software%20engineer&location=pune' \
  -H 'accept: application/json'
```


directly via browser url
```
https://jobgate.onrender.com/get_linkedin_jobs?job_title=software%20engineer&location=pune
```

can be used with python requests
```
import requests

response = requests.get('https://jobgate.onrender.com/get_linkedin_jobs?job_title=software%20engineer&location=pune')
print(response.json())
```


wait for the further updates :))))