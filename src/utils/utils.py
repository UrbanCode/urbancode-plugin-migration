import os
from pathlib import Path
import logging
import json

script_name="utils.log" 
#script_name=Path(__file__).stem
#logging.basicConfig(filename=script_name,
#                    format="[%(filename)s:%(lineno)s - %(funcName)20s() - %(levelname)s] %(message)s",
#                    filemode='w')


# Creating an object
loggerU = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(script_name)
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

# Setting the threshold of logger to DEBUG
c_format = logging.Formatter('[%(filename)s:%(lineno)s - %(funcName)30s() - %(levelname)s] %(message)s')
f_format = logging.Formatter('[%(filename)s:%(lineno)s - %(funcName)30s() - %(levelname)s] %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
loggerU.addHandler(c_handler)
loggerU.addHandler(f_handler)

DOCS_NOT_FOUND = "DOCS_NOT_FOUND"
NOT_PLUGIN_FILE = "NOT PLUGIN FILE"
NOT_PLUGIN_FILE_SPECIAL_PLUGIN = "NOT PLUGIN FILE - SPECIAL"
NOT_PLUGIN_FILE_SAMPLE_OR_TEMPLATE = "NOT PLUGIN FILE - SAMPLE OR TEMPLATE"
ERROR_FILE_DAMAGED = "ERROR FILE DAMAGED"
MULTIVOLUME_FILE = "MULTIVOLUME FILE"

GITHUB_API_BASE_URL="GITHUB_API_BASE_URL"
GITHUB_API_URL="GITHUB_API_URL"
GITHUB_TOKEN="GITHUB_TOKEN"
GITHUB_USER="GITHUB_USER"
GITHUB_EMAIL="GITHUB_EMAIL"

# Plug-In documentation settings
PLUGIN_DOCS_ROOT="PLUGIN_DOCS_ROOT"
PLUGIN_DOCS_REPO="PLUGIN_DOCS_REPO"
PLUGIN_DOCS_FOLDER="PLUGIN_DOCS_FOLDER"
PLUGIN_DOCS_FILES_FOLDER="PLUGIN_DOCS_FILES_FOLDER"

# Plug-in files settings
UCD_PLUGIN_FILES_ROOT="UCD_PLUGIN_FILES_ROOT"
UCD_PLUGIN_FILES_REPO="UCD_PLUGIN_FILES_REPO"
NEW_UCD_ORG="NEW_UCD_ORG"

UCV_PLUGIN_FILES_ROOT="UCV_PLUGIN_FILES_ROOT"
UCV_PLUGIN_FILES_REPO="UCV_PLUGIN_FILES_REPO"
NEW_UCV_ORG="NEW_UCV_ORG"

UCR_PLUGIN_FILES_ROOT="UCR_PLUGIN_FILES_ROOT"
UCR_PLUGIN_FILES_REPO="UCR_PLUGIN_FILES_REPO"
NEW_UCR_ORG="NEW_UCR_ORG"

UCB_PLUGIN_FILES_ROOT="UCB_PLUGIN_FILES_ROOT"
UCB_PLUGIN_FILES_REPO="UCB_PLUGIN_FILES_REPO"
NEW_UCB_ORG="NEW_UCB_ORG"


PLUGIN_INDEX_REPO="PLUGIN_INDEX_REPO"
PLUGIN_INDEX_ROOT="PLUGIN_INDEX_ROOT"
PLUGIN_INDEX_FOLDER="PLUGIN_INDEX_FOLDER"

UCX_PLUGIN_FILES_FOLDER="UCX_PLUGIN_FILES_FOLDER"
UCX_DOCS_FILES_FOLDER="UCX_DOCS_FILES_FOLDER"
UCX_META_INFO_FOLDER="UCX_META_INFO_FOLDER"

ZIP_TEMP_DIR = "ZIP_TEMP_DIR"
PLUGIN_DOCS_MEDIA_FOLDER_NAME="PLUGIN_DOCS_MEDIA_FOLDER_NAME"

PLUGIN_NAME="name"
PLUGIN_DOCS_FOLDER="docs_folder"
PLUGIN_FILES_FOLDER="plugin_folder"
PLUGIN_NEW_REPO_NAME="NEW_FOLDER_NAME"
PLUGIN_FILES="PLUGIN_FILES"

MAPDIC = {
    "UCB" : {
        "SHORTNAME": "Build",
    },
    "UCD" : {
        "SHORTNAME": "Deploy"
    },
    "UCR" : {
        "SHORTNAME": "Release"
    },
    "UCV" : {
        "SHORTNAME": "Velocity"
    }
}

# Author template field names
AUTHOR_NAME="name"
AUTHOR_EMAIL="email"

# Author details
def get_author_template():
    return {
        AUTHOR_NAME: "",
        AUTHOR_EMAIL: ""
    }

# Plugin specification field names
PLUGIN_SPECIFICATION_CATEGORIES="categories"
PLUGIN_SPECIFICATION_TYPE="type"

# category: SCM, Source, Automation, ..
# type: OSS, PARTNER, IBM, ..
def get_plugin_specification_template():
    return {
        PLUGIN_SPECIFICATION_CATEGORIES: [],
        PLUGIN_SPECIFICATION_TYPE: ""
    }


# info template field names
INFO_NAME="name"
INFO_DOCS_URL="docsURL"
INFO_SOURCE_PROJECT="source_project"
INFO_DESCRIPTION="description"
INFO_PLUGIN_SPECIFICATION="specification"
INFO_AUTHOR="author"

PUBLISH="publish"

def get_info_template():
    return {
        INFO_NAME: "",
        INFO_DOCS_URL: "",
        INFO_SOURCE_PROJECT: "",
        INFO_DESCRIPTION: "",
        INFO_PLUGIN_SPECIFICATION: get_plugin_specification_template(),
        INFO_AUTHOR: get_author_template(),
        PUBLISH: True
    }

RELEASE_VERSION="version" 
RELEASE_SEMVER="semver" 
RELEASE_DATE="date"  
RELEASE_FILE="file"
RELEASE_IMAGE="image"
RELEASE_NOTES="notes"
RELEASE_SUPPORTS="supports"
RELEASE_SORTVERSION="SORT_VERSION"

def get_release_template():
    return {
        RELEASE_VERSION:"0", 
        RELEASE_SEMVER:"0.0", 
        RELEASE_DATE:"",  
        RELEASE_FILE:"",
        RELEASE_NOTES:[],
        RELEASE_SUPPORTS:"",
        RELEASE_SORTVERSION: ""
    }


def get_repo_name (ucproduct, plugin):
    ucproduct_shortname = get_productshortname(ucproduct)
    repo_name = f"{ucproduct_shortname.lower()}-{plugin.get(PLUGIN_NEW_REPO_NAME).lower()}"
    return repo_name

def get_dir_names(src):
    # getting the absolute path of the source
    # directory
    src = os.path.abspath(src)
    loggerU.info(f"Source: {src}")

    list_subfolders_with_paths = [f.name for f in os.scandir(src) if f.is_dir()]
    return sorted(list_subfolders_with_paths)

# def get_info_template():
#     return {
#         PLUGIN_NAME: "",
#         PLUGIN_DOCS_FOLDER: "",
#         PLUGIN_FILES_FOLDER:"",
#         PLUGIN_NEW_REPO_NAME: ""
#     }

def get_organization(ucproduct):
    loggerU.info(f"product:{ucproduct}")
    org_name = get_productshortname(ucproduct)
    org_name = org_name + "-Plugins"
    # if (ucproduct=="UCB"): return config[NEW_UCB_ORG]
    # if (ucproduct=="UCD"): return config[NEW_UCD_ORG]
    # if (ucproduct=="UCR"): return config[NEW_UCR_ORG]
    # if (ucproduct=="UCV"): return config[NEW_UCV_ORG]
    return org_name

def get_productshortname(ucproduct):
    loggerU.info(f"product:{ucproduct}")
#    config = get_config()
    prod = MAPDIC.get(ucproduct, "")
    loggerU.info(f"product:{prod}")
    shortname = "ERROR"
    if prod != "" : shortname = prod.get("SHORTNAME")
    loggerU.info(f"shortname:{shortname}")
    return shortname

def get_product_doc_plugin_list(ucproduct):
    loggerU.info(f"product:{ucproduct}")
    # open product-list.json file and put it into a dictionary and return it
    pdpdict=[]
    config = get_config()
    config[PLUGIN_INDEX_ROOT]
    loggerU.info(f"plugin_index_root:{config[PLUGIN_INDEX_ROOT]}")
    with open(f'{config[PLUGIN_INDEX_ROOT]}/{ucproduct}-list.json', "r") as json_file:
        templist = json.load(json_file)
        pdpdict = templist[ucproduct]
    return pdpdict

def get_plugin_files_root(ucproduct):
    loggerU.info(f"product:{ucproduct}")
    config = get_config()
    if (ucproduct=="UCB"): return config[UCB_PLUGIN_FILES_ROOT]
    if (ucproduct=="UCD"): return config[UCD_PLUGIN_FILES_ROOT]
    if (ucproduct=="UCR"): return config[UCR_PLUGIN_FILES_ROOT]
    if (ucproduct=="UCV"): return config[UCV_PLUGIN_FILES_ROOT]
    return "ERROR"

def get_config():

    # TODO: read from config file instead of environment variables
    loggerU.info("configuration read")

    return {
        GITHUB_API_BASE_URL: os.getenv(GITHUB_API_BASE_URL, ""),
        GITHUB_API_URL: os.getenv(GITHUB_API_URL, ""),
        GITHUB_TOKEN: os.getenv(GITHUB_TOKEN, ""),
        GITHUB_USER: os.getenv(GITHUB_USER, ""),
        GITHUB_EMAIL: os.getenv(GITHUB_EMAIL, ""),        
        PLUGIN_DOCS_ROOT: os.getenv(PLUGIN_DOCS_ROOT, ""),
        PLUGIN_DOCS_FOLDER: os.getenv(PLUGIN_DOCS_FOLDER, ""),
        PLUGIN_DOCS_FILES_FOLDER: os.getenv(PLUGIN_DOCS_FILES_FOLDER, ""),
        PLUGIN_DOCS_REPO: os.getenv(PLUGIN_DOCS_REPO, ""),
        UCD_PLUGIN_FILES_REPO: os.getenv(UCD_PLUGIN_FILES_REPO, ""),
        UCD_PLUGIN_FILES_ROOT: os.getenv(UCD_PLUGIN_FILES_ROOT, ""),
        NEW_UCD_ORG: os.getenv(NEW_UCV_ORG, ""),
        UCV_PLUGIN_FILES_REPO: os.getenv(UCV_PLUGIN_FILES_REPO, ""),
        UCV_PLUGIN_FILES_ROOT: os.getenv(UCV_PLUGIN_FILES_ROOT, ""),  
        NEW_UCV_ORG: os.getenv(NEW_UCV_ORG, ""),      
        UCR_PLUGIN_FILES_REPO: os.getenv(UCR_PLUGIN_FILES_REPO, ""),
        UCR_PLUGIN_FILES_ROOT: os.getenv(UCR_PLUGIN_FILES_ROOT, ""),
        NEW_UCR_ORG: os.getenv(NEW_UCR_ORG, ""),
        UCB_PLUGIN_FILES_REPO: os.getenv(UCB_PLUGIN_FILES_REPO, ""),
        UCB_PLUGIN_FILES_ROOT: os.getenv(UCB_PLUGIN_FILES_ROOT, ""),
        NEW_UCB_ORG: os.getenv(NEW_UCB_ORG, ""),
        PLUGIN_INDEX_REPO: os.getenv(PLUGIN_INDEX_REPO, ""),
        PLUGIN_INDEX_ROOT: os.getenv(PLUGIN_INDEX_ROOT, ""),
        PLUGIN_INDEX_FOLDER: os.getenv(PLUGIN_INDEX_FOLDER, ""),
        UCX_PLUGIN_FILES_FOLDER: os.getenv(UCX_PLUGIN_FILES_FOLDER, ""),
        UCX_DOCS_FILES_FOLDER: os.getenv(UCX_DOCS_FILES_FOLDER, ""),
        UCX_META_INFO_FOLDER: os.getenv(UCX_META_INFO_FOLDER, ""),
        ZIP_TEMP_DIR: os.getenv(ZIP_TEMP_DIR, ""),
        PLUGIN_DOCS_MEDIA_FOLDER_NAME: os.getenv(PLUGIN_DOCS_MEDIA_FOLDER_NAME, "")
    }

def is_compareable_file(file_name):
    do_compare = True
    list_of_binary_file_endings=[".zip", ".001", ".002", ".003", ".004", ".005" ,".006", ".007", ".008" ,".009", ".gif", ".jpg", ".png", ".pdf", "7z", "jpeg"]
    last4 = file_name[-4:].lower()
    for ending in list_of_binary_file_endings:
        if last4 in ending: 
            do_compare = False
            break
        
    return do_compare

def main():

    print ("Utility Functions for urbancode migration project")
    config=get_config()
    os._exit(0)

if __name__ == '__main__':
    #main(sys.argv[1:])
    main()
    