FROM python:3.12

ENV PATH="/root/.local/bin/:$PATH"

RUN apt update && \
    apt upgrade -y && \
    apt install postgresql-client-15 -y

RUN ln -sf /usr/share/zoneinfo/Africa/Johannesburg /etc/localtime && \
    ln -sf /usr/share/zoneinfo/Africa/Johannesburg /etc/timezone

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN mkdir /root/app/

RUN mkdir -p /home/kevin/projects/tread-events-python/images/
RUN mkdir -p /home/kevin/projects/tread-events-python/

COPY tread-media-f50f10bbaaf3.json /home/kevin/projects/tread-events-python/

COPY pyproject.toml /root/app/
COPY .env.prod /root/app/

WORKDIR /root/app/
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root

COPY /app/ /root/app/

COPY start.sh /root/

RUN chmod 777 /root/*.sh

CMD [ "/root/start.sh" ]