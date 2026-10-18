FROM python:3.13-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PORT=8080
COPY app/ ./app/
COPY config/ ./config/
RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin appuser \
    && python -m compileall -q app
USER appuser
EXPOSE 8080
HEALTHCHECK --interval=3s --timeout=2s --start-period=5s --retries=10 \
    CMD python -c "import os,urllib.request; urllib.request.urlopen('http://127.0.0.1:'+os.getenv('PORT','8080')+'/health',timeout=1)" || exit 1
CMD ["python", "app/main.py"]
