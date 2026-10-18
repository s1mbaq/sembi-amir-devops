#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
if [ -e .git ]; then
    printf 'A Git repository already exists. It has not been changed.\n' >&2
    exit 1
fi
if [ "$#" -ne 2 ]; then
    printf 'Usage: bash scripts/init_history.sh "Amir Sembi" "your verified Git email"\n' >&2
    exit 1
fi
if [[ "$2" != *@* ]] || [[ "$2" == *' '* ]]; then
    printf 'Enter your GitHub-verified email or your exact GitHub noreply address.\n' >&2
    exit 1
fi
python3 scripts/validate_personalization.py
bash scripts/prepare_linux.sh
git init -b main
git config user.name "$1"
git config user.email "$2"
git add .gitignore README.md app/.gitkeep scripts/.gitkeep config/.gitkeep logs/.gitkeep tests/.gitkeep infra/.gitkeep docs/.gitkeep
git commit -m "Create project structure and ignore local runtime files"
git add Sembi_Amir_info.txt config/student.json .env.example private.txt public.txt
git commit -m "Add personalized student information and permission examples"
git add scripts/
git commit -m "Add Linux system information and project setup scripts"
git add app/ tests/ config/app.conf
git commit -m "Implement student HTTP application and ten automated tests"
git add Dockerfile .dockerignore docker-compose.yml infra/Linux.Dockerfile infra/linux-compose.yml
git commit -m "Containerize the application and add the Linux workspace"
git add Jenkinsfile infra/Jenkins.Dockerfile infra/jenkins-compose.yml
git commit -m "Add Jenkins build test and Docker deployment pipeline"
git add docs/
git commit -m "Document setup demonstration and verification requirements"
git branch development
git switch development
cat > docs/WORKFLOW.md <<'WORKFLOW'
# Integrated DevOps workflow

Linux provides the shell, files, permissions and processes for development.
Git records meaningful changes and isolates work in branches.
GitHub stores the remote repository that Jenkins checks out.
Jenkins validates the project and runs the automated application tests.
Only after these checks pass does Jenkins build the Docker image.
Docker starts a container from that image and exposes the HTTP service.
Jenkins verifies health and student data before the run can succeed.
A failing command stops its stage and skips later deployment stages.
WORKFLOW
git add docs/WORKFLOW.md
git commit -m "Explain the integrated DevOps workflow on development branch"
git switch main
git merge --no-ff development -m "Merge development workflow documentation"
git status
git log --oneline --graph --all
printf '\nReal commits were created from staged changes. Nothing was pushed to GitHub.\n'
