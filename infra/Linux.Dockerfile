FROM python:3.13-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends bash git procps less \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 1000 --create-home --shell /bin/bash student
USER student
WORKDIR /home/student/devops/sembi_amir
CMD ["bash"]
