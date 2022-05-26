# SQS Controller
import sqs_handler as sqs
# DynamoDB Controller
import dynamodb_handler as dynamodb
# Helpers
import helpers_handler as helpers
# Base Framework
from flask import Flask, jsonify, request
# Used to generate id for SQS Id and dynamoDB ID
import uuid
# Starting Flask App
app = Flask(__name__)

#  Create DynamoDB Tables and SQS Queues
#  Route: http://127.0.0.1:5001/ready
#  Method : GET
@app.route('/ready')
def ready():
    return {
        'msg' : 'Ready'
    }, 200

#  Create DynamoDB Tables and SQS Queues
#  Route: http://127.0.0.1:5001/health
#  Method : GET
@app.route('/health')
def health():
    return {
        'msg' : 'Healthy'
    }, 200

#  Create DynamoDB Tables and SQS Queues
#  Route: http://127.0.0.1:5001/
#  Method : GET
@app.route('/')
def root_route():
    """ Create DynamoDB Tables and SQS Queues. """

    # Create DynamoDB Tables
    response_dynamodb = dynamodb.CreateTables()
    if response_dynamodb != None:
        msg_dynamodb = 'Problem to Create Table, try to use the route /cleanAll before run create again.'
        msg_response_dynamodb = f"Response: {response_dynamodb}."
        helpers.logger.warning(msg_dynamodb)
        helpers.logger.warning(msg_response_dynamodb)

    # Creating SQS Queue
    response_sqs = sqs.CreateSQSQueue(helpers.AWS_SQS_NAME)
    if response_sqs != None:
        msg_sqs = f"Problem to create SQS Queue."
        msg_response_sqs = f"Response: {response_sqs}."
        helpers.logger.warning(msg_sqs)
        helpers.logger.warning(msg_response_sqs)

    # Check response from SQS and DynamoDB
    if response_dynamodb != None and response_sqs != None:
        return {
            'msg_dynamodb': msg_dynamodb,
            'msg_response_dynamodb': msg_response_dynamodb,
            'msg_sqs': msg_sqs,
            'msg_response_sqs': msg_response_sqs
        }, 400
    elif response_dynamodb != None and response_sqs == None:
        return {
            'msg_dynamodb': msg_dynamodb,
            'msg_response_dynamodb': msg_response_dynamodb,
            'msg_sqs': f"Queue {helpers.AWS_SQS_NAME} created successfully.",
        }, 400
    elif response_dynamodb == None and response_sqs != None:
        return {
            'msg_dynamodb': f"DynamoDB Tables Created",
            'msg_sqs': msg_sqs,
            'msg_response_sqs': msg_response_sqs
        }, 400
    else:
        return {
            'msg': 'Tables and SQS Queue have been created Successfully.'
        }, 200


#  Clean DynamoDB Tables and SQS Queues
#  Route: http://127.0.0.1:5001/cleanAll
#  Method : GET
@app.route('/cleanAll', methods=['GET'])
def cleanAll():
    """ Clean DynamoDB Tables and SQS Queues. """

    # Delete DynamoDB Tables
    response_dynamodb = dynamodb.DeleteTables()
    if response_dynamodb != None:
        msg_dynamodb = f"Problem to Delete DynamoDB Tables."
        msg_response_dynamodb = f"Response: {response_dynamodb}."
        helpers.logger.warning(msg_dynamodb)
        helpers.logger.warning(msg_response_dynamodb)

    # Delete SQS Queue
    response_sqs = sqs.DeleteSQSQueue(helpers.AWS_SQS_NAME)
    if response_sqs != None:
        msg_sqs = f"Problem to Delete SQS Queue."
        msg_response_sqs = f"Response: {response_sqs}."
        helpers.logger.warning(msg_sqs)
        helpers.logger.warning(msg_response_sqs)

    # Check response from SQS and DynamoDB
    if response_dynamodb != None and response_sqs != None:
        return {
            'msg_dynamodb': msg_dynamodb,
            'msg_response_dynamodb': msg_response_dynamodb,
            'msg_sqs': msg_sqs,
            'msg_response_sqs': msg_response_sqs
        }, 400
    elif response_dynamodb != None and response_sqs == None:
        return {
            'msg_dynamodb': msg_dynamodb,
            'msg_response_dynamodb': msg_response_dynamodb,
            'msg_sqs': f"Queue {helpers.AWS_SQS_NAME} deleted successfully.",
        }, 400
    elif response_dynamodb == None and response_sqs != None:
        return {
            'msg_dynamodb': f"DynamoDB Tables Deleted",
            'msg_sqs': msg_sqs,
            'msg_response_sqs': msg_response_sqs
        }, 400
    else:
        msg = f"Tables and SQS Queue Deleted."
        helpers.logger.info('Tables and SQS Queue Deleted.')
        return {
            'msg': msg
        }, 200

#  Create an SQS Entry for a new payment
#  Route: http://127.0.0.1:5001/payment
#  Method : POST


@app.route('/payment', methods=['POST'])
def addPayment():
    """ Create an SQS Entry for a new payment. """
    data = request.get_json()
    # Run here if we have a list
    if isinstance(data, list):
        payloads = []
        for i in data:
            id = '{}'.format(uuid.uuid1())
            payload = {
                'Id': id,
                'MessageBody': 'Payment',
                'MessageAttributes': {
                    'id': {
                        'StringValue': id,
                        'DataType': 'String'
                    },
                    'transactionType': {
                        'StringValue': f"{i['transactionType']}",
                        'DataType': 'String'
                    },
                    'amount': {
                        'StringValue': f"{i['amount']}",
                        'DataType': 'String'
                    }
                }
            }
            payloads.append(payload)
        response = sqs.SendMessage(helpers.AWS_SQS_NAME, payloads)
        # Check if we were able to send the message into the Queue
        if response.get('Failed') == None:
            msg = f"Message Sent Successfully to the Queue: {helpers.AWS_SQS_NAME}."
            helpers.logger.info(msg)
            return {
                'msg': msg,
            }
        # Return error if we could not send the message to the Queue
        else:
            msg = 'Some error occured'
            msg_response = f"Response: {response}."
            helpers.logger.warning(msg)
            helpers.logger.warning(msg_response)
            return {
                'msg': msg,
                'response': msg_response
            }
    # Check if we have only one record            
    else:
        payloads = []
        id = '{}'.format(uuid.uuid1())
        payload = {
            'Id': id,
            'MessageBody': 'Payment',
            'MessageAttributes': {
                'id': {
                    'StringValue': id,
                    'DataType': 'String'
                },
                'transactionType': {
                    'StringValue': f"{data['transactionType']}",
                    'DataType': 'String'
                },
                'amount': {
                    'StringValue': f"{data['amount']}",
                    'DataType': 'String'
                }
            }
        }
        payloads.append(payload)
        response = sqs.SendMessage(helpers.AWS_SQS_NAME, payloads)
        if response.get('Failed') == None:
            msg = f"Message Sent Successfully."
            helpers.logger.info(msg)

            return {
                'msg': msg,
            }

#  Store Data from SQS Queue into DynamoDB and clean SQS Queue
#  Route: http://127.0.0.1:5001/persist
#  Method : POST


@app.route('/persist', methods=['POST'])
def persistIntDynamoDB():
    """ Store Data from SQS Queue into DynamoDB and clean SQS Queue. """
    try:
        # Get all messages avaible in the queue, limited up to 10 each time
        messages = sqs.ReceiveQueueMessage(helpers.AWS_SQS_NAME)
        print(messages)
        for m in messages['Messages']:
            id = m['MessageAttributes']['id']['StringValue']
            transactionType = m['MessageAttributes']['transactionType']['StringValue']
            amount = m['MessageAttributes']['amount']['StringValue']

            response = dynamodb.AddItem(id, transactionType, amount)
            if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
                # Get the handle that will be used to identify the Message
                receipt_handle = m['ReceiptHandle']
                response = sqs.DeleteQueueMessage(
                    helpers.AWS_SQS_NAME, receipt_handle)
                if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
                    msg = f"Received processed, stored into DynamoDB and deleted message(s) from {helpers.AWS_SQS_NAME}."
                    helpers.logger.info(msg)
                    return {
                        'msg': msg
                    }
                else:
                    msg = f"Error on received and deleted message(s) from {helpers.AWS_SQS_NAME}."
                    msg_response = f"Response: {response}"
                    helpers.logger.info(msg)
                    return {
                        'msg': msg,
                        'response': msg_response
                    }, 400
        else:
            msg = f"Error on received and deleted message(s) from {helpers.AWS_SQS_NAME}."
            msg_response = f"Response: {response}"
            return {
                'msg': msg,
                'response': msg_response
            }, 400
    except KeyError:
        msg = f"There is no messages in the queue to deal with."
        return {
            'msg': msg
        }, 400
    except:
        return {
            'error': f"{messages}",
            'possible_fix': "Maybe you did not bootstrap your Application, please go to / to start it."
        }, 400  

#  Read a All Payment Entries for PayPal
#  Route: http://localhost:5001/list/paypal
#  Method : GET
@app.route('/list/paypal', methods=['GET'])
def getPayPalPayments():
    try:
        response = dynamodb.GetAllItemsFromPayments('paypal')
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                return { 
                    'Payments': response['Items'],
                    'Amount': len(response['Items'])
                }
            return { 'msg' : 'Item not found!' }
    except:
        return {
            'error': f"{response}",
            'possible_fix': "Maybe you did not bootstrap your Application, please go to / to start it."
        }, 400

#  Read a payment entry for PayPal
#  Route: http://localhost:5001/list/paypal/<id>
#  Method : GET
@app.route('/list/paypal/<string:id>', methods=['GET'])
def getPaymentById(id):
    """ Read a payment entry for PayPal """
    try:
        response = dynamodb.GetPaymentById(id,'paypal')
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Item' in response):
                return { 'Payment': response['Item'] }
            return { 'msg' : 'Item not found!' }
    except:
        return {
            'error': f"{response}",
            'possible_fix': "Maybe you did not bootstrap your Application, please go to / to start it."
        }, 400

#  Read all payment entries for credit card
#  Route: http://localhost:5000/list/credit_card
#  Method : GET
@app.route('/list/credit_card', methods=['GET'])
def getCreditCardPayments():
    """ Read all payment entries for credit card """
    response = dynamodb.GetAllItemsFromPayments('credit_card')
    try:
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            
            if ('Items' in response):
                return { 
                    'Payments': response['Items'],
                    'Amount': len(response['Items'])
                }

            return { 'msg' : 'Item not found!' }
    except:
        return {
            'error': f"{response}",
            'possible_fix': "Maybe you did not bootstrap your Application, please go to / to start it."
        }, 400

#  Read a book entry
#  Route: http://localhost:5001/list/credit_card/<id>
#  Method : GET
@app.route('/list/credit_card/<string:id>', methods=['GET'])
def getCreditCardPaymentById(id):
    try:
        response = dynamodb.GetPaymentById(id,'credit_card')
        
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            
            if ('Item' in response):
                return { 'Payment': response['Item'] }

            return { 'msg' : 'Item not found!' }
    except:
        return {
            'error': f"{response}",
            'possible_fix': "Maybe you did not bootstrap your Application, please go to / to start it."
        }, 400

# Bootstraping
if __name__ == '__main__':
    app.run(host=helpers.FLASK_HOST, port=helpers.FLASK_PORT,
            debug=helpers.FLASK_DEBUG)
