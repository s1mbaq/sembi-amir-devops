# DevOps Project — Amir Sembi

A personal Linux, Git, Docker and Jenkins project for Laboratory Work 1.
The Python application serves a student information page, JSON data and a health endpoint.
It uses only the Python standard library.

## Start here

Read [the Windows 11 setup guide](docs/SETUP_WINDOWS_RU.md) or
[the Mac setup guide](docs/SETUP_RU.md).
Confirmed personal data: Amir Sembi, group IT2-2307, Student ID 37693.
The archive includes a local `.env` with these ordinary application settings.
After a Git clone, regenerate the ignored `.env` with:
`python3 scripts/personalize.py --group IT2-2307 --student-id 37693`.

## Project Structure and Naming

| Element | Name |
| --- | --- |
| Project directory | `sembi_amir` |
| Information file | `Sembi_Amir_info.txt` |
| Bash script | `scripts/Sembi_Amir_system.sh` |
| Repository and image | `sembi-amir-devops` |
| Application container | `sembi-amir-container` |
| Jenkins job | `Sembi_Amir_DevOps` |

## Application

| Route | Response |
| --- | --- |
| `/` | HTML student information |
| `/api/student` | JSON student information |
| `/health` | HTTP 200 and `{"status":"ok"}` |

The application reads `config/student.json`. The four `STUDENT_*` environment
variables override the corresponding defaults. `config/app.conf` stores the
application name, version, message and port.

## Local checks

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_personalization.py
```

There are ten tests. They cover configuration, all environment overrides,
partial overrides, HTML escaping, the live HTTP routes and a missing route.

## Docker and Jenkins

After personalization:

```bash
docker compose up --build -d
docker compose ps
docker compose down
docker compose -f infra/jenkins-compose.yml up --build -d
```

| Address | Service |
| --- | --- |
| `http://localhost:8080` | Application started directly or with Compose |
| `http://localhost:8081` | Jenkins |
| `http://localhost:8082` | Application deployed by Jenkins |

Jenkins uses a separate Docker-in-Docker daemon with TLS. Inspect its images
and containers through `docker compose -f infra/jenkins-compose.yml exec jenkins docker ps`.
The Jenkinsfile has Checkout, Build, Test, Docker Build and Docker Run stages.
An unsuccessful command fails its stage; later stages are skipped.

This is a local educational setup. The Python development server and builds
on the Jenkins controller are intended for this single-user laboratory.
Do not use the privileged Docker service to execute untrusted repositories.

## Evidence and documentation

- [Setup and troubleshooting](docs/SETUP_RU.md)
- [Commands for Tasks 1 through 21](docs/COMMANDS_RU.md)
- [Video demonstration plan](docs/VIDEO_RU.md)
- [Answers for individual verification](docs/DEFENSE_RU.md)
- [Submission and screenshot checklist](docs/SUBMISSION_RU.md)
- [Verification scope](docs/VERIFICATION.md)
- [Official references](docs/REFERENCES.md)

Run `scripts/prepare_linux.sh` after cloning: Git does not preserve empty
directories, log files or all Unix permission bits. The script recreates
runtime folders and the sample log, and sets the demonstration permissions.

This project was developed as part of my DevOps coursework. It demonstrates Linux administration, Git version control, Docker containerization, and CI/CD automation using Jenkins. The repository also includes technical documentation, verification results, and supporting materials for the project demonstration.
