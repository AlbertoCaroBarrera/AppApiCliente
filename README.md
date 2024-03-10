# README

## Descripción
Este proyecto es una aplicación web para un hotel que ofrece funcionalidades de reserva de habitaciones, gestión de clientes, administración de servicios y promociones, entre otras características.

## Características principales
- **Reserva de habitaciones:** Los clientes pueden realizar reservas de habitaciones en línea, seleccionando fechas de entrada y salida, así como el tipo de habitación deseado.
- **Gestión de clientes:** La aplicación permite gestionar la información de los clientes, incluyendo sus datos personales, reservas realizadas y comentarios.
- **Administración de servicios:** Los administradores pueden agregar, editar y eliminar servicios disponibles en el hotel, como desayuno, almuerzo, cena, entre otros.
- **Rebajas en aniversarios del usuario**

## Tecnologías utilizadas
- **Django:** Framework de desarrollo web en Python que proporciona un conjunto de herramientas para construir aplicaciones web de manera eficiente y escalable.
- **HTML/CSS:** Lenguajes de marcado y estilos para la estructura y presentación de la interfaz de usuario.
- **Bootstrap:** Framework de diseño frontend que facilita la creación de interfaces de usuario atractivas y responsivas.
- **JavaScript:** Lenguaje de programación utilizado para agregar interactividad a la aplicación web.

## Instalación y configuración
1. Clona el repositorio desde GitHub: `git clone https://github.com/tu-usuario/nombre-proyecto.git`
2. Crea y activa un entorno virtual para el proyecto.
3. Instala las dependencias del proyecto: `pip install -r requirements.txt`
4. Configura las variables de entorno según sea necesario.
5. Ejecuta las migraciones de la base de datos: `python manage.py migrate`
6. Inicia el servidor local: `python manage.py runserver`

# Permisos de Acceso para Empleados y Clientes

## Empleados (Grupo 3)
Los empleados del hotel tienen acceso a las siguientes funcionalidades:

### Gestión de Habitaciones:
- Crear, editar y eliminar habitaciones.
- Buscar habitaciones avanzadas.

### Gestión de Clientes:
- Buscar clientes.
- Crear, editar y eliminar clientes.

### Gestión de Reservas:
- Crear, editar y eliminar reservas.
- Buscar reservas avanzadas.

## Clientes (Grupo 2)
Los clientes del hotel tienen acceso a las siguientes funcionalidades:

### Consulta de Habitaciones:
- Ver la lista de habitaciones disponibles.
- Buscar habitaciones avanzadas.

### Consulta de Reservas:
- Crear, editar y eliminar reservas. (deberian ser las propias de cada usuario)
- Ver la lista de reservas realizadas.
- Buscar reservas avanzadas.




### Funcionalidades del Proyecto final

#### Inclusión de Servicios en las Reservas y Modificación del Precio Final
- **Descripción:** Los clientes pueden seleccionar servicios adicionales, como desayuno, almuerzos y cenas, al momento de realizar una reserva de habitación.
- **Implementación:** Se ha desarrollado un formulario de reserva que incluye opciones para agregar servicios adicionales. Al calcular el precio final de la reserva, se tienen en cuenta los costos de los servicios seleccionados.

#### Listado de Habitaciones Favoritas
- **Descripción:** Los usuarios pueden agregar habitaciones a su lista de favoritos para acceder fácilmente a ellas en el futuro.
- **Problemas Actuales:** La funcionalidad de agregar favoritos presenta errores que deben corregirse para garantizar un funcionamiento adecuado.

#### Listado de Eventos Filtrados por el Próximo Mes
- **Descripción:** Se muestra un listado de eventos que tendrán lugar durante el próximo mes.
- **Implementación:** Se realiza un filtrado de los eventos disponibles según su fecha, mostrando únicamente aquellos que están programados para el próximo mes.

#### Descuento del 10% en el Aniversario del Registro del Usuario
- **Descripción:** Los usuarios reciben un descuento del 10% en su reserva si es el aniversario de su registro en el sistema.
- **Implementación:** Se verifica la fecha de registro del usuario al realizar una reserva y se aplica automáticamente el descuento si corresponde.

#### Galería de Imágenes Según el Tipo de Habitación en el lado cliente
- **Descripción:** Se muestra una galería de imágenes específicas dependiendo del tipo de habitación seleccionado (pequeñas, medianas, grandes o deluxe).
- **Implementación:** Se ha implementado una lógica que determina el tipo de habitación seleccionado y carga las imágenes correspondientes en la galería.

#### Filtro para Ordenar Habitaciones por Categorías
- **Descripción:** Los usuarios pueden filtrar las habitaciones disponibles según diferentes categorías, como precio, tamaño o comodidades.
- **Implementación:** Se ha desarrollado un sistema de filtros que permite a los usuarios ordenar y visualizar las habitaciones según sus preferencias.

#### Listado de Habitaciones Reservadas del Usuario Logeado
- **Descripción:** Los usuarios pueden ver un listado de las habitaciones que han reservado anteriormente.
- **Implementación:** Se ha implementado una funcionalidad que muestra las habitaciones reservadas por el usuario logeado, permitiéndoles acceder fácilmente a esta información.

#### Añadidos Tokens de Seguridad a las Vistas para Usuarios Registrados
- **Descripción:** Se ha añadido seguridad a las vistas del sistema para garantizar que solo los usuarios registrados puedan acceder a ciertas funcionalidades.
- **Implementación:** Se han implementado tokens de seguridad en las vistas relevantes, requiriendo que los usuarios inicien sesión antes de acceder a determinadas partes del sistema.

#### Permisos Diferenciados para Empleados y Clientes
- **Descripción:** Se establecen diferentes niveles de permisos para empleados y clientes, permitiendo a los empleados editar, crear y eliminar información, mientras que los clientes solo pueden interactuar con las partes del sistema para las que tienen permiso.
- **Implementación:** Se han definido roles de usuario y se han asignado permisos específicos a cada tipo de usuario, controlando así su acceso y las acciones que pueden realizar dentro del sistema.

