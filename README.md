# README

## Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Postman

- I added a Postman Collection with the curl command lines below.

## Configure your .env

In the root of the project we have .env.sample that you need to configure to start your application, AWS values are required to start the app, otherwise it will fail.

Let's create an .env file

```bash
vim .env
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_DEFAULT_REGION=""
AWS_SQS_NAME="audibene-sqs"
FLASK_HOST="0.0.0.0"
FLASK_PORT="5000"
FLASK_DEBUG=True
DYNAMODB_CREDIT_CARD_TABLE="CreditCard"
DYNAMODB_PAYPAL_TABLE="PayPal"
```

## Starting your Flask App

Let's check if we have all requirements in place to start the compose.

```bash
docker-compose config
services:
  audibene-api-sqs-to-dynamodb:
    build:
      context: /Volumes/Data/test/audibene-api-sqs-to-dynamodb
    environment:
      AWS_ACCESS_KEY_ID: XXX
      AWS_DEFAULT_REGION: us-east-1
      AWS_SECRET_ACCESS_KEY: XXX
      AWS_SQS_NAME: audibene-sqs
      DYNAMODB_CREDIT_CARD_TABLE: CreditCard
      DYNAMODB_PAYPAL_TABLE: PayPal
      FLASK_DEBUG: "True"
      FLASK_HOST: 0.0.0.0
      FLASK_PORT: '5001'
    ports:
    - published: 5001
      target: 5001
version: '3.7'
```

We seems to be in good shape to start.

Let's run the Docker

```bash
docker-compose up -d
Creating network "audibene-api-sqs-to-dynamodb_default" with the default driver
Building audibene-api-sqs-to-dynamodb
[+] Building 0.2s (10/10) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                                          0.0s
 => => transferring dockerfile: 37B                                                                                                                                                           0.0s
 => [internal] load .dockerignore                                                                                                                                                             0.0s
 => => transferring context: 35B                                                                                                                                                              0.0s
 => [internal] load metadata for docker.io/library/python:3.9.12-alpine                                                                                                                       0.0s
 => [internal] load build context                                                                                                                                                             0.0s
 => => transferring context: 10.18kB                                                                                                                                                          0.0s
 => [1/5] FROM docker.io/library/python:3.9.12-alpine                                                                                                                                         0.0s
 => CACHED [2/5] COPY ./requirements.txt /app/requirements.txt                                                                                                                                0.0s
 => CACHED [3/5] WORKDIR /app                                                                                                                                                                 0.0s
 => CACHED [4/5] RUN pip install -r requirements.txt                                                                                                                                          0.0s
 => CACHED [5/5] COPY . /app                                                                                                                                                                  0.0s
 => exporting to image                                                                                                                                                                        0.0s
 => => exporting layers                                                                                                                                                                       0.0s
 => => writing image sha256:45f425542978b5c97c8ee8b03262953da84e35e982734962f0c6aebaf7a896bb                                                                                                  0.0s
 => => naming to docker.io/library/audibene-api-sqs-to-dynamodb_audibene-api-sqs-to-dynamodb                                                                                                  0.0s
WARNING: Image for service audibene-api-sqs-to-dynamodb was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
Creating audibene-api-sqs-to-dynamodb_audibene-api-sqs-to-dynamodb_1 ... done
```

Let's check the logs

```bash
docker-compose logs -f
Attaching to audibene-api-sqs-to-dynamodb_audibene-api-sqs-to-dynamodb_1
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:15,407: INFO: Loading AWS Configurations
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:15,407: INFO: AWS Configurations Loaded
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:15,407: INFO: Loading Flask Configurations
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:15,407: INFO: Flask Configurations Loaded
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:15,408: INFO: Loading Dynamodb Configurations
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:15,408: INFO: Dynamodb Configurations Loaded
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:15,668: INFO: Found credentials in environment variables.
audibene-api-sqs-to-dynamodb_1  |  * Serving Flask app 'app' (lazy loading)
audibene-api-sqs-to-dynamodb_1  |  * Environment: production
audibene-api-sqs-to-dynamodb_1  |    WARNING: This is a development server. Do not use it in a production deployment.
audibene-api-sqs-to-dynamodb_1  |    Use a production WSGI server instead.
audibene-api-sqs-to-dynamodb_1  |  * Debug mode: on
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:15,998: INFO:  * Running on all addresses (0.0.0.0)
audibene-api-sqs-to-dynamodb_1  |    WARNING: This is a development server. Do not use it in a production deployment.
audibene-api-sqs-to-dynamodb_1  |  * Running on http://172.23.0.2:5001
audibene-api-sqs-to-dynamodb_1  |  * Running on http://172.23.0.2:5001 (Press CTRL+C to quit)
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:16,002: INFO:  * Restarting with stat
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:16,095: INFO: Loading AWS Configurations
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:16,095: INFO: AWS Configurations Loaded
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:16,095: INFO: Loading Flask Configurations
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:16,096: INFO: Flask Configurations Loaded
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:16,096: INFO: Loading Dynamodb Configurations
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:16,096: INFO: Dynamodb Configurations Loaded
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:16,406: INFO: Found credentials in environment variables.
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:16,639: WARNING:  * Debugger is active!
audibene-api-sqs-to-dynamodb_1  | 2022-05-26 17:22:16,648: INFO:  * Debugger PIN: 103-167-805
```

## Deploying via Helm

Please change the values.yaml file ./chart/audibene-api-sqs-to-dynamodb/values.yaml

You can change the default values
```yaml
...
secrets:
  AWS_ACCESS_KEY_ID: ""
  AWS_SECRET_ACCESS_KEY: ""
  AWS_DEFAULT_REGION: "us-east-1"
  AWS_SQS_NAME: "audibene-sqs"
  FLASK_HOST: "0.0.0.0"
  FLASK_PORT: "5001"
  FLASK_DEBUG: "True"
  DYNAMODB_CREDIT_CARD_TABLE: "CreditCard"
  DYNAMODB_PAYPAL_TABLE: "PayPal"
```

Or you can replace the values with --set subcommand when you deploy your new application.

```bash
helm install audibene-api-sqs-to-dynamodb ./chart/audibene-api-sqs-to-dynamodb --set secrets.AWS_ACCESS_KEY_ID="XXXX" --set secrets.AWS_SECRET_ACCESS_KEY="QYYYY" --set secrets.AWS_DEFAULT_REGION="us-east-1" -n default --dry-run
```

If the command line above you have no errors we can install the chart

```bash
helm install audibene-api-sqs-to-dynamodb ./chart/audibene-api-sqs-to-dynamodb --set secrets.AWS_ACCESS_KEY_ID="XXXX" --set secrets.AWS_SECRET_ACCESS_KEY="YYYY" --set secrets.AWS_DEFAULT_REGION="us-east-1" -n default
NAME: audibene-api-sqs-to-dynamodb
LAST DEPLOYED: Thu May 26 15:28:57 2022
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=audibene-api-sqs-to-dynamodb,app.kubernetes.io/instance=audibene-api-sqs-to-dynamodb" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT
```

## Kubernetes Objects

All Objects

```bash
k get all -n default -l app.kubernetes.io/instance=audibene-api-sqs-to-dynamodb
NAME                                              READY   STATUS    RESTARTS   AGE
pod/audibene-api-sqs-to-dynamodb-dfb8ddb4-jkl62   1/1     Running   0          119s

NAME                                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/audibene-api-sqs-to-dynamodb   ClusterIP   172.20.165.29   <none>        80/TCP    2m

NAME                                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/audibene-api-sqs-to-dynamodb   1/1     1            1           2m1s

NAME                                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/audibene-api-sqs-to-dynamodb-dfb8ddb4   1         1         1       2m1s

NAME                                                               REFERENCE                                 TARGETS           MINPODS   MAXPODS   REPLICAS   AGE
horizontalpodautoscaler.autoscaling/audibene-api-sqs-to-dynamodb   Deployment/audibene-api-sqs-to-dynamodb   53%/80%, 2%/80%   1         5         1          2m2s
```

Pods resources

```bash
kubectl top pods
NAME                                          CPU(cores)   MEMORY(bytes)
audibene-api-sqs-to-dynamodb-dfb8ddb4-jkl62   2m           68Mi
```

## Note about endpoint

If you are using Helm approach please change: http://127.0.0.1:5001 to http://127.0.0.1:8080 in the next command lines.

## Create Tables and Queue

```bash
# Using Kubernetes Api
export API_URL="http://127.0.0.1:8080"

# Using Docker compose Api
export API_URL="http://127.0.0.1:5001"
```

```bash
curl -v ${API_URL}
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> GET / HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.79.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.9.12
< Date: Thu, 26 May 2022 19:58:37 GMT
< Content-Type: application/json
< Content-Length: 68
< Connection: close
<
{
  "msg": "Tables and SQS Queue have been created Successfully."
}
* Closing connection 0
```

## Sending Data to the Queue

```bash
curl -v -H 'Content-Type:application/json' -H "Accept:application/json" -d '@data.json' ${API_URL}/payment
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> POST /payment HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.79.1
> Content-Type:application/json
> Accept:application/json
> Content-Length: 130
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.9.12
< Date: Thu, 26 May 2022 19:58:52 GMT
< Content-Type: application/json
< Content-Length: 69
< Connection: close
<
{
  "msg": "Message Sent Successfully to the Queue: audibene-sqs."
}
* Closing connection 0
```

## Persist data into DynamoDB

```bash
curl -v -X POST ${API_URL}/persist
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> POST /persist HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.79.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.9.12
< Date: Thu, 26 May 2022 19:59:04 GMT
< Content-Type: application/json
< Content-Length: 98
< Connection: close
<
{
  "msg": "Received processed, stored into DynamoDB and deleted message(s) from audibene-sqs."
}
* Closing connection 0
```

As we are working with just two messages the queue will send usually only one message to be proceed at a time, so run the command above twice.

```bash
curl -v -X POST ${API_URL}/persist
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> POST /persist HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.79.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.9.12
< Date: Thu, 26 May 2022 19:59:17 GMT
< Content-Type: application/json
< Content-Length: 98
< Connection: close
<
{
  "msg": "Received processed, stored into DynamoDB and deleted message(s) from audibene-sqs."
}
* Closing connection 0
```

Now if I try to run it again to persist new messages that we do not have at the momment we will have

```bash
curl -v -X POST ${API_URL}/persist
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> POST /persist HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.79.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 400 BAD REQUEST
< Server: Werkzeug/2.1.2 Python/3.9.12
< Date: Thu, 26 May 2022 19:59:36 GMT
< Content-Type: application/json
< Content-Length: 63
< Connection: close
<
{
  "msg": "There is no messages in the queue to deal with."
}
* Closing connection 0
```

## Checking Payments for Credit Card

Listing all payments for credit card transactions

```bash
curl -v ${API_URL}/list/credit_card
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> GET /list/credit_card HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.79.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.9.12
< Date: Thu, 26 May 2022 19:59:48 GMT
< Content-Type: application/json
< Content-Length: 174
< Connection: close
<
{
  "Amount": 1,
  "Payments": [
    {
      "amount": "\u20ac100",
      "id": "43e3a930-dd2e-11ec-b8ae-fe369c926c0c",
      "transactionType": "credit_card"
    }
  ]
}
* Closing connection 0
```

Now lets list the payment with the id that we have just got.

```bash
curl -v ${API_URL}/list/credit_card/43e3a930-dd2e-11ec-b8ae-fe369c926c0c
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> GET /list/credit_card/43e3a930-dd2e-11ec-b8ae-fe369c926c0c HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.79.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.9.12
< Date: Thu, 26 May 2022 20:00:09 GMT
< Content-Type: application/json
< Content-Length: 139
< Connection: close
<
{
  "Payment": {
    "amount": "\u20ac100",
    "id": "43e3a930-dd2e-11ec-b8ae-fe369c926c0c",
    "transactionType": "credit_card"
  }
}
* Closing connection 0
```

## Checking Payments for PayPal

Listing all payments for PayPal transactions

```bash
curl -v ${API_URL}/list/paypal
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> GET /list/paypal HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.79.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.9.12
< Date: Thu, 26 May 2022 20:00:24 GMT
< Content-Type: application/json
< Content-Length: 169
< Connection: close
<
{
  "Amount": 1,
  "Payments": [
    {
      "amount": "\u20ac150",
      "id": "43e3aa84-dd2e-11ec-b8ae-fe369c926c0c",
      "transactionType": "paypal"
    }
  ]
}
* Closing connection 0
```

Now lets list the payment with the id that we have just got.

```bash
curl -v ${API_URL}/list/paypal/43e3aa84-dd2e-11ec-b8ae-fe369c926c0c
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> GET /list/paypal/43e3aa84-dd2e-11ec-b8ae-fe369c926c0c HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.79.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.9.12
< Date: Thu, 26 May 2022 20:00:47 GMT
< Content-Type: application/json
< Content-Length: 134
< Connection: close
<
{
  "Payment": {
    "amount": "\u20ac150",
    "id": "43e3aa84-dd2e-11ec-b8ae-fe369c926c0c",
    "transactionType": "paypal"
  }
}
* Closing connection 0
```

## Cleaning the Environment

```bash
curl -v ${API_URL}/cleanAll
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> GET /cleanAll HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.79.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.9.12
< Date: Thu, 26 May 2022 20:01:01 GMT
< Content-Type: application/json
< Content-Length: 45
< Connection: close
<
{
  "msg": "Tables and SQS Queue Deleted."
}
* Closing connection 0
```

Let's try to get all the payments for paypal again.

```bash
curl -v  ${API_URL}/list/paypal
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> GET /list/paypal HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.79.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 400 BAD REQUEST
< Server: Werkzeug/2.1.2 Python/3.9.12
< Date: Thu, 26 May 2022 20:01:13 GMT
< Content-Type: application/json
< Content-Length: 221
< Connection: close
<
{
  "error": "An error occurred (ResourceNotFoundException) when calling the Scan operation: Requested resource not found",
  "possible_fix": "Maybe you did not bootstrap your Application, please go to / to start it."
}
* Closing connection 0
```

Let's try to persist some data

```bash
curl -v -X POST ${API_URL}/persist
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> POST /persist HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.79.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 400 BAD REQUEST
< Server: Werkzeug/2.1.2 Python/3.9.12
< Date: Thu, 26 May 2022 20:01:27 GMT
< Content-Type: application/json
< Content-Length: 135
< Connection: close
<
{
  "error": "There is no Queue Url",
  "possible_fix": "Maybe you did not bootstrap your Application, please go to / to start it."
}
* Closing connection 0
```
