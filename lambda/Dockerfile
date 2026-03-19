FROM public.ecr.aws/lambda/python:3.9

# Instala dependências direto no ambiente padrão
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY app.py ${LAMBDA_TASK_ROOT}
COPY model.pkl ${LAMBDA_TASK_ROOT}

CMD ["app.lambda_handler"]
