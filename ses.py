import boto3
import os
from botocore.exceptions import ClientError
import base64

s3_client = boto3.client('s3')
ses_client = boto3.client('ses')


def lambda_handler(event, context):
    # Environment variables
    bucket_name = os.getenv('BUCKET_NAME')
    object_key = os.getenv('OBJECT_KEY')
    sender_email = os.getenv('SENDER_EMAIL')
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    subject = os.getenv('EMAIL_SUBJECT', 'Your Subject Here')
    body_text = os.getenv('EMAIL_BODY_TEXT', 'Your email body here')

    try:
        # Get the file from S3
        s3_object = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        file_content = s3_object['Body'].read()
        file_name = object_key.split('/')[-1]

        # Create the email
        CHARSET = "utf-8"
        body_html = """<html>
        <head></head>
        <body>
          <h1>Your email subject</h1>
          <p>{}</p>
        </body>
        </html>""".format(body_text)

        # Encode file content to base64
        attachment = base64.b64encode(file_content).decode(CHARSET)

        # Email structure
        email_data = {
            'Source': sender_email,
            'Destination': {'ToAddresses': [recipient_email]},
            'Message': {
                'Subject': {'Data': subject, 'Charset': CHARSET},
                'Body': {
                    'Html': {'Data': body_html, 'Charset': CHARSET},
                    'Text': {'Data': body_text, 'Charset': CHARSET}
                }
            },
            'Attachments': [{
                'Filename': file_name,
                'Data': attachment,
                'ContentType': s3_object['ContentType']
            }]
        }

        # Send email
        response = ses_client.send_raw_email(
            Source=email_data['Source'],
            Destinations=email_data['Destination']['ToAddresses'],
            RawMessage={
                'Data': build_raw_email(email_data)
            }
        )

        return {
            'statusCode': 200,
            'body': f'Email sent! Message ID: {response["MessageId"]}'
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }


def build_raw_email(email_data):
    import email
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication

    msg = MIMEMultipart('mixed')
    msg['Subject'] = email_data['Message']['Subject']['Data']
    msg['From'] = email_data['Source']
    msg['To'] = email_data['Destination']['ToAddresses'][0]

    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(email_data['Message']['Body']['Text']['Data'], 'plain', CHARSET)
    htmlpart = MIMEText(email_data['Message']['Body']['Html']['Data'], 'html', CHARSET)
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    attachment = email_data['Attachments'][0]
    att = MIMEApplication(base64.b64decode(attachment['Data']))
    att.add_header('Content-Disposition', 'attachment', filename=attachment['Filename'])
    msg.attach(msg_body)
    msg.attach(att)

    return msg.as_string()
