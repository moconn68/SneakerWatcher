import json
import main


def lambda_handler(event, context):
    status, error = main.main()
    if status == 0:
        return {
            'statusCode': 200,
            'body': json.dumps('Execution Successful')
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps(error)
        }

