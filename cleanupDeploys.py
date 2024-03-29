#!/usr/bin/env python

import argparse
import boto3
from collections import defaultdict
import logging

class DeploymentManager:
    def __init__(self, bucket_name, profile_name):
        """
        Initialize the DeploymentManager object with the given S3 bucket name.

        Parameters:
            bucket_name (str): The name of the S3 bucket.
        """
        self.bucket_name = bucket_name
        # Initialize a boto3 session with localstack profile
        self.session = boto3.Session(profile_name=profile_name)
        # Create an S3 client
        self.s3_client = self.session.client('s3', endpoint_url='http://localhost:4566')

        # Configure logging
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    def get_list_of_deployments(self):
        """
        Retrieve the list of objects (deployments) in the S3 bucket.

        Returns:
            list: A list of objects representing the deployments in the S3 bucket.
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            deployments = []
            if 'Contents' in response:
                deployments = response['Contents']
            return deployments
        except Exception as e:
            logging.error(f"An error occurred while retrieving deployments: {e}")
            return []

    def group_deployments(self, objects):
        """
        Group objects (deployments) by their deployment name.

        Parameters:
            objects (list): A list of objects representing the deployments.

        Returns:
            dict: A dictionary where keys are deployment names and values are lists of objects for each deployment.
        """
        deployments = defaultdict(list)
        for obj in objects:
            # Extract the deployment name from the object key
            deployment_name = obj['Key'].split('/')[0]  ## get the prefix of the deployment path
            deployments[deployment_name].append(obj)
        return deployments

    def sort_deployments_by_upload_date(self, deployments):
        """
        Sort deployments by their upload date.

        Parameters:
            deployments (dict): A dictionary where keys are deployment names and values are lists of objects for each deployment.

        Returns:
            list: A list of deployment names sorted by their upload date in descending order.
        """
        upload_dates = {}
        for deployment, objects in deployments.items():
            last_modified_values = []
            # Iterate over each object in the objects list
            for obj in objects:
                # Append the LastModified value of the current object to the list
                last_modified_values.append(obj['LastModified'])

            max_last_modified = max(last_modified_values)
            # Assigning the maximum 'LastModified' value to the corresponding deployment
            upload_dates[deployment] = max_last_modified

        # Sort deployment names based on their upload dates
        sorted_deployments = sorted(deployments.keys(), key=upload_dates.get, reverse=True)
        return sorted_deployments

    def delete_deployments(self, keep_x_deployment):
        """
        Delete old deployments, keeping only the most recent ones.

        Parameters:
            keep_x_deployment (int): The number of most recent deployments to keep.
        """
        # Get the list of deployments in the S3 bucket
        deployments_list = self.get_list_of_deployments()
        # Group deployments by their names
        ordered_deployments = self.group_deployments(objects=deployments_list)
        # Sort deployments by their upload dates
        sorted_deployments = self.sort_deployments_by_upload_date(ordered_deployments)
        logging.info(f'There are total of {len(sorted_deployments)} deployments we are keeping {keep_x_deployment} deployments')
        x_deployment = sorted_deployments[keep_x_deployment:]
        logging.info(f'These deployments will be deleted {x_deployment}')
        # Create an S3 resource to delete objects
        s3_resource = self.session.resource('s3', endpoint_url='http://localhost:4566')
        # Iterate over deployments to be deleted
        for deployment in x_deployment:
            # Iterate over objects in the S3 bucket
            for obj in deployments_list:
                if obj['Key'].startswith(deployment):
                    # Delete objects associated with the deployment
                    s3_resource.Object(bucket_name, obj['Key']).delete()
            logging.info(f"Deleted deployment: {deployment}")

    def delete_deployments_xdays_ydeploys(self, keep_x_days, y_deploys):
        deployments_list = self.get_list_of_deployments()
        # Group deployments by their names
        sorted_deployments = sorted(deployments_list, key=lambda x: x['LastModified'], reverse=True)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cleanup old deployments in S3 bucket')
    parser.add_argument('--keep-x-deployments', type=int, default=1, help='Number of deployments to keep (default: 1)')
    args = parser.parse_args()

    # Define the S3 bucket name
    bucket_name = "deployments"
    # Initialize a DeploymentManager object
    manager = DeploymentManager(bucket_name, profile_name='localstack')
    # Delete old deployments, keeping only the most recent ones
    manager.delete_deployments(args.keep_x_deployments)

'''
List Objects in Bucket: get_list_of_deployments()
The script starts by listing all objects in the S3 bucket s3-bucket-name.
For each object, it retrieves information including the object key and its LastModified timestamp.

Group Objects by Deployment: group_deployments(objects=deployments_list)
It then groups the objects by their parent deployment folders (deploy1, deploy2, etc.).
Each deployment folder becomes a key in the dictionary, and the corresponding value is a list of objects belonging to that deployment.

Sort Deployments by Creation/last-modified Date: sort_deployments_by_upload_date(ordered_deployments)
The script sorts the deployments based on the creation date of their objects.
For example, deploy1 has objects with modification dates on 2023-03-10, deploy2 on 2023-03-09, and so on.

Delete Old Deployments:
Since we want to keep only the two most recent deployments, the script selects the top two deployments from the sorted list (ex deploy1 and deploy2).
It then deletes the objects belonging to the older deployments dirs&files (deploy3, deploy4, and deploy5) using the get_list_of_deployments() dictionary output

'''