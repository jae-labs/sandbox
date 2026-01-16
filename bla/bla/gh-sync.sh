#!/bin/bash

# Note: Not using set -e to allow parallel operations to continue even if some fail

# Function to fetch all paginated results from GitHub API
fetch_github_repos() {
  local base_url=$1
  local page=1
  local per_page=100

  while true; do
    local sep="?"
    [[ "$base_url" == *"?"* ]] && sep="&"

    local response=$(curl -sfL -H "Accept: application/vnd.github.inertia-preview+json" \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      "${base_url}${sep}page=${page}&per_page=${per_page}" 2>/dev/null) || break

    local count=$(echo "$response" | jq 'length' 2>/dev/null)
    if ! [[ "$count" =~ ^[0-9]+$ ]] || [ "$count" -eq 0 ]; then
      break
    fi

    echo "$response" | jq -r '.[] | .ssh_url'
    ((page++))
  done
}

# Function to clone repos from an API endpoint into a target directory
clone_repos() {
  local api_url=$1
  local target_dir=$2

  echo "Cloning repos from $api_url to $target_dir"
  mkdir -p "$target_dir"
  cd "$target_dir"

  local -a repo_urls=()
  while IFS= read -r url; do
    repo_urls+=("$url")
  done < <(fetch_github_repos "$api_url")
  for repo_url in "${repo_urls[@]}"; do
    local folder=$(echo "$repo_url" | awk -F ":" '{ print $2}' | awk -F "/" '{ print $2 }' | sed 's/.git$//g')
    mkdir -p "$folder"
    echo "$repo_url"
    if ! git clone "$repo_url" "$folder" 2>&1 | grep -v "already exists and is not an empty directory"; then
      :
    fi
  done
}

# Fetch all organizations the user is part of
echo "Discovering GitHub organizations..."
ORGS=$(curl -sfL -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/user/orgs" | jq -r '.[].login')

# Clone org repositories (requires $GITHUB_TOKEN with repo scope for private repos)
declare -a ORG_FOLDERS=()
for org in $ORGS; do
  echo "Found organization: $org"
  clone_repos "https://api.github.com/orgs/$org/repos" "${HOME}/gh_${org}"
  ORG_FOLDERS+=("${HOME}/gh_${org}")
done

# Use authenticated /user/repos so private personal repos are included; limit to repos you own
clone_repos "https://api.github.com/user/repos?visibility=all&affiliation=owner" "${HOME}/gh_personal"

echo ""
echo ">>> GIT Pulling..."
echo ""

# Folders to pull - combine org folders with personal folder
FOLDERS=("${ORG_FOLDERS[@]}" "${HOME}/gh_personal")

# Collect all git directories first
declare -a GIT_DIRS=()
for i in "${FOLDERS[@]}"; do
  echo "Scanning folder: $i"
  local_count=0
  while IFS= read -r dir; do
    GIT_DIRS+=("$dir")
    ((local_count++))
  done < <(find -L "$i" -name .git -type d 2>/dev/null | sed 's/.git$//g')
  echo "Found $local_count repos in $i"
done

echo "Total repos to pull: ${#GIT_DIRS[@]}"
echo ""

# Run git operations in parallel on all directories
printf '%s\n' "${GIT_DIRS[@]}" | parallel --will-cite --halt never "echo \"Pulling: {}\" && cd {} && git remote prune origin >/dev/null 2>&1; (git checkout main >/dev/null 2>&1 || git checkout master >/dev/null 2>&1 || true); git pull >/dev/null 2>&1 || echo \">>> FAILED: {}\""

# Remove all branches other than main locally, garbage collection, display git ignored files
#git branch | grep -v \"main\" | xargs git branch -D | git gc | git clean -xdn
