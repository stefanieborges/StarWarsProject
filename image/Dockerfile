FROM public.ecr.aws/lambda/python:3.13

# Copia requirements
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Instala dependências
RUN pip install -r requirements.txt

# Copia a pasta app como módulo
COPY app ${LAMBDA_TASK_ROOT}/app

ENV IS_AWS=true

# Define o handler corretamente
CMD [ "app.main.handler" ]
