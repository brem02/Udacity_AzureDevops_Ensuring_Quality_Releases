# Udacity Cloud DevOps using Microsoft Azure Nanodegree Program - Project: Ensuring Quality Releases

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Dependencies](#dependencies)
- [Instructions](#instructions)
  - [Create a Service Principal for Terraform](#create-a-service-principal-for-terraform)
  - [Configure the storage account and state backend](#configure-the-storage-account-and-state-backend)
  - [Configuring Terraform](#configuring-terraform)
  - [Executing Terraform](#executing-terraform)
- [References](#references)
- [Requirements](#requirements)
- [License](#license)

## Introduction

This project uses Microsoft Azure and a variety of industry leading tools to create disposable test environments and run a variety of automated tests with the click of a button. Additionally it monitors and provides insight into the application's behavior, and determines root causes by querying the application’s custom log files.

## Getting Started

1. Clone this repository
2. Ensure you have all the dependencies
3. Follow the instructions below

## Dependencies

The following are the dependecies of the project you will need:

- Create an [Azure Account](https://portal.azure.com)
- Install the following tools:
  - [Azure command line interface](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
  - [Terraform](https://www.terraform.io/downloads.html)
  - [JMeter](https://jmeter.apache.org/download_jmeter.cgi)
  - [Postman](https://www.postman.com/downloads/)
  - [Python](https://www.python.org/downloads/)
  - [Selenium](https://sites.google.com/a/chromium.org/chromedriver/getting-started)

## Instructions

### Create a Service Principal for Terraform

A Service Principal is an application within Azure Active Directory whose authentication tokens can be used as the `client_id`, `client_secret`, and `tenant_id` fields needed by Terraform (`subscription_id` can be independently recovered from your Azure account details). See [Azure Provider: Authenticating using a Service Principal with a Client Secret](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_client_secret) for details or follow the instructions below.

Firstly, login to the Azure CLI using:

```bash
az login
```

Get the subscription ID:

```bash
az account list
```

Select the `id` field of the subscription you would like to use.

Should you have more than one Subscription, you can specify the Subscription to use via the following command:

```bash
az account set --subscription="SUBSCRIPTION_ID"
```

Now we can create the service principal which will have permissions to manage resources in the specified Subscription using the following command:

```bash
az ad sp create-for-rbac --role="Contributor" --name="terraform-sa" --scopes="/subscriptions/SUBSCRIPTION_ID"
```

This command will output 5 values:

```json
{
  "appId": "00000000-0000-0000-0000-000000000000",
  "displayName": "azure-cli-2017-06-05-10-41-15",
  "name": "http://azure-cli-2017-06-05-10-41-15",
  "password": "0000-0000-0000-0000-000000000000",
  "tenant": "00000000-0000-0000-0000-000000000000"
}
```

These values map to the Terraform variables like so:

- `appId` is the `client_id` defined above.
- `password` is the `client_secret` defined above.
- `tenant` is the `tenant_id` defined above.

Rename `terraform/environments/test/terraform.tfvars.example` to `terraform.tfvars` and store those values:

```bash
# Azure subscription vars
subscription_id = "00000000-0000-0000-0000-000000000000"
client_id = "00000000-0000-0000-0000-000000000000"
client_secret = "0000-0000-0000-0000-000000000000"
tenant_id = "00000000-0000-0000-0000-000000000000"
```

### Configure the storage account and state backend

Terraform supports the persisting of state in remote storage. See [Tutorial: Store Terraform state in Azure Storage](https://docs.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage) for details or follow the instructions below.

Firstly, execute the `create-tf-storage.sh` script:

```bash
bash create-tf-storage.sh
```

Update `terraform/main.tf` with the Terraform storage account and state backend configuration variables:

- `storage_account_name`: The name of the Azure Storage account.
- `container_name`: The name of the blob container.
- `key`: The name of the state store file to be created.
- `access_key`: The storage access key.

```bash
terraform {
  backend "azurerm" {
    resource_group_name  = "tstate"
    storage_account_name = "tstate00000"
    container_name       = "tstate"
    key                  = "terraform.tfstate"
    access_key           = "ACCESS_KEY"
  }
}
```

### Configuring Terraform

Fill in the remaining variables in `terraform/environments/test/terraform.tfvars`:

```bash
# Resource Group/Location
location = "East US"
resource_group = "udacity-ensuring-quality-releases-rg"
application_type = "WebApp"

# Network
virtual_network_name = "udacity-ensuring-quality-releases-vnet"
address_space = ["10.5.0.0/16"]
address_prefix_test = "10.5.1.0/24"
```

### Executing Terraform

Use Terraform to create the following resources for a specific environment tier:

- AppService
- Network
- Network Security Group
- Public IP
- Resource Group
- Linux VM

```bash
cd terraform/environments/test
terraform init
terraform plan -out solution.plan
terraform apply solution.plan
```

## References

- [Tutorial: Store Terraform state in Azure Storage](https://docs.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage)
- [Azure Provider: Authenticating using a Service Principal with a Client Secret](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_client_secret)
- [Create your first pipeline](https://docs.microsoft.com/en-us/azure/devops/pipelines/create-first-pipeline)
- [Automating infrastructure deployments in the Cloud with Terraform and Azure Pipelines](https://azuredevopslabs.com/labs/vstsextend/terraform/)
- [Terraform on Azure Pipelines Best Practices](https://julie.io/writing/terraform-on-azure-pipelines-best-practices/)
- [Use Terraform to manage infrastructure deployment](https://docs.microsoft.com/en-us/azure/devops/pipelines/release/automate-terraform)

## Requirements

Graded according to the [Project Rubric](https://review.udacity.com/#!/rubrics/2843/view).

## License

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2021 © [Thomas Weibel](https://github.com/thom).
