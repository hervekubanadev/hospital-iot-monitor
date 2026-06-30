FROM python:3.11-slim AS base

WORKDIR /app

COPY hospital_system.py .

RUN groupadd -r hospital && useradd -r -g hospital hospital

RUN mkdir -p /app/active_logs /app/archived_logs /app/reports && \
    chown -R hospital:hospital /app && \
    chmod 700 /app/active_logs

USER hospital

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD pgrep -f hospital_system.py || exit 1

FROM base AS production

CMD ["python3", "hospital_system.py", "start"]

FROM base AS development

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    shellcheck \
    && rm -rf /var/lib/apt/lists/*
USER hospital

CMD ["tail", "-f", "/dev/null"]
