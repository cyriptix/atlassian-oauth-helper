# atlassian-oauth-helper
Python helper script for generating Jira and Confluence OAuth tokens, for use with their REST APIs

## Requirements

* Python 3
* A reasonably recent version of Jira/Confluence

## Instructions

Create and source a new virtualenv:

```
virtualenv --python=python3 venv
source venv/bin/activate
```

Install required Python modules:

```
pip install -r requirements.txt
```

Generate a private RSA key to sign your requests, and extract the public key:

```
openssl genrsa -out privkey.pem 2048
openssl rsa -pubout -in privkey.pem -out pubkey.pem
```

Configure an Application Link in Jira/Confluence as detailed [here](https://developer.atlassian.com/cloud/jira/platform/jira-rest-api-oauth-authentication/) (see the section titled 'Configure the client app as a consumer in Jira, using application links').

Run the script:

```
./atlassian-oauth-helper.py BASEURL CONSUMER KEYFILE
```

Where:

* `BASEURL`: The base URL (including any context, if applicable) to your Jira/Confluence instance. For example, `https://www.example.com/confluence`
* `CONSUMER`: The consumer key you chose when setting up your Application Link
* `KEYFILE`: The path to the RSA private key you created at the beginning of this guide
