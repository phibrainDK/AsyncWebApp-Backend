FROM public.ecr.aws/lambda/python:3.9

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install --upgrade pip-tools

COPY pip/with-dep/requirements-prod.txt ./pip/with-dep/requirements-prod.txt

RUN pip install -r ./pip/with-dep/requirements-prod.txt

COPY api/ ./api/
COPY business_logic/ ./business_logic/
COPY common/ ./common/
COPY schemas/ ./schemas/
COPY external_services/ ./external_services/
COPY *.py ./

CMD [ "api.main.handler" ]
