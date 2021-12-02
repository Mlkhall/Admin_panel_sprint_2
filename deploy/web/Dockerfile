FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR ./admin_panel

COPY . .

EXPOSE 8000/tcp

RUN pip install --upgrade pip
RUN pip install -r movies_admin/requirements.txt

COPY deploy/web/docker-entrypoint.sh .

RUN sed -i 's/\r$//g' docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh


