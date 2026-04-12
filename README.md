# AD Mérida Dashboard 🏟️

Página estática premium para seguir la actualidad del AD Mérida (Primera Federación), automatizada con GitHub Actions y API-Football v3.

## ✨ Características
- **Sincronización Automática:** Los datos se actualizan cada 6 horas mediante Python.
- **Resultados y Próximos:** Estados de los últimos 5 y próximos 5 partidos con código de colores.
- **Clasificación en Tiempo Real:** Tabla completa destacando zonas de playoff y descenso.
- **Plantilla Actualizada:** Lista de jugadores por posición con dorsales y edades.
- **Diseño Premium:** Estética oscura con colores oficiales (Grana #B22222 y Oro #D4AF37).

## 🚀 Configuración Paso a Paso

### 1. Preparar el Repositorio
Si has clonado o hecho fork de este repositorio, asegúrate de tener la estructura de carpetas `docs/`, `scripts/` y `.github/`.

### 2. Configurar el API Key (Secreto)
Para obtener datos reales, necesitas una clave de [API-Football](https://www.api-football.com/) (RapidAPI o API-Sports).
1. Ve a **Settings > Secrets and variables > Actions** en tu repositorio de GitHub.
2. Haz clic en **New repository secret**.
3. Nombre: `API_FOOTBALL_KEY`
4. Valor: Tu clave de API.
   *Nota: Si no configuras el secreto, el sitio funcionará con datos de ejemplo (Mock Data) realistas.*

### 3. Activar GitHub Pages
1. Ve a **Settings > Pages**.
2. En **Build and deployment > Source**, selecciona `GitHub Actions`.
   *(Esto permite que el workflow de actualización despliegue directamente el sitio).*

### 4. Lanzamiento Inicial
El sitio se desplegará automáticamente en cada `push`. Para forzar la primera carga de datos:
1. Ve a la pestaña **Actions**.
2. Selecciona el workflow `Update Data and Deploy`.
3. Haz clic en **Run workflow**.

## 🛠️ Tecnologías
- **Frontend:** HTML5, CSS3 (Vanilla), JavaScript (ES6+).
- **Backend:** Python 3 + `requests` (Scraper).
- **Automatización:** GitHub Actions (CI/CD + Cron).
- **Fuentes:** Bebas Neue & Barlow (Google Fonts).

---
*Desarrollado para la afición del AD Mérida. ¡Vamos Romano!*
