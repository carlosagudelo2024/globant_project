# routes/__init__.py
from  app.routes.department import router as department_router
from  app.routes.job import router as job_router
from  app.routes.hired import router as employee_router

# Esto permite importar así:
# from routes import department_router, job_router, employee_router