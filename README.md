# urbancode-migration

code for migration of urbancode.com (plug-ins) to new location

## steps

1. read the plug-in index file (contains all data)
   1. or read simplified index file. contains only plug-in name, docs folder name, plug-in repo name, target repo name, rest will be build on the fly
2. using REST interface to create REPOsitories in the products ORG
3. upload documentation (processed, remove unecessary navtable etc) into docs folder
4. upload special files (files not marked as PLUGIN) to files folder
5. create and upload info.json and releases.json into files folder
6. create and upload mkdocs.yaml
7. setup gh-pages
8. either clone repo to disk or continue using REST interface
9. create for each plugin-version a release based on plugin-version information and attach plugin-file to release

## take care of

- plugin files with semver 0.0
  - copy them into files subfolder
  - and link them in the downloads.md too!
  - take care of files with .001 ending, there maybe more and need also to be copied...

## other input

- check to use gh cli client for creating and uploading releases instead of REST interface
- look at <https://cli.github.com/manual/gh_release_create>

## GitHub Token

### Settings used

- ALL repo
- workflow
- write:packages
- ALL admin:org
- ALL user

#### not sure if needed

- ALL admin:enterprise
- ALL project

## shell scripts

- do_it.sh: use to run the migration
- set_env.sh: default settings and environment variables used in the python code
- set_secret_env.sh: file not under versioncontrol. overrides the set_env.sh settings with your special settings (for example your github token and so on)