#!/bin/bash

files="files/test.txt,files/test2.txt"
echo $files | sed -n 1'p' | tr ',' '\n' | while read file; do
  echo "Updating file: $file"

  # get the files new content
  new_content=$(cat $file)
  new_content="$new_content\n$(date)"

  # Base64 encode the new content
  new_content_base64=$(echo -n $new_content | base64)

  # Update the file with github api
  curl -i -X PUT \
    -H "Authorization: token $GITHUB_TOKEN" \
    -d "{\"message\":\"feat($file): update file contents\",\"committer\":{\"name\":\"github-file-updater\",\"email\":\"no-reply@github.com\"},\"content\":\"${new_content_base64}\"}" \
    https://api.github.com/repos/apollorion/$GITHUB_REPOSITORY/contents/$file

done