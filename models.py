from pydantic import BaseModel

class Contract(BaseModel):
    nombre: str
    numero_identificacion: str
    tipo_contrato: str

