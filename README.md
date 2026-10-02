## **PrintNode API Client Python Library**

> [!NOTE]
> This repository is a community-maintained fork of the PrintNode Python API client. It is not an official PrintNode release unless PrintNode explicitly confirms maintainership or transfer. The maintained project name is `printnode_community`.

This is a Python library to interact with PrintNode's remote printing API. This client allows you to access the API's functions for quick use in Python scripts.

### Requirements

* Python 3.10+
* requests
* future

### Installation

Install the maintained community package with:

```sh
uv add printnode_community
```

or:

```sh
python -m pip install printnode_community
```

Install from source with `uv`:

```sh
uv sync --locked
```

`uv sync --locked` also installs this project in editable mode and includes
the development dependencies.

### Development

Install development dependencies and run the local verification gates with:

```sh
uv sync --locked
uv run pytest
uv build
uv run twine check dist/*
```

### Releases

Maintained releases are published to PyPI from reviewed release tags. See
[RELEASE.md](RELEASE.md) for the release process and TestPyPI/PyPI workflow
requirements.

### Getting Started

Create a `Gateway` with an API key, or one of the other authentication modes
below. Construction configures authentication; accessing account data or calling
an API method sends an HTTP request. The examples use placeholder credentials
and illustrative results. Account, tag, API-key and print-job mutations change
the authenticated account; run them only against an account you intend to change.

```python
from printnode_community import Gateway
my_account_gateway = Gateway(apikey='my_api_key')
```

After creating a Gateway, you can access any requests as such:

```python
my_account_id = my_account_gateway.account.id
new_tag = my_account_gateway.ModifyTag("Likes","PrintNode")
```

### Initial Gateway Configuration

You can authenticate in 2 ways other than using an api-key:
```python
Gateway(email='email',password='password')
Gateway(clientkey='ckey')
```

The three below will authenticate with access to child accounts of a specific user:

```python
Gateway(apikey='api-key',child_email='c_email')
Gateway(apikey='api-key',child_ref='c_creator_ref')
Gateway(apikey='api-key',child_id='c_id')
```

### Gateway Methods
The links below describe the remote API. This library returns model objects
for account, computer, printer, print-job, state and download lookups; these
are named tuples with snake_case attributes. Tag and API-key methods return
the decoded API response. Python method names and lookup behavior are described
below; they do not always match the remote API parameter names.


### Computers Library
This handles anything that is associated with a computer, such as Printers, PrintJobs, States (of PrintJobs) and Scales.

### Account lookup
https://www.printnode.com/docs/api/curl/#whoami

#### account(self)
Returns an Account object of the currently authenticated account.
```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
print(gateway.account.firstname)

'''
Results:
Mr
'''
```
### Computer lookup
https://www.printnode.com/docs/api/curl/#computers

#### computers(computer=None, limit=None, after=None, dir=None)
With no computer selector, returns a list of computers. A name string filters
that list by exact name, and still returns a list. An integer ID or `Computer`
model returns one computer, raising `LookupError` if the ID is not found.
Comma-separated ID strings and ID lists are not supported selectors.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
print(gateway.computers(computer=10027).name)

'''
Results:
5.2015-07-10 15:04:40.253763.TEST-COMPUTER
'''
```
### Printer lookup
https://www.printnode.com/docs/api/curl/#printers

#### printers(computer=None, printer=None, limit=None, after=None, dir=None)

* With no printer selector, returns a list of printers.
* A printer name string filters that list by exact name, and still returns a list.
* For these list lookups, `computer` may be an integer ID, a `Computer` model,
  an exact computer name, or `None` for all computers.
* An integer printer ID or `Printer` model returns one printer, raising
  `LookupError` if the ID is not found. This lookup ignores `computer`;
  supplying a computer does not check that the printer belongs to it.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
print(gateway.printers(printer=50120).name)
for printer in gateway.printers(computer=10027):
    print(printer.name)

'''
Results:
10027.3.TEST-PRINTER
10027.1.TEST-PRINTER
10027.2.TEST-PRINTER
10027.3.TEST-PRINTER
10027.4.TEST-PRINTER
10027.5.TEST-PRINTER
'''
```

### PrintJob lookup
https://www.printnode.com/docs/api/curl/#printjob-viewing

#### printjobs(computer=None, printer=None, printjob=None, limit=None, after=None, dir=None)
There are five ways this can be run:

* No arguments : Returns all printjobs associated with the account.
* *computer* int : Returns all printjobs relative to printers associated with the computer specified by the argument *computer*.
* *printer* int : Returns all printjobs relative to the printer specified by the argument *printer*.
* *computer* int, *printer* int : Returns jobs for the printer ID; the numeric
  printer lookup ignores the computer argument.
* *printjob* int or `PrintJob` model : Returns one print job, ignoring
  computer, printer and pagination arguments; raises `LookupError` if absent.
* *printjob* str : Filters the list lookup by exact title and returns a list.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
printjob_id = gateway.printjobs(computer=10027)[0].id
print(gateway.printjobs(printer=50120)[0].id)
print(gateway.printjobs(printjob=printjob_id).id)

'''
Results:
251137
251127
'''
```
### PrintJob creation
https://www.printnode.com/docs/api/curl/#printjob-creating

#### PrintJob(computer=None, printer=None, job_type='pdf', title='PrintJob', qty=None, options=None, authentication=None, uri=None, base64=None, binary=None)
Exactly one of `uri`, `base64` and `binary` is required. The destination must
resolve to one printer. `uri` is a URL the PrintNode client can fetch, not a
local file path; use `binary` for local file contents. The method submits the
job, then looks up and returns its `PrintJob` model.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
print(gateway.PrintJob(printer=50120,options={"copies":2},uri="https://example.com/document.pdf").id)

'''
Results:
251153
'''
```
### State lookup

https://www.printnode.com/docs/api/curl/#printjob-states

#### states(pjob_set=None, limit=None, after=None, dir=None)
Returns a list of lists of `State` models, with one inner list per print job
returned by the API. `pjob_set` accepts a print-job ID or a string describing
a set of IDs; omit it to request states across print jobs.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
printjob_id = gateway.printjobs(computer=10027)[0].id
print(gateway.states(printjob_id)[0][0].state)

'''
Results:
new
'''
```

### Accounts Library
This handles anything to do with accounts, such as Account creation, deletion and modification, api-key handling, tag handling and Client handling.

### Tag lookup
https://www.printnode.com/docs/api/curl/#account-tagging

#### tag(self, tagname)
Given a *tagname*, returns the value of that tag.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
print(gateway.tag("Likes"))

'''
Results:
Everything!
'''
```
### Tag modification
#### ModifyTag(self, tagname, tagvalue)
Given a *tagname* and *tagvalue*, either creates a tag with specified value if *tagname* doesn't exist, otherwise changes the value.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
gateway.ModifyTag("Likes","PrintNode")
print(gateway.tag("Likes"))

'''
Results:
PrintNode
'''
```

### Tag deletion
#### DeleteTag(self, tagname)
Given a *tagname*, deletes that tag and returns the decoded API response.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
gateway.ModifyTag("Likes","PrintNode")
gateway.DeleteTag("Likes")
print(gateway.account.tags)

'''
Results:
[]
'''
```

### Account creation
https://www.printnode.com/docs/api/curl/#account-creation

#### CreateAccount(self, firstname, lastname, email, password, creator_ref=None, api_keys=None, tags=None)
Creates an account with the specified values. The last three are optional.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
new_account = gateway.CreateAccount(
    firstname="A",
    lastname="Person",
    password="password",
    email="aperson@emailprovider.com",
    tags={"Likes":"Something"}
    )
new_account_gateway = Gateway(url='https://api.printnode.com',apikey='secretAPIKey',child_id=new_account["Account"]["id"])
print(new_account_gateway.account.firstname)
new_account_gateway.DeleteAccount()

'''
Results:
A
'''
```

### Account deletion
https://www.printnode.com/docs/api/curl/#account-deletion

#### DeleteAccount(self)
Deletes the child account that is currently authenticated. Accounts can only be deleted if authenticated by a parent account's api-key and a reference to the child account being deleted (e.g the child account's id)
```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
new_account = gateway.CreateAccount(
    firstname="A",
    lastname="Person",
    password="password",
    email="aperson@emailprovider.com",
    tags={"Likes":"Something"}
    )
new_account_gateway = Gateway(url='https://api.printnode.com',apikey='secretAPIKey',child_id=new_account["Account"]["id"])
new_account_gateway.DeleteAccount()
print(new_account["Account"]["id"] in gateway.account.child_accounts)

'''
Results:
False
'''
```

### Account modification
https://www.printnode.com/docs/api/curl/#account-modification

#### ModifyAccount(self, firstname=None, lastname=None, password=None, email=None, creator_ref=None)
Given one or more arguments, changes the account details specified by the arguments.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
new_account = gateway.CreateAccount(
    firstname="A",
    lastname="Person",
    password="password",
    email="aperson@emailprovider.com",
    tags={"Likes":"Something"}
    )
new_account_gateway = Gateway(url='https://api.printnode.com',apikey='secretAPIKey',child_id=new_account["Account"]["id"])
new_account_gateway.ModifyAccount(firstname="B")
print(new_account_gateway.account.firstname)
new_account_gateway.DeleteAccount()

'''
Results:
B
'''
```
### Api-key lookup
https://www.printnode.com/docs/api/curl/#account-apikeys

#### api_key(api_key)
Returns value of api-key specified by the argument.
```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
new_account = gateway.CreateAccount(
    firstname="A",
    lastname="Person",
    password="password",
    email="aperson@emailprovider.com",
    tags={"Likes":"Something"},
    api_keys=["Production"]
    )
new_account_gateway = Gateway(url='https://api.printnode.com',apikey='secretAPIKey',child_id=new_account["Account"]["id"])
print(new_account_gateway.api_key("Production"))
new_account_gateway.DeleteAccount()

'''
Results:
example-api-key
'''
```
### API Key Creation
#### CreateApiKey(api_key)
Creates an api-key with the api-key's reference given by the argument.

```python
from printnode_community import Gateway

gateway = Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
new_account = gateway.CreateAccount(
    firstname="A",
    lastname="Person",
    password="password",
    email="aperson@emailprovider.com",
    tags={"Likes":"Something"},
    api_keys=["Production"]
    )
new_account_gateway = Gateway(url='https://api.printnode.com',apikey='secretAPIKey',child_id=new_account["Account"]["id"])
new_account_gateway.CreateApiKey("Development")
print(new_account_gateway.account.api_keys)
new_account_gateway.DeleteAccount()

'''
Results:
{'Development': '123SecretAPIKey', 'Production': '456SecretAPIKey'}
'''
```
### API Key Deletion
#### DeleteApiKey(api_key)
Deletes api-key specified by the argument.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
new_account = gateway.CreateAccount(
    firstname="A",
    lastname="Person",
    password="password",
    email="aperson@emailprovider.com",
    tags={"Likes":"Something"},
    api_keys=["Production"]
    )
new_account_gateway = Gateway(url='https://api.printnode.com',apikey='secretAPIKey',child_id=new_account["Account"]["id"])
new_account_gateway.DeleteApiKey("Production")
print(new_account_gateway.account.api_keys)
new_account_gateway.DeleteAccount()

'''
Results:
[]
'''
```

### Client Key creation
https://www.printnode.com/docs/api/curl/#account-delegated-auth

#### clientkey(uuid, version, edition)
Generates a clientkey for the account.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
new_account = gateway.CreateAccount(
    firstname="A",
    lastname="Person",
    password="password",
    email="aperson@emailprovider.com",
    tags={"Likes":"Something"},
    api_keys=["Production"]
    )
new_account_gateway = Gateway(url='https://api.printnode.com',apikey='secretAPIKey',child_id=new_account["Account"]["id"])
new_clientkey = new_account_gateway.clientkey(
    uuid="0a756864-602e-428f-a90b-842dee47f57e",
    edition="printnode",
    version="4.7.2")
print(new_clientkey)
new_account_gateway.DeleteAccount()

'''
Results:
example-client-key
'''
```
### Download client lookup
https://www.printnode.com/docs/api/curl/#account-download-management

#### clients(self, client_ids = None, os = None)
This has three different outcomes:

* *os* and *client_ids* both None: Returns all clients available for the current account.
* *os* str and *client_ids* None: Returns a `Download` model for the most
  recent version for the OS value accepted by the API.
* *os* None and *client_ids* str: Given a set of ids (e.g "11-15"), return all clients in that set.

Having both set will default to showing the most recent version for the os argument.

```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
for client in gateway.clients(client_ids="11-12"):
    print(client.id)
print(gateway.clients(os="windows").os)

'''
Results:
12
11
windows
'''
```

### Download client controlling
#### ModifyClientDownloads(self, client_id, enabled)
Given a set of ids and either True or False, sets whether the clients are enabled or not. Returns a list of modified clients.
```python
from printnode_community import Gateway

gateway=Gateway(url='https://api.printnode.com',apikey='secretAPIKey')
gateway.ModifyClientDownloads(11,False)
print(gateway.clients(client_ids=11)[0].enabled)

'''
Results:
False
'''
```
