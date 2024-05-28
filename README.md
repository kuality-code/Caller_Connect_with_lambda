

# Caller_Connect_with_Lambda
This project demonstrates the integration of AWS Lambda and Amazon Connect to generate vanity numbers from dialed phone numbers.

### Overview
To test this setup, place a call to the following number registered on AWS Connect: `+18444280920`. The system will generate three vanity numbers for your dialed number.


The Lambda function, written in Python, utilizes a custom package for generating vanity numbers, as the built-in package did not recognize US-based dialed numbers. All runtime libraries are packaged in a Lambda layer. The Lambda function is invoked via a JSON event trigger from the AWS Connect flow.

### Automating AWS Resources to Generate Vanity Numbers

Follow these steps to automate resource deployment using AWS CloudFormation:
1. **Package the CloudFormation Template**
   
   Use the AWS CLI to package your Lambda function and CloudFormation template. This uploads the local artifacts to S3 and produces a new template with the S3 URL.

    ```sh

    aws cloudformation package \

        --template-file template.yaml \

        --s3-bucket your-s3-bucket-name \

        --output-template-file packaged-template.yaml

    ```

2. **Deploy the Packaged CloudFormation Stack**

   Use the following command to deploy your CloudFormation stack:

    ```sh

    aws cloudformation deploy \

        --template-file packaged-template.yaml \

        --stack-name VanityNumberStack \

        --capabilities CAPABILITY_IAM

    ```

This command will:

- Create a CloudFormation stack named `VanityNumberStack`.

- Deploy the resources defined in your `packaged-template.yaml`, including the Lambda function, DynamoDB table, and IAM roles.

### Importing the Amazon Connect Contact Flow

To complete the setup, manually import the contact flow into your Amazon Connect instance:

1. **Log in to Amazon Connect:**

   - Open the [Amazon Connect console](https://console.aws.amazon.com/connect/).

   - Log in to your Amazon Connect instance.

2. **Navigate to Contact Flows:**

   - Go to "Routing" > "Contact flows".

   - Click "Create contact flow".

3. **Import Contact Flow:**

   - Click on the "Import flow" button.

   - Select the provided `contact-flow.json` file and upload it
