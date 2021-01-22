# Overview

Instructions for setup can be found here: <https://psiturk.readthedocs.io/en/latest/heroku.html>. Make sure that you run through all the instructions whenever setting up a new app on Heroku.

A number of the instructions can be streamlined by running `python set-heroku-settings.py`.

# Details

## Git Remote

When using the Heroku command line tools, they will determine the current app from the git remote.
So make sure you set the git remote and are in the appropriate project folder.

## Buildpacks

Make sure that the app is configured with buildpacks for both Python and for nodejs.

The python buildpack is needed to run the app, and the node buildpack is needed to automatically generate the compiled version of the task.

You can add a second buildpack as follows:
`heroku buildpacks:add --index 2 heroku/nodejs`

## Files

1. `Procfile`

This file contains the command that Heroku will use when it launches. This typically will call on python directly.

2. `requirements.txt`

Heroku will automatically install all python requirements listed in this file.

3. `package.json`

Heroku will generate the compiled javascript files by installing the packages listed under `devDependencies` and then running the `postinstall` hook.

# Useful commands

1. `heroku ps:exec`

Open a shell on the remote server.

2. `heroku logs --tail`

Show logs from the current Heroku session.
