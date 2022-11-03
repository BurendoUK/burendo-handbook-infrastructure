# Burendo Handbook Infrastructure

This repo contains the AWS infrastructure for the Burendo Handbook & the pipeline to pull in the content from the content repos, build docusaurus and deploy.

## Content
To update the content used to create the handbook, modify in the respective content repo.
[burendo-handbook-public](https://github.com/BurendoUK/burendo-handbook-public)
[burendo-handbook-private](https://github.com/BurendoUK/burendo-handbook-private)

## Architecture
![Handbook architecture](handbook-architecture.png)

## Running locally

Running locally, you will need to bring in the docs from content repos into burendo-handbook/docs.
Then enter `burendo-handbook` folder and run `npm run`.
