# Used to handle variables and logs
import helpers_handler as helpers
# Importing base boto3
from boto3 import client, resource
# Used to Handle specific Client Errors
from botocore.exceptions import ClientError

# SQS Client
client = client('sqs')

# SQS Resource
resource = resource('sqs')

# Function to create Queue
def CreateSQSQueue(queueName):
    """ 
    Function to create Queue
    Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.create_queue
    """
    try:
        queueUrl = GetQueueURL(queueName)
        if queueUrl == None:
            queueUrl = client.create_queue(
                QueueName=queueName, Attributes={'DelaySeconds': '5', 'VisibilityTimeout' : '5'})
            msg = f"Queue {queueName} created. URL: {queueUrl['QueueUrl']}"
            helpers.logger.warning(msg)
            return None
        else:
            msg = f"Queue {queueName} Already Exists. URL: {queueUrl}"
            helpers.logger.warning(msg)
            return msg
    except client.exceptions.QueueNameExists:
        msg = "Queue Already Exists"
        helpers.logger.warning(msg)
        return msg
    except client.exceptions.QueueDeletedRecently:
        msg = "You must wait 60 seconds after deleting a queue before you can create another with the same name."
        helpers.logger.warning(msg)
        return msg
    except Exception as e:
        msg = f"Exception: {e}"
        helpers.logger.warning(msg)
        return msg

# Function to delete Queue
def DeleteSQSQueue(queueName):
    """ 
    Function to delete Queue
    Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.delete_queue
    """
    try:
        queueUrl = GetQueueURL(queueName)
        if queueUrl != None:
            client.delete_queue(
                QueueUrl=queueUrl)
            helpers.logger.warning(f"Deleting SQS Queue {queueName}")
            return None
        else:
            msg = "There is no QueueURL to Remove..."
            helpers.logger.warning(msg)
            return msg
    except client.exceptions.QueueDoesNotExist:
        msg = "Queue Does Not Exists"
        helpers.logger.warning(msg)
        return msg

# Function to get Queue Url
def GetQueueURL(queueName):
    """
    Function to get Queue Url
    Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.get_queue_url
    """
    try:
        queue = client.get_queue_url(QueueName=queueName)
        return queue['QueueUrl']
    except client.exceptions.QueueDoesNotExist:
        return None

# Function to send message to the Queue
def SendMessage(queueName, msg=[]):
    """
    Function to send message to the Queue
    Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message
    """
    try:
        queue = resource.get_queue_by_name(QueueName=queueName)
        response = queue.send_messages(Entries=msg)
        return response
    except client.exceptions.QueueDoesNotExist:
        print("Queue does not exist.")
        return None

# Function to retrieves one or more messages (up to 10), from the specified queue.
def ReceiveQueueMessage(queueName):
    """ 
    Function to retrieves one or more messages (up to 10), from the specified queue.
    Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.receive_message
    """
    try:
        queueUrl = GetQueueURL(queueName)
        response = client.receive_message(
            QueueUrl=queueUrl, MaxNumberOfMessages=10, MessageAttributeNames=['All'])
    except ClientError:
        helpers.logger.warning(f'Could not receive the message from the - {queueUrl}.')
        return f'Could not receive the message from the - {queueUrl}.'
    except Exception as e:
        if queueUrl == None:
            return 'There is no Queue Url'
        else:
            return e
    else:
        return response

# Function to delete message from the given Queue.
def DeleteQueueMessage(queueName, receiptHandle):
    """ 
    Function to delete message from the given Queue.
    Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.delete_message
    """
    try:
        queueUrl = GetQueueURL(queueName)
        response = client.delete_message(QueueUrl=queueUrl,
                                         ReceiptHandle=receiptHandle)
    except ClientError:
        helpers.logger.exception(
            f'Could not delete the meessage from the - {queueUrl}.')
        raise
    else:
        return response
