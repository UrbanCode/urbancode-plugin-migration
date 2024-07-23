import requests
from pathlib import Path
import logging
import json
import base64
from utils import utils as myutils
import os


from github import Github
from github import Auth

script_name="simplegh.log" 
# -----------
# some parts I have found here: https://gist.github.com/ursulacj/36ade01fa6bd5011ea31f3f6b572834e
# thank you for the great code examples!

#script_name=Path(__file__).stem
#logging.basicConfig(filename=script_name,
#                    format="[%(filename)s:%(lineno)s - %(funcName)20s() - %(levelname)s] %(message)s",
#                    filemode='w')


# Creating an object
loggerS = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(script_name)
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

# Setting the threshold of logger to DEBUG
c_format = logging.Formatter('[%(filename)s:%(lineno)s - %(funcName)30s() - %(levelname)s] %(message)s')
f_format = logging.Formatter('[%(filename)s:%(lineno)s - %(funcName)30s() - %(levelname)s] %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
loggerS.addHandler(c_handler)
loggerS.addHandler(f_handler)


def get_gh_session_header():
    config = myutils.get_config()
    session = requests.Session()
    session.auth = (config.get(myutils.GITHUB_USER), config.get(myutils.GITHUB_TOKEN))
    session.headers = {'accept': 'application/vnd.github.v3+json'}

    return session

def gh_post_request(url, data):
    loggerS.info(f"url={url} - data={data}")
    session = get_gh_session_header()
    response = session.post(url, data)
    response_status = response.status_code
    loggerS.info(f'response_status={response_status}')    
    if response_status > 201:
        print(f'\n response code: {response_status}')
        exit()

    json = response.json()

    print (f"response-json={json}")
    loggerS.info(f"response-json={json}")
    return json 

def gh_put_request(url, data):
    loggerS.info(f"url={url} - data={data}")
    session = get_gh_session_header()
    session.headers.update({'Content-Type':'application/json'})
    response = session.put(url, data)
    response_status = response.status_code
    loggerS.info(f'response_status={response_status} - response={response.json()}')    
    if response_status > 201:
        print(f'\n response code: {response_status} - response={response.json()}')
        exit()

    json = response.json()

    print (f"response-json={json}")
    loggerS.info(f"response-json={json}")
    return json 

def gh_crate_gh_action(org_name, repo_name, file_name, file_content, sha=""):
    fc_bytes=file_content.encode("ascii")
    b64content = base64.urlsafe_b64encode(fc_bytes)
    b64content_string = b64content.decode("ascii")
    config = myutils.get_config()
    url = f'{config.get(myutils.GITHUB_API_URL)}/repos/{org_name}/{repo_name}/contents/.github/workflows/{file_name}'
    data = {
        "message" : "creating action",
        "committer": {
            "name" : config.get(myutils.GITHUB_USER),
            "email": config.get(myutils.GITHUB_EMAIL)
        },
        "content" : f"{b64content_string}"
    }
    if sha != "": data["sha"] = sha
    data = json.dumps(data)
    loggerS.info (f"url={url} - data={data}")
    reporesponse = gh_put_request(url, data)

    # reporesponse = sgh.create_update_repo_file(repo, list_of_existing_files, ".github/workflows/ci.yml", file_content)     
    return reporesponse

def get_gh_repo_files_list(repo):
    list_of_files=[]
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            list_of_files.append(file_content.path)
    loggerS.info(f"list_of_files={list_of_files}")
    return list_of_files

    
def create_update_repo_file(repo, list_of_existing_files, new_file_name, file_content):
    loggerS.info(f"new_file_name={new_file_name} - list_of_existing_files={list_of_existing_files}")
    reporesponse = ""
    do_compare = myutils.is_compareable_file(new_file_name) 

    if new_file_name in list_of_existing_files:
        if do_compare:
            encodedcontents = repo.get_contents(new_file_name)
            contents=encodedcontents.decoded_content.decode('utf-8')
            loggerS.debug(f"origcontent={contents}")
            loggerS.debug(f"newcontent={file_content}")
            if (file_content == contents): 
                reporesponse= "files are equal - no update needed"
            else:
                loggerS.debug("files are not equal - do update")
                reporesponse = repo.update_file(encodedcontents.path, f"updating {new_file_name}", file_content, encodedcontents.sha)
    else: 
        reporesponse = repo.create_file(new_file_name, f"adding {new_file_name}", file_content, branch="main")
    loggerS.info(f"response={reporesponse}")
    return reporesponse

def gh_get_all_release_assets(repo):
    all_release_assets=[]
    repo_releases = repo.get_releases()
    for rr in repo_releases:
        loggerS.debug(f"release={rr}")
        rassets=rr.get_assets()
        for ra in rassets:
            rurl=ra.url
            loggerS.debug(f"assets={ra} - url={rurl}")
            # now curl the url and get
            session = get_gh_session_header()
            response = session.get(rurl)
            response_status = response.status_code
            assetinfo=response.json()
            loggerS.debug(f'response_status={response_status} - response.json={assetinfo}')   
            all_release_assets.append(assetinfo.get('browser_download_url'))
    return all_release_assets

def gh_get_release(repo, release_name):
    release = None
    repo_releases = repo.get_releases()
    loggerS.info(f"all_releases={repo_releases}")
    for rr in repo_releases:
        loggerS.debug(f"release={rr}")
        if (release_name == rr.title):
            loggerS.info(f"release found={rr.title}")
            release = rr
            break
    return release


def gh_create_release(repo, ucproduct, plugin):
    all_assets=gh_get_all_release_assets(repo)
    loggerS.debug(f"all assets={all_assets}")

    config = myutils.get_config()
    # loggerS.info(f"config={config}")
    plugin_versions = plugin.get(myutils.PLUGIN_FILES)
    for version in plugin_versions:
        loggerS.info(f"versionobject={version}")
        # only upload files which are marked for publishing
        if (not plugin[myutils.PUBLISH]): continue

        # only upload valid files, skip files which description is ERROR_FILE_DAMAGED
        if (myutils.ERROR_FILE_DAMAGED in version.get(myutils.INFO_DESCRIPTION)): continue

        # only upload Plugin files and nothing else, skip files which description is NOT_PLUGIN_FILE
        # if (myutils.NOT_PLUGIN_FILE == version.get(myutils.INFO_DESCRIPTION)): continue
        if (myutils.NOT_PLUGIN_FILE in version.get(myutils.INFO_DESCRIPTION)): continue

        version_notes= "\n".join(version.get(myutils.RELEASE_NOTES))
        release_version=version.get(myutils.RELEASE_VERSION)
        release_tag = version.get(myutils.RELEASE_SEMVER)

        # no release for not plugins - put them all into the files folder
        # if (myutils.NOT_PLUGIN_FILE_SAMPLE_OR_TEMPLATE == version.get(myutils.INFO_DESCRIPTION)):
        #     release_version = "Sample_Template"
        #     release_tag = "Sample_Template"
        

        loggerS.info(f"version={release_version} - tag={release_tag} - notes={version_notes}")
        plugin_files_root=myutils.get_plugin_files_root(ucproduct)
        plugin_files_folder=config.get(myutils.UCX_PLUGIN_FILES_FOLDER)
        plugin_name_folder=plugin.get(myutils.PLUGIN_FILES_FOLDER)
        plugin_file_name=version.get(myutils.RELEASE_FILE)

        inrelease=False
        for assetitem in all_assets: 
            if plugin_file_name in assetitem:
                inrelease=True
                break
        if not inrelease: 
            loggerS.debug(f"root={plugin_files_root} - folder={plugin_files_folder} - plugin={plugin_name_folder} - file={plugin_file_name}")
            file_path=f"{plugin_files_root}/{plugin_files_folder}/{plugin_name_folder}/{plugin_file_name}"
            loggerS.debug(f"file_path={file_path}")
            branch=repo.get_branch("main")
            release = gh_get_release(repo, release_version)
            if (release == None):
                rel_draft=False
                if release_tag == "Sample_Template": rel_draft=True
                loggerS.info(f"create release with version={release_version} - tag={release_tag} - notes={version_notes}")
                reporesponse = repo.create_git_ref(ref='refs/tags/' + release_tag, sha=branch.commit.sha)
                release = repo.create_git_release(tag=release_tag, name=release_version, message=version_notes, target_commitish=branch, draft=rel_draft ) 
                # release = repo.create_git_tag_and_release(tag=release_tag, tag_message=release_tag, release_name=release_version, release_message=version_notes, object=branch.commit.sha, type="commit" ) 
            loggerS.info(f"release={release}")
            reporesponse = release.upload_asset(path=file_path, content_type="application/octet-stream")
            loggerS.info(f"reporespons={reporesponse}")
        else:
            reporesponse = "file is in a release"
            loggerS.debug(f"release={reporesponse}")
    return reporesponse

def gh_init_repo(repo, ucproduct, plugin):
    # create LICENSE file?
    # copy plugin infos from templates
    # create README
    template_files=["README.md", "DevOps-Automation_General_Plugin_Terms_and_Conditions.md", "DevOps-Automation_Plugin_Terms_and_Conditions.md", "ibm-plugins-terms-and-conditions.txt"]
    for file_name_orig in template_files:
        file_content = open(f"src/templates/{file_name_orig}", "r").read()
        reporesponse = repo.create_file(file_name_orig, "init", file_content)
        loggerS.info (f"reporesponse={reporesponse}")
    return reporesponse

def gh_get_repo(ucproduct, plugin):
    config = myutils.get_config()
    auth = Auth.Token(config[myutils.GITHUB_TOKEN])
    g = Github(auth=auth)
    g.get_user().login
    org_name = myutils.get_organization(ucproduct)
    org = g.get_organization(org_name)
    repo_name= myutils.get_repo_name (ucproduct, plugin)
    repo_desc=plugin.get("description", "").replace("\n", " ")

    loggerS.info(f'org={org_name} - repo={repo_name} - desc={repo_desc}')
    # CHECK if repo exists, if not create

    all_repos=org.get_repos(type='all', sort='full_name')
    repo_found=False
    for repo in all_repos:
        loggerS.info (f"repo.name={repo.name}")
        if repo_name in repo.name:
            repo_found = True
            break
    if (not repo_found): 
        repo = org.create_repo(repo_name, description = repo_desc)
        loggerS.info (f"repo created={repo.name}")
        # init the repo 
        reporesponse = gh_init_repo(repo, ucproduct, plugin)
        loggerS.info (f"repo initresults={reporesponse}")
    return repo 

def gh_create_ghpages_branch(repo):
    reporesponse = ""
    source_branch="main"
    target_branch = "gh-pages"

    list_of_branches = repo.get_branches()
    loggerS.info(f"list of branches={list_of_branches}")
    for b in list_of_branches:
        if b.name==target_branch: 
            loggerS.info(f"branch {target_branch} exists")
            return f"branch {target_branch} exists"

    sb = repo.get_branch(source_branch)
    reporesponse = repo.create_git_ref(ref='refs/heads/' + target_branch, sha=sb.commit.sha)
    loggerS.info(f"response={reporesponse}")
    return reporesponse

def main():

    print ("Utility Functions for urbancode migration project using github")
    os._exit(0)

if __name__ == '__main__':
    #main(sys.argv[1:])
    main()
    