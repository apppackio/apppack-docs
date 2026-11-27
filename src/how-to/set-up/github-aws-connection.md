# Connect your AWS account to GitHub

Before you deploy an app using AppPack, you should connect your GitHub account 
to AWS using their app, which is available in the GitHub Marketplace, free of 
charge. You can do it as part of the process of deploying an app, however the app 
appears to make some assumptions regarding any organisations you belong to, so it 
is best to set up the connection beforehand. This guide takes you through all the 
steps, so you can deploy apps from any of the repositories  you have access to.

First, visit [AWS Connector for GitHub](https://github.com/marketplace/aws-connector-for-github).
Scroll down to the bottom to **Plans and Pricing**.

1. If shown, select the account where you want to install the app.
2. Click "Install".

The **Install & Authorize** page will be displayed:

![aws github app configuration screenshot](./../../assets/aws-gihub-app-configuration.png)

1. At least initially, select **All Repositories**. 
2. Click on **Install & Authorize** to install the app.

You will be redirected to your AWS account. Sign in, then the **Connect to GitHub** 
page will be displayed:

![aws create connection screenshot](./../../assets/aws-create-connection.png)

1. Enter the name of the connection. Any name will do.
2. Click "Connect"

The connection details page will be displayed:

![aws connection details screenshot](./../../assets/aws-github-connection-details.png)

1. Select the region where you want to use the connection.

That's it. Now you can build applications from any of the repositories in your account.
