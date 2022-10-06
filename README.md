# burendo-handbook-infrastructure
This repository contains all the infrastructure and content code to build and deploy the Burendo Handbook.

## Usage

### First run
`pip3 install -r requirements.txt`

### Bootstrap

Replace any mentions of `example` with the name of your new repository, e.g. `burendo-my-service`

Create your AWS session with the cli, and assume the `Administrator` role. For this I personally use [awsume](https://awsu.me/).

then:

`make bootstrap`
`terraform init`


## Adding content

The content is managed in separate repositories.  One [public](https://github.com/BurendoUK/burendo-handbook-public) and one [private](https://github.com/BurendoUK/burendo-handbook-private).  This allows us to be as transparent as possible with our handbook, without exposing content we wish to keep private, such as interview questions or tech tests.

This content is intended to be uploaded to S3 buckets and consumed by the infrastructure in this repository.


## Application Installation

Install [Node.js](https://nodejs.org/en/download/)


## Local Development

You will need to place content from the above mentioned repositories within the `docusaurus/docs/` folder.  This is in `.gitignore`, so feel free to keep that content for testing.

First time running, from within this repo:

```
cd docusaurus/
npm install
npm run start
```
else:
```
npm run start
```

Connect via you're browser on http://localhost:3000 - Most changes are reflected live without having to restart the server.


![Infra](handbook.png)
