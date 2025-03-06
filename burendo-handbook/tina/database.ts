import { createDatabase, createLocalDatabase } from "@tinacms/datalayer";
import { GitHubProvider } from "tinacms-gitprovider-github";
import { MongodbLevel } from 'mongodb-level'

const isLocal = process.env.TINA_PUBLIC_IS_LOCAL === "true";
const token = process.env.GITHUB_PERSONAL_ACCESS_TOKEN as string;
const owner = process.env.GITHUB_OWNER;
const repo = process.env.GITHUB_REPO;
const branch =
  process.env.GITHUB_BRANCH ||
  process.env.HEAD ||
  "main";

const checkValue = (valToCheck: any, name: string, envVarName: string) => {
  if (!valToCheck) {
    throw new Error(
      "No " + name + " found. Make sure that you have set the " + envVarName + " environment variable."
    );
  }
}

checkValue(token, "token", "GITHUB_PERSONAL_ACCESS_TOKEN")
checkValue(owner, "owner", "GITHUB_OWNER")
checkValue(repo, "repo", "GITHUB_REPO")

export default isLocal
  ? createLocalDatabase()
  : createDatabase({
      gitProvider: new GitHubProvider({
        branch,
        owner,
        repo,
        token,
      }),
      databaseAdapter: new MongodbLevel<string, Record<string, any>>({
        collectionName: `tinacms`,
        dbName: 'burendo-handbook-db',
        mongoUri: process.env.MONGODB_URI as string,
      }),
      namespace: branch,
    });
    