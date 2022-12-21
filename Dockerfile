FROM public.ecr.aws/lambda/python:3.9
WORKDIR /usr/src
COPY requirements.txt ./
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN rm -r requirements.txt
COPY alembic/ ${LAMBDA_TASK_ROOT}/alembic
COPY app/ ${LAMBDA_TASK_ROOT}/app/
COPY alembic.ini ${LAMBDA_TASK_ROOT}
COPY .env . 
CMD ["app.main.handler"]
