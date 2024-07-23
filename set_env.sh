#!/bin/bash

# Define environment variables for source repositories 

# first Github URLs for Base and API
export GITHUB_API_BASE_URL="https://github.com"
## export GITHUB_API_URL="https://github.com/api/v3"
export GITHUB_API_URL="https://api.github.com"
export GITHUB_USER="YOUR_GITHUB_USER"
export GITHUB_EMAIL="YOUR_GITHUB_EMAIL"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"


# Plugin documentation variables
export PLUGIN_DOCS_ROOT="$HOME/PLUGINS/IBM-UCx-PLUGIN-DOCS"
export PLUGIN_DOCS_REPO="https://github.com/UrbanCode/IBM-UCx-PLUGIN-DOCS.git"
export PLUGIN_DOCS_FOLDER="docs"
export PLUGIN_DOCS_FILES_FOLDER="files"

# structure
# <product_name>_FILES_ROOT= path to local copy of repository
# <product_name>_FILES_REPO= url to github repository
# NEW_<product>_ORG= top level organization which will contain all plug-in repositories for this product


# Deploy plug-ins
export UCD_PLUGIN_FILES_ROOT="$HOME/PLUGINS/IBM-UCD-PLUGINS"
export UCD_PLUGIN_FILES_REPO="https://github.com/UrbanCode/IBM-UCD-PLUGINS.git"
export NEW_UCD_ORG="Devops-Deploy-Plugins"
#export NEW_UCD_ORG="Deploy-Plugins"

# Velocity plug-ins
export UCV_PLUGIN_FILES_ROOT="$HOME/PLUGINS/IBM-UCV-PLUGINS"
export UCV_PLUGIN_FILES_REPO="https://github.com/UrbanCode/IBM-UCV-PLUGINS.git"
export NEW_UCV_ORG="Devops-Velociy-Plugins"
#export NEW_UCV_ORG="Velocity-Plugins"

# Release plug-ins
export UCR_PLUGIN_FILES_ROOT="$HOME/PLUGINS/IBM-UCR-PLUGINS"
export UCR_PLUGIN_FILES_REPO="https://github.com/UrbanCode/IBM-UCR-PLUGINS.git"
export NEW_UCR_ORG="Devops-Release-Plugins"
#export NEW_UCR_ORG="Release-Plugins"

# Build plug-ins
export UCB_PLUGIN_FILES_ROOT="$HOME/PLUGINS/IBM-UCB-PLUGINS"
export UCB_PLUGIN_FILES_REPO="https://github.com/UrbanCode/IBM-UCB-PLUGINS.git"
export NEW_UCB_ORG="Devops-Build-Plugins"
#export NEW_UCB_ORG="Build-Plugins"

# plugin-index local folder, repository and folder where file is stored
export PLUGIN_INDEX_ROOT="$HOME/PLUGINS/urbancode-plugins-index"
export PLUGIN_INDEX_REPO="https://github.com/UrbanCode/urbancode-plugins-index.git"
export PLUGIN_INDEX_FOLDER="plugins"

# folder names which will be used in the new target repositories for the plug-ins
export UCX_PLUGIN_FILES_FOLDER="files"
export UCX_DOCS_FILES_FOLDER="docs"
export UCX_META_INFO_FOLDER="plugin"

# other variables

# temp folder 
export ZIP_TEMP_DIR="$HOME/PLUGINS/TEMP"

# name of the folder which will contain all media files. is used in each plugin folder!
export PLUGIN_DOCS_MEDIA_FOLDER_NAME="media"

