

# Caller_Connect_with_Lambda
This project demonstrates the integration of AWS Lambda and Amazon Connect to generate vanity numbers from dialed phone numbers.

### Overview
To test this setup, place a call to the following number registered on AWS Connect: `+18444280920`. The system will generate three vanity numbers for your dialed number.


The Lambda function, written in Python, utilizes a custom package for generating vanity numbers, as the built-in package did not recognize US-based dialed numbers. All runtime libraries are packaged in a Lambda layer. The Lambda function is invoked via a JSON event trigger from the AWS Connect flow.

### Automating AWS Resources to Generate Vanity Numbers
#### *Bonus part*

Follow these steps to automate resource deployment using AWS CloudFormation:
1. **Package the CloudFormation Template**
   
   Use the AWS CLI to package your Lambda function and CloudFormation template. This uploads the local artifacts to S3 and produces a new template with the S3 URL.

    ```sh

    aws cloudformation package \
        --template-file deployments.yaml \
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

### *Super Bonus part*

For a web application, we can create a Flask app to retrieve data from AWS DynamoDB and host it on AWS S3 for static hosting, with CloudFront for content delivery and caching. 

##### This approach provides a scalable, cost-effective solution for hosting a web interface that interacts with dynamoDB on AWS.
---



### Reasons for Solution Implementation, Struggles, and Overcomings

I chose an optimal strategy for integrating AWS Connect with Lambda using CloudFormation. The primary challenge I encountered was passing the dialed number to the Lambda function from Connect. After thorough research, I discovered this capability is supported by the built-in AWS Invoke Lambda Connect block. Overall, I enjoyed the experience and the learning process.

### Shortcuts and Production Considerations
In a production environment, it’s best practice to pass vanity numbers as JSON from Lambda and use AWS Connect Set Attributes to manage them efficiently. However, due to complexity, I simplified this by concatenating vanity numbers into a flat string for Lambda responses in the Connect flow. This shortcut bypasses optimal data handling but enabled quicker implementation for this project.

### Additional Work with More Time
Given more time, I would have developed a live, deployed web app to display the last five dialers and their generated vanity numbers, pulling data directly from the DynamoDB database.
