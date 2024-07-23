import logging
import os
import json
from utils import utils as myutils
from utils import simplegh as sgh 


script_name="migrate_plugins_and_docs.log" 
#script_name=Path(__file__).stem
logging.basicConfig(filename=script_name ,
                    format="[%(filename)s:%(lineno)s - %(funcName)20s() - %(levelname)s] %(message)s",
                    filemode='w')

# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def remove_navbar(file_path):
    new_content_list = []
    # |Back to ...|
    with open(file_path, "r") as file:
        file_content = file.readlines()
    for line in file_content:
        if ("|Back to ..." in line): break
        new_content_list.append(line)
    new_content = "".join(new_content_list)
    return new_content

def create_history_md(plugin, repo, list_of_existing_files):
    file_content = "# History\n \n## List of Versions\n \n"
    plugin_versions = plugin.get(myutils.PLUGIN_FILES)
    reverse_sorted_plugin_versions = sorted(plugin_versions, key=lambda d: d['SORT_VERSION'], reverse=True)
    for version in reverse_sorted_plugin_versions:
        version_notes= "\n".join(version.get('notes'))
        version_text = f"### Version {version.get('version')}\n \n#### Build: {version.get('semver')} - Date: {version.get('date')}\n \n{version_notes}\n \n"
        file_content = file_content + version_text
    logger.info(f"file_content={file_content}")
    reporesponse = sgh.create_update_repo_file(repo, list_of_existing_files, "docs/history.md", file_content)
    return reporesponse

def create_mkdocs_yml(ucproduct, plugin, repo, list_of_existing_files):
    file_content = open("src/templates/mkdocs_template.yml", "r").read()
    file_content = file_content.replace("ORGPLUGINNAME", f"{myutils.get_productshortname(ucproduct)} - {plugin.get('name')}")
    reporesponse = sgh.create_update_repo_file(repo, list_of_existing_files, "mkdocs.yml", file_content)
    return reporesponse

def create_info_json(ucproduct, plugin, repo, list_of_existing_files):
    info = myutils.get_info_template()
    logger.info(f"info={info}")
    for key in info:
        logger.info(f"key={key}")
        value = plugin.get(key, "")
        logger.info(f"value={value}")
        info[key]= value
    file_content = json.dumps(info, indent=4)
    logger.info(f"info={info}")
    reporesponse = sgh.create_update_repo_file(repo, list_of_existing_files, "files/info.json", file_content)
    return reporesponse

def create_releases_json(ucproduct, plugin, repo, list_of_existing_files):
    list_of_releases=[]
    plugin_files=plugin.get(myutils.PLUGIN_FILES)
    reverse_sorted_plugin_versions = sorted(plugin_files, key=lambda d: d[myutils.RELEASE_SORTVERSION], reverse=True)    
    for plugin_file in reverse_sorted_plugin_versions:
        release = myutils.get_release_template()
        for key in release:
            logger.info(f"key={key}")
            value = plugin_file.get(key, "")
            logger.info(f"value={value}")
            release[key]= value
        list_of_releases.append(release)
    file_content = json.dumps(list_of_releases, indent=4)
    logger.info(f"list_of_releases={list_of_releases}")
    reporesponse = sgh.create_update_repo_file(repo, list_of_existing_files, "files/releases.json", file_content)
    return reporesponse

def create_downloads_md(ucproduct, plugin, repo, list_of_existing_files):
    config=myutils.get_config()
    file_content = "# Downloads\n \n## List of Versions\n \n"
    plugin_versions = plugin.get(myutils.PLUGIN_FILES)
    org_name = myutils.get_organization(ucproduct)
    repo_name= myutils.get_repo_name (ucproduct, plugin)
    reverse_sorted_plugin_versions = sorted(plugin_versions, key=lambda d: d[myutils.RELEASE_SORTVERSION], reverse=True)
    for version in reverse_sorted_plugin_versions:
        if (myutils.NOT_PLUGIN_FILE in version.get(myutils.INFO_DESCRIPTION)): continue
        tag_name=version.get(myutils.RELEASE_SEMVER)
        file_name=version.get(myutils.RELEASE_FILE)
        download_url = f"{config.get(myutils.GITHUB_API_BASE_URL)}/{org_name}/{repo_name}/releases/download/{tag_name}/{file_name}" 
        version_text = f"- Date: {version.get('date')} - [{file_name}]({download_url})\n"
        file_content = file_content + version_text
    logger.info(f"file_content={file_content}")
    reporesponse = sgh.create_update_repo_file(repo, list_of_existing_files, "docs/downloads.md", file_content)    
    return reporesponse    

def setup_ghpages(ucproduct, plugin, repo, list_of_existing_files):
    # create ci action
    reporesponse = create_gh_ci_action_yml(ucproduct, plugin, repo, list_of_existing_files)
    logger.info(f"reporesponse={reporesponse}")
    # create gh-pages branch
    reporesponse = sgh.gh_create_ghpages_branch(repo)
    logger.info(f"reporesponse={reporesponse}")

#    repo.update_branch("main")

    return reporesponse

def create_gh_ci_action_yml(ucproduct, plugin, repo, list_of_existing_files):
    file_name_orig = "ci_template.yml"
    file_name = "ci.yml"
    file_sha = ""
    new_file_name = f".github/workflows/{file_name}"
    logger.info(f"new_file_name={new_file_name} - list_of_files={list_of_existing_files}")
    for f in list_of_existing_files:
        logger.info(f"f={f}")
        if f == new_file_name:
            contents = repo.get_contents(new_file_name)
            logger.info(f"ci.yml contents={contents}")
            file_sha = contents.sha
            logger.info(f"ci.yml sha={file_sha}")
            break
 
    file_content = open(f"src/templates/{file_name_orig}", "r").read()
    org_name = myutils.get_organization(ucproduct)
    repo_name= myutils.get_repo_name (ucproduct, plugin)
    reporesponse = sgh.gh_crate_gh_action(org_name, repo_name, file_name, file_content, file_sha)
    return reporesponse

def copy_special_files_to_repo(ucproduct, repo, plugin):
    config = myutils.get_config()
    plugin_versions = plugin.get(myutils.PLUGIN_FILES)
    list_of_existing_files=[]
    list_of_existing_files = sgh.get_gh_repo_files_list(repo)
    reporesponse = ""

    for version in plugin_versions:
        logger.info(f"versionobject={version}")
        # only upload files which are marked for publishing
        if (not plugin[myutils.PUBLISH]): continue

        if (myutils.NOT_PLUGIN_FILE not in version.get(myutils.INFO_DESCRIPTION)): continue
        
        plugin_files_root=myutils.get_plugin_files_root(ucproduct)
        plugin_files_folder=config.get(myutils.UCX_PLUGIN_FILES_FOLDER)
        plugin_name_folder=plugin.get(myutils.PLUGIN_FILES_FOLDER)
        plugin_file_name=version.get(myutils.RELEASE_FILE)
        logger.debug(f"root={plugin_files_root} - folder={plugin_files_folder} - plugin={plugin_name_folder} - file={plugin_file_name}")
        file_path=f"{plugin_files_root}/{plugin_files_folder}/{plugin_name_folder}/{plugin_file_name}"
        logger.debug(f"file_path={file_path}")
        new_file_name = f"files/{plugin_file_name}"
        file_content = open(file_path, "rb").read()
        reporesponse = sgh.create_update_repo_file(repo, list_of_existing_files, new_file_name, file_content)

    return reporesponse

def copy_files_to_repo(ucproduct, repo, plugin):
    list_of_existing_files=[]
#    if repo.size > 0: 
    list_of_existing_files = sgh.get_gh_repo_files_list(repo)

    # Walk through the directory tree and add files to the repository
    config = myutils.get_config()
    root_dir = f"{config.get(myutils.PLUGIN_DOCS_ROOT)}/docs/{ucproduct}/{plugin.get(myutils.PLUGIN_DOCS_FOLDER)}"
    logger.info(f"root_dir={root_dir}")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            logger.info(f"for file in files={file}")
            # skip downloads.md for now
            if file=="downloads.md": continue

            file_path = os.path.join(root, file)
            splitted=file_path.split(root_dir+"/")
            new_file_name = f"docs/{splitted[1]}"

            # do not process existing files
            logger.info(f"new_file_name={new_file_name} - orig_file_path={file_path}")
            if (".md" in file):
                # remove the navbar from markdownfile, not needed here
                file_content = remove_navbar(file_path)
            else:
                file_content = open(file_path, "rb").read()
            if file=="README.md": new_file_name = "docs/index.md"
            reporesponse = sgh.create_update_repo_file(repo, list_of_existing_files, new_file_name, file_content)
    
    # copy special files to repository

    reporesponse = copy_special_files_to_repo(ucproduct, repo, plugin)
    # create info.json 
    reporesponse = create_info_json(ucproduct, plugin, repo, list_of_existing_files)

    # create releases.json 
    reporesponse = create_releases_json(ucproduct, plugin, repo, list_of_existing_files)

    # create downloads.md 
    reporesponse = create_downloads_md(ucproduct, plugin, repo, list_of_existing_files)

    # create history
    reporesponse = create_history_md(plugin, repo, list_of_existing_files)
    
    # create mkdocs.yml
    reporesponse = create_mkdocs_yml(ucproduct, plugin, repo, list_of_existing_files)
    
    setup_ghpages(ucproduct, plugin, repo, list_of_existing_files)
    return reporesponse


def migrate_product_plugin(ucproduct, plugin_list):
    logger.info(f"{ucproduct}")

# DEBUG:
    debug_counter=5

    for plugin in plugin_list:

# DEBUG:
        # if (not plugin.get(myutils.PLUGIN_DOCS_FOLDER) == "WebSphereLiberty"): continue 

        logger.info(f"processing plugin: {plugin[myutils.PLUGIN_NAME]}")
        
        # skip all plugins where publish flag is not set
        if (not plugin[myutils.PUBLISH]): continue
        # TODO: for now skip where no docs are not available - later create repo without docs instead
        if (plugin[myutils.PLUGIN_NAME] == myutils.DOCS_NOT_FOUND): continue

        repo = sgh.gh_get_repo(ucproduct,plugin) # gh_create_repository(ucproduct, plugin)
        logger.info(f"REPO.SIZE={repo.size}")

        # migrate original docs to new repo
        copy_files_to_repo(ucproduct, repo, plugin)
        
        # create releases for each file
        sgh.gh_create_release(repo, ucproduct, plugin)


# DEBUG:
        debug_counter-=1
        if debug_counter == 0:break

def main():

    print ("Migrating Plug-Ins and documentation")
    logger.info("Migrating Plug-Ins and documentation")
    config = myutils.get_config()
    for product in ["UCB"]: #  ["UCB", "UCD", "UCR", "UCV"]
        logger.info(f"product={product}")
        product_plugins = myutils.get_product_doc_plugin_list(product)
        migrate_product_plugin(product, product_plugins)

if __name__ == '__main__':
    #main(sys.argv[1:])
    main()
    