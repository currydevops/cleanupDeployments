-Where should we run this script?
There are several options for running this script:
- My preferred method is to deploy the deployment cleanup process as a serverless Lambda function on AWS. This entails setting up a scheduled trigger using EventBridge to run the Lambda function periodically. Additionally, I can enable manual execution by integrating the Lambda function with Slackbot through API Gateway.
- Another approach is to run the script as a cronjob configured with IAM Roles for Service Accounts (IRSA) for recurring execution, or as a job using Kubernetes (e.g., kubectl apply -f job-template/helm-install) on an EKS cluster. This assumes that we will be building a Docker image for this project.
- Alternatively, we can execute the script in a Continuous Integration (CI) environment like GitHub Actions. We can manually trigger the workflow to run the Python script, or utilize Argo Workflows to create a Kubernetes job on demand in EKS that executes the Python script.

How should we test the script before running it production?
- Assuming that each environment has its own bucket for deployment assets, it's important to test the script in various environments such as development and staging. This helps uncover any environment-specific issues and guarantees uniformity across deployments.
- Write unit tests for individual components and functions of the script using a testing framework like unittest or pytest.
- If the deploy-assets are only presents in production, we mock some data in dev and run our script there as well.
- Conduct end-to-end tests to verify the entire workflow, including EventBridge triggers, Lambda execution, S3 interactions, and API Gateway integration in the dev/staging environment first.
- Get your code peer-reviewed.
- Make sure that your bucket in production has `versioning enabled`, just in case if we need to revert our changes

If we want to add an additional requirement of deleting deploys older than X days but we must maintain at least Y number of deploys. What additional changes would you need to make in the script?
I have written a `delete_deployments_xdays_ydeploys` in cleanupDeploys.py method that explains the code with the points below 
- Retention Threshold Calculation: Determine a retention threshold based on the requirement to maintain at least Y deployments. This will ensure that the script retains a minimum number of deployments even after cleanup. 
- Cutoff Date Calculation: Calculate a cutoff date for retaining deployments based on the maximum age of deployments (X days). Deployments older than this cutoff date will be candidates for deletion.
- Adjust Deletion Logic: Modify the deletion logic to consider both the age of deployments and the number of retained deployments. Only delete deployments that exceed the retention threshold in terms of age and quantity.