# Examen de certificación - QueridoDiario
# Autora: Isidora Valenzuela 

# QueridoDiario Examen Certificación
QueridoDiario es una aplicación web para gestionar entradas de diario personal de forma privada y segura.

## Descripción
Proyecto desarrollado para el examen final de certificación Full Stack Python. La plataforma permite a los usuarios crear una cuenta, iniciar sesión y administrar sus entradas personales mediante un CRUD completo con restricciones estricta de autoría y privacidad.

## Tecnologías utilizadas en mi examen:
- Backend: Python con Flask.
- Base de Datos: MySQL con relaciones.
- Seguridad: Encriptación de contraseñas con Bcrypt y manejo seguro de sesiones.
- Frontend: Plantillas Jinja2 con diseño responsivo mediante Bootstrap.

## Resumen de Módulos
- Módulo Usuarios: Registro e inicio de sesión seguro con validaciones, restricción de edad mínima (18 años) y hash de contraseña.
- Módulo Entradas: Creación, lectura, modificación y eliminación de registros personales (diario) con filtrado estricto por usuario en sesión.
- Módulo Búsqueda: Filtro dinámico de entradas a través de la URL según el contenido de las notas.

## Instalación y Ejecución

1. **Clonar o descargar el repositorio:**
   Puede ubicarse en la carpeta raíz del proyecto.

2. **Instalar dependencias:**
    Luego instalar las dependencias de esta manera: 
   ```bash
   pip install -r requirements.txt