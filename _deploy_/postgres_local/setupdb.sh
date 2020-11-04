#!/bin/bash

GitRepoRoot=$(pwd | sed -e 's/\(.*eventmicro\).*/\1/')
echo $GitRepoRoot
SetupDbCommand="sudo -u postgres psql -f ${GitRepoRoot}/_deploy_/postgres_local/eventmicrodbsetup.sql"

echo "List Existing Database"
echo '\list' | sudo -u postgres psql

echo "List Existing Users"
echo '\du' | sudo -u postgres psql

echo "Configure eventmicro Database"
echo "..."
echo ${SetupDbCommand}
${SetupDbCommand}

echo "Listing Updated Database"
echo '\list' | sudo -u postgres psql

echo "Listing Updated Users"
echo '\du' | sudo -u postgres psql



