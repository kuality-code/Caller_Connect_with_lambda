import boto3
import re
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Initialize DynamoDB resource automatically using the Lambda's execution role

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("VanityNumbers")

def digit_to_vanity(digit):
    digit_to_letters = {
        '2': 'CAR', '3': 'TUCK', '4': 'PEN', '5': 'HEN',
        '6': 'COW', '7': 'TRUCK', '8': 'BED', '9': 'ROAD'
    }
    return digit_to_letters.get(digit, digit)

def generate_vanity_combinations(digits):
    if not digits:
        return ['']
    
    first_digit = digits[0]
    remaining_digits = digits[1:]
    vanity_for_first = digit_to_vanity(first_digit)
    remaining_combinations = generate_vanity_combinations(remaining_digits)
    
    combinations = []
    for letter in vanity_for_first:
        for combination in remaining_combinations:
            combinations.append(letter + combination)
    
    return combinations


def is_meaningful(word):
    return bool(re.match(r"^[A-Z]+$", word))


# Define a function to score vanity numbers
def score_vanity_number(vanity_number):
    words = re.findall(r"[A-Z]+", vanity_number)
    score = 0
    for word in words:
        if is_meaningful(word):
            score += len(word)  # Example: Score based on length of meaningful words
    return score


def phone_to_vanity(number):
    # Remove non-digit characters
    number = "".join(filter(str.isdigit, number))

    # Generate vanity numbers using the correct function
    vanity_numbers = generate_vanity_combinations(number)
    return vanity_numbers


def lambda_handler(event, context):
    # phone_number = event["phone_number"]
    phone_number = event['Details']['ContactData']['CustomerEndpoint']['Address']

    print(f"Received phone number: {phone_number}")
    vanity_numbers = phone_to_vanity(phone_number)
    scored_vanity_numbers = [(vn, score_vanity_number(vn)) for vn in vanity_numbers]
    scored_vanity_numbers.sort(key=lambda x: x[1], reverse=True)

    # Select the top 5 best vanity numbers to store
    best_vanity_numbers_to_store = [vn for vn, score in scored_vanity_numbers][:5]
    print(f"Vanity numbers to be stored: {best_vanity_numbers_to_store}")
    

    try:
        table.put_item(
            Item={"phone_number": phone_number, "vanity_numbers": best_vanity_numbers_to_store}
        )
        print("Data successfully stored in DynamoDB")
    except NoCredentialsError:
        print("Credentials not available")
        return {"statusCode": 500, "body": "Credentials not available"}
    except PartialCredentialsError:
        print("Incomplete credentials provided")
        return {"statusCode": 500, "body": "Incomplete credentials provided"}
    except Exception as e:
        print(f"Error storing data in DynamoDB: {str(e)}")
        return {"statusCode": 500, "body": str(e)}

    # Select the top 3 best vanity numbers to return
    best_vanity_numbers_to_return = [vn for vn, score in scored_vanity_numbers][:3]
    best_vanity_numbers_to_speak = f"First is {best_vanity_numbers_to_return[0]} second is {best_vanity_numbers_to_return[1]} and third one is {best_vanity_numbers_to_return[2]}"
    print(f"Vanity numbers to be return: {best_vanity_numbers_to_speak}")

    return {"phone_number": best_vanity_numbers_to_speak}