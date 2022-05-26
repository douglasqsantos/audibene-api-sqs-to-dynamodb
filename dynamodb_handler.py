# Used to handle variables and logs
import helpers_handler as helpers
# Importing base boto3
from boto3 import client, resource

# DynamoDB Client
client = client('dynamodb')

# DynamoDB Resource
resource = resource('dynamodb')


# Function to Create Initial Tables
def CreateTables():
    """ 
    Function to Create Initial Tables 
    Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table
    """
    try:
        for table in helpers.Tables:
            response = client.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S'
                    }
                ],
                TableName=table,
                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'
                    }
                ],
                BillingMode='PAY_PER_REQUEST',
                Tags=[
                    {
                        'Key': 'test-resource',
                        'Value': 'dynamodb-test'

                    }
                ]
            )
            helpers.logger.warning(
                f"Table {table} is in state: {response['TableDescription']['TableStatus']}.")
        return None
    except client.exceptions.ResourceInUseException:
        return "Table Already Exists."


# Function to Delete the current Tables
def DeleteTables():
    """ 
    Function to Delete the current Tables 
    References: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_table
    """
    try:
        for table in helpers.Tables:
            response = client.delete_table(
                TableName=table
            )
            helpers.logger.warning(
                f"Table {table} is in state: {response['TableDescription']['TableStatus']}.")
        return None
    except client.exceptions.ResourceNotFoundException:
        return "Table does not exist!"
    except Exception as e:
        return e

# Function to add Item to DynamodDB Table based on Transaction Type
def AddItem(id, transactionType, amount):
    """
    Function to add Item to DynamodDB Table based on Transaction Type
    Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item
    """

    try:
        if transactionType == "credit_card":
            PaymentTable = resource.Table(helpers.DYNAMODB_CREDIT_CARD_TABLE)
        elif transactionType == "paypal":
            PaymentTable = resource.Table(helpers.DYNAMODB_PAYPAL_TABLE)
        else:
            msg = f"Transaction Type does not have support"
            return {
                'ResponseMetadata': {
                    'HTTPStatusCode': '400',
                    'msg': msg
                }
            }

        response = PaymentTable.put_item(
            Item={
                'id': id,
                'transactionType': transactionType,
                'amount': amount,
            }
        )

        return response
    except Exception as e:
        return e

# Function to get all Payments for a given Transaction Type
def GetAllItemsFromPayments(transactionType):
    """
    Function to get all Payments for a given Transaction Type
    References: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.scan
    """
    try:
        if transactionType == "credit_card":
            PaymentTable = resource.Table(helpers.DYNAMODB_CREDIT_CARD_TABLE)
        elif transactionType == "paypal":
            PaymentTable = resource.Table(helpers.DYNAMODB_PAYPAL_TABLE)
        response = PaymentTable.scan()
        return response
    except Exception as e:
        return e

# Function to get all Payments for a given Transaction Type and Id
def GetPaymentById(id, transactionType):
    """
    Function to get all Payments for a given Transaction Type and Id
    References: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_item
    """
    try:
        if transactionType == "credit_card":
            PaymentTable = resource.Table(helpers.DYNAMODB_CREDIT_CARD_TABLE)
        elif transactionType == "paypal":
            PaymentTable = resource.Table(helpers.DYNAMODB_PAYPAL_TABLE)

        response = PaymentTable.get_item(
            Key={
                'id': id
            },
            AttributesToGet=[
                'id', 'transactionType', 'amount'
            ]
        )
        return response
    except Exception as e:
        return e
