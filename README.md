# AD Mérida | Información

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-Educational-red.svg)

Bienvenido al repositorio central de **AD Mérida | Información**, un dashboard web automatizado y responsivo diseñado para realizar seguimiento en tiempo real de la actualidad de la **Asociación Deportiva Mérida** (Primera Federación).

Este proyecto genera estáticamente su propio motor de información, emulando la interfaz y la utilidad de aplicaciones deportivas de primer nivel de manera completamente automatizada.

---

## 🎯 Objetivo del Proyecto

El propósito de esta plataforma es ofrecer una experiencia de usuario rápida, limpia y sin interrupciones para visualizar:
*   🟢 **Resultados Históricos y en Vivo**
*   📅 **Próximos Encuentros (Calendario)**
*   🏆 **Clasificación General (Actualizada)**

Todo esto implementando técnicas modernas de orquestación, automatización y desarrollo web de vanguardia.

## ⚙️ Arquitectura y Tecnologías

El proyecto se divide estructuralmente en dos capas principales que interactúan entre sí bajo el flujo de CI/CD de GitHub:

### 1. El Cliente Visual (Frontend)
Una aplicación empaquetada en la ruta `docs/` extremadamente ligera y optimizada:
*   **HTML5 y CSS3 (Vanilla)**: Diseño *"Mobile-First"*, arquitectura basada en Grid/Flexbox y variables CSS para un tema oscuro prémium, todo sin frameworks externos pesados.
*   **JavaScript (ES6+)**: Gestión de estado con promesas (Async/Await) que obtiene toda la información consumiendo archivos estáticos `.json`.

### 2. El Motor de Recolección (Scraper)
Un robot robusto escrito en Python que dota de actualización continua al sistema:
*   **Python y Playwright**: Automatización que instancía sesiones de Chromium en modo *headless*, permitiendo inmersión en plataformas que usan carga dinámica pesada.
*   **GitHub Actions**: Trabajos programados y automatizados ejecutados cada ciertas horas en servidores virtuales. Ellos toman la data fresca, formatean y configuran los `.json`, y actualizan silenciosamente la web en vivo y en directo mediante Github Pages.

## 🚀 Despliegue Local (Para Desarrolladores)

Si se desea levantar o auditar el mecanismo de extracción de datos localmente:

```bash
# 1. Clonar el repositorio base
git clone https://github.com/tu-usuario/MeridaAD.git
cd MeridaAD

# 2. Instalar requerimientos del robot web
pip install playwright

# 3. Instalar la instancia subyacente de Chromium
playwright install --with-deps chromium

# 4. Iniciar recolección (Escribirá las respuestas en '/docs/data')
python scripts/fetch_data.py
```

> **TIP Front-end:** Para visualizar tu propia instalación, levanta un servidor de pruebas desde el directorio base (ej. `npx serve docs` o `python -m http.server -d docs`).

## ⚖️ Descargo de Responsabilidad (Disclaimer Educativo)

**⚠️ IMPORTANTE: FINALIDAD ACADÉMICA Y EDUCATIVA**

Este repositorio y todo el material técnico aquí recogido ha sido gestado y publicado de manera estricta con **fines experimentales, de aprendizaje técnico y de demostración de pruebas de concepto**.

*   El presente código o plataforma y sus derivados **NO persiguen** ánimo de lucro u operaciones comerciales algunas.
*   El diseño es una aplicación interactiva que prueba aptitudes técnicas en el análisis del DOM dinámico (*Scraping*) y despliegue automático de plataformas.
*   Todos los nombres propios de asociaciones, entidades, escudos heráldicos futbolísticos, así como la información estadística reflejada, son y pertenecen permanentemente a sus **respectivos y legales dueños / instituciones empresariales**, recayendo la autoría únicamente a ellos.

