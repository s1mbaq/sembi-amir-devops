# Integrated DevOps workflow

Linux provides the shell, files, permissions and processes for development.
Git records meaningful changes and isolates work in branches.
GitHub stores the remote repository that Jenkins checks out.
Jenkins validates the project and runs the automated application tests.
Only after these checks pass does Jenkins build the Docker image.
Docker starts a container from that image and exposes the HTTP service.
Jenkins verifies health and student data before the run can succeed.
A failing command stops its stage and skips later deployment stages.
