"""Genera las páginas de consultoriosenventaslp.mx desde un mismo molde.

Uso:  python construir.py

Cabecera, pie, botones y metadatos salen de aquí: cambiar el menú o el pie
es cambiarlo UNA vez. Cada página es una carpeta con su index.html, para
tener direcciones limpias (/hospital/, /preventa/…) que es lo que mejor
posiciona en Google.

Los dos destinos de todos los botones están en assets/js/enlaces.js.
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).parent
DOMINIO = "https://consultoriosenventaslp.mx"
HOY = "2026-10-11"

MENU = [
    ("/", "Inicio"),
    ("/hospital/", "Hospital"),
    ("/consultorios/", "Consultorios"),
    ("/ubicacion/", "Ubicación"),
    ("/preventa/", "Preventa"),
    ("/red-50-doctors/", "La red 50 Doctors"),
    ("/noticias/", "Noticias"),
]

# CEO 2026-10-11: «pon enlaces a Instagram y Facebook en todos lados». Las
# cuentas del desarrollo de SLP (la de Instagram, comprobada; la de Facebook,
# por el id de su página, que no depende del nombre corto).
INSTAGRAM = "https://www.instagram.com/consultoriosenventa.slp/"
FACEBOOK = "https://www.facebook.com/1326223403898883"

ICONO_IG = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1.1.4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1.1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2Zm0 4.9a4.9 4.9 0 1 0 0 9.8 4.9 4.9 0 0 0 0-9.8Zm0 8.1a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4Zm5.1-9.4a1.15 1.15 0 1 0 0 2.3 1.15 1.15 0 0 0 0-2.3Z"/></svg>'
ICONO_FB = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M13.5 22v-8.2h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.6-1.6h1.7V4.1c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.4H7.4v3.2h2.8V22h3.3Z"/></svg>'


def redes(clase: str = "redes") -> str:
    return (f'<span class="{clase}">'
            f'<a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram de 50 Doctors SLP">{ICONO_IG}<span>Instagram</span></a>'
            f'<a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook de 50 Doctors SLP">{ICONO_FB}<span>Facebook</span></a>'
            '</span>')

DIRECCION = "Av. Paseo de los Horizontes 500, San Luis Potosí"

# CEO 2026-10-11: «tenemos que poner la oficina y dónde está el hospital, que
# es más adelante; que quede muy claro en el mapa». Son DOS sitios:
#  · el TERRENO del hospital (número oficial 500, Fracc. Lomas del Lago, según
#    el contrato de promesa), donde se construye la torre;
#  · la OFICINA de ventas, en el 418, planta baja del edificio de Habi.
# Los mapas son de Google y buscan el sitio por su dirección o por su nombre en
# Google (el del hospital, «Hospital 50 Doctors», lo da por bueno el CEO).
HOSPITAL = {
    "nombre": "Hospital 50 Doctors (en preventa)",
    "direccion": "Av. Paseo de los Horizontes 500, Fracc. Lomas del Lago, San Luis Potosí",
    "lat": None, "lng": None,
    # El punto de Google «Hospital 50 Doctors», que el CEO da por bueno.
    "google": "Hospital 50 Doctors, Paseo de los Horizontes, San Luis Potosí",
}
OFICINA = {
    "nombre": "Oficina de ventas",
    "direccion": "Paseo de los Horizontes 418 (planta baja, edificio Habi), Horizontes, 78183 San Luis Potosí",
    # La dirección tal como la da su ficha de Google (la del edificio de Habi).
    # El código 5X93+8P, convertido a mano, caía en otra zona: no se usa.
    "lat": None, "lng": None,
    "google": "5X93+8P San Luis Potosí, S.L.P.",
}


def _maps(lugar: dict) -> str:
    """Enlace «Cómo llegar» de Google Maps."""
    from urllib.parse import quote
    return "https://www.google.com/maps/dir/?api=1&destination=" + quote(lugar["google"])


def _embed(lugar: dict) -> str:
    """Mapa de Google insertable (sin clave): UNA marca por mapa."""
    from urllib.parse import quote
    return f"https://www.google.com/maps?q={quote(lugar['google'])}&z=16&output=embed"


def _ruta() -> str:
    """De la oficina al hospital: enseña que está más adelante en la avenida."""
    from urllib.parse import quote
    return ("https://www.google.com/maps/dir/?api=1&origin=" + quote(OFICINA["google"])
            + "&destination=" + quote(HOSPITAL["google"]))


def cabecera(ruta: str) -> str:
    enlaces = "\n".join(
        f'      <a href="{h}"{" aria-current=\"page\"" if h == ruta else ""}>{t}</a>'
        for h, t in MENU[1:]
    )
    return f"""<div class="barra-dominio">
  <div class="contenedor barra-dominio__fila">
    <a href="/" class="barra-dominio__nombre">consultoriosenventa<strong>SLP</strong>.mx</a>
    <span class="barra-dominio__lema">Consultorios médicos en venta · Torre con hospital · San Luis Potosí</span>
    {redes("redes redes--barra")}
  </div>
</div>
<header class="cabecera">
  <div class="contenedor cabecera__fila">
    <a href="/" class="marca" aria-label="50 Doctors SLP, inicio">
      <img src="/assets/img/logo.png" alt="50 Doctors Hospital San Luis Potosí" width="190" height="53">
    </a>
    <nav class="menu" aria-label="Secciones">
{enlaces}
    </nav>
    <a class="boton boton--pequeno" data-formulario href="/#contacto">Pedir información</a>
  </div>
  <nav class="menu-movil" aria-label="Secciones">
{enlaces}
  </nav>
</header>"""


PIE = f"""<section class="seccion seccion--gris" id="contacto">
  <div class="contenedor contacto">
    <h2>Pide información de los consultorios</h2>
    <p>Déjanos tus datos y un asesor te contacta por WhatsApp con la disponibilidad, los planos y las condiciones de la preventa.</p>
    <div class="botones centrar">
      <a class="boton" data-formulario href="/#contacto">Pedir información</a>
      <a class="boton boton--borde-oscuro" data-whatsapp href="/#contacto">Escribir por WhatsApp</a>
    </div>
    <p class="siguenos">Síguenos y entérate de los avances de la obra: {redes("redes redes--grande")}</p>
  </div>
</section>

<footer class="pie">
  <div class="contenedor pie__fila">
    <div>
      <img src="/assets/img/logo.png" alt="50 Doctors Hospital San Luis Potosí" width="160" height="45" class="pie__logo">
      <p>Hospital (en preventa): {HOSPITAL["direccion"]}.<br>Oficina de ventas: {OFICINA["direccion"]}.</p>
      <p>{redes("redes redes--pie")}</p>
      <nav class="pie__menu" aria-label="Secciones">
        {" · ".join(f'<a href="{h}">{t}</a>' for h, t in MENU)}
      </nav>
    </div>
    <div class="pie__legal">
      <p>Comercializa <a href="https://www.blueinsights2011.com/" target="_blank" rel="noopener">Blue Insights 2011 SL</a>, empresa comercializadora y agencia de marketing de los hospitales 50&nbsp;Doctors en San Luis Potosí. La marca 50&nbsp;FIFTY&nbsp;DOCTORS® está registrada en el IMPI a nombre de su titular (registro n.º 2196212); sitio oficial: <a href="https://www.50doctors.mx" target="_blank" rel="noopener">50doctors.mx</a>.</p>
      <p>Imágenes representativas. Disponibilidad y condiciones sujetas a cambios sin previo aviso. <a href="https://fifty-doctors-crm-805505290896.us-central1.run.app/privacidad" target="_blank" rel="noopener">Aviso de privacidad</a>.</p>
    </div>
  </div>
</footer>

<a class="flotante" data-whatsapp href="/#contacto" aria-label="Escribir por WhatsApp">
  <svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3Zm0 23.6c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6Zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4s-1.2 1.1-1.2 2.8 1.2 3.3 1.4 3.5 2.4 3.7 5.9 5.2c2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5s.3-1.4.2-1.5-.3-.2-.6-.3Z"/></svg>
</a>
<script src="/assets/js/enlaces.js?v=4"></script>"""

LD_TORRE = {
    "@context": "https://schema.org",
    "@type": "Place",
    "name": "Torre médica 50 Doctors Hospital San Luis Potosí",
    "description": "Torre médica de 12 niveles con hospital propio, 192 consultorios médicos, 14 locales comerciales y 350 cajones de estacionamiento.",
    "url": DOMINIO + "/",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Av. Paseo de los Horizontes 500",
        "addressLocality": "San Luis Potosí",
        "addressRegion": "S.L.P.",
        "addressCountry": "MX",
    },
}


def pagina(ruta: str, titulo: str, descripcion: str, cuerpo: str, ld: dict | None = None) -> str:
    url = DOMINIO + ruta
    ld_txt = (
        f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
        if ld else ""
    )
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#0039ea">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<meta property="og:site_name" content="50 Doctors SLP">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descripcion}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMINIO}/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css?v=5">{ld_txt}
</head>
<body>
{cabecera(ruta)}
<main>
{cuerpo}
</main>
{PIE}
</body>
</html>
"""


def titular(etiqueta: str, h1: str, sub: str, foto: str, alt: str, w: int, h: int) -> str:
    """La cabecera de foto de cada página interior."""
    return f"""<section class="portada portada--interior">
  <img class="portada__foto" src="/assets/img/{foto}" alt="{alt}" width="{w}" height="{h}" fetchpriority="high">
  <div class="portada__velo"></div>
  <div class="contenedor portada__texto">
    <p class="etiqueta">{etiqueta}</p>
    <h1>{h1}</h1>
    <p class="portada__sub">{sub}</p>
    <div class="botones">
      <a class="boton" data-formulario href="/#contacto">Pedir información</a>
      <a class="boton boton--claro" data-whatsapp href="/#contacto">WhatsApp</a>
    </div>
  </div>
</section>"""


CIFRAS = """<section class="cifras" aria-label="La torre en cifras">
  <div class="contenedor cifras__fila">
    <div><strong>192</strong><span>consultorios médicos</span></div>
    <div><strong>Hospital</strong><span>en el mismo edificio</span></div>
    <div><strong>24 h</strong><span>urgencias</span></div>
    <div><strong>12</strong><span>niveles</span></div>
    <div><strong>350</strong><span>cajones de estacionamiento</span></div>
    <div><strong>14</strong><span>locales comerciales</span></div>
  </div>
</section>"""


def tarjeta_enlace(href: str, titulo: str, texto: str, foto: str, alt: str) -> str:
    return f"""<a class="tarjeta tarjeta--enlace" href="{href}">
      <img src="/assets/img/{foto}" alt="{alt}" loading="lazy">
      <div>
        <h3>{titulo}</h3>
        <p>{texto}</p>
        <span class="tarjeta__mas">Ver más →</span>
      </div>
    </a>"""


# ── Páginas ──────────────────────────────────────────────────────────────

PAGINAS: dict[str, tuple[str, str, str, dict | None]] = {}

PAGINAS["/"] = (
    "Consultorios médicos en venta en San Luis Potosí · Torre con hospital · 50 Doctors SLP",
    "Consultorios médicos en venta en San Luis Potosí, en una torre con hospital propio: quirófanos, urgencias 24 h, terapia intensiva e imagenología. Av. Paseo de los Horizontes 500. Preventa.",
    f"""<section class="portada">
  <img class="portada__foto" src="/assets/img/torre-slp.webp" alt="Render de la torre médica 50 Doctors Hospital en San Luis Potosí" width="1600" height="1313" fetchpriority="high">
  <div class="portada__velo"></div>
  <div class="contenedor portada__texto">
    <p class="etiqueta">Preventa · San Luis Potosí</p>
    <h1>Consultorios médicos en venta en San Luis Potosí, en una torre con hospital propio</h1>
    <p class="portada__sub">Quirófanos, urgencias 24 h y terapia intensiva en tu mismo edificio. {DIRECCION}. La construcción está por comenzar: es el momento de elegir tu ubicación.</p>
    <div class="botones">
      <a class="boton" data-formulario href="/#contacto">Pedir información</a>
      <a class="boton boton--claro" data-whatsapp href="/#contacto">Escribir por WhatsApp</a>
    </div>
  </div>
</section>
{CIFRAS}
<section class="seccion">
  <div class="contenedor">
    <p class="etiqueta centrado">Conoce el proyecto</p>
    <h2 class="centrado">Todo lo que necesita tu consulta, en un solo edificio</h2>
    <div class="tarjetas tarjetas--enlace">
    {tarjeta_enlace("/hospital/", "El hospital", "Quirófanos, urgencias 24 h, UCI, laboratorio e imagenología en la misma torre.", "quirofano.webp", "Quirófano 50 Doctors")}
    {tarjeta_enlace("/consultorios/", "Los consultorios", "De 22 a 32 m², sin divisiones para adaptarlos a tu especialidad.", "consultorio.webp", "Consultorio médico")}
    {tarjeta_enlace("/ubicacion/", "La ubicación", "Av. Paseo de los Horizontes 500, zona Horizontes, con 350 cajones.", "torre-slp.webp", "Torre 50 Doctors SLP")}
    {tarjeta_enlace("/preventa/", "La preventa", "La obra está por comenzar: elige la mejor ubicación en la torre.", "sala-espera.webp", "Sala de espera")}
    </div>
  </div>
</section>
<section class="seccion seccion--gris">
  <div class="contenedor">
    <p class="etiqueta centrado">Por qué un consultorio propio</p>
    <h2 class="centrado">Deja de pagar renta y construye patrimonio</h2>
    <div class="tarjetas">
      <article class="tarjeta"><h3>Pacientes del propio hospital</h3><p>Un hospital en el edificio trae flujo de pacientes, estudios e interconsultas a la puerta de tu consultorio.</p></article>
      <article class="tarjeta"><h3>Un activo que es tuyo</h3><p>Lo que hoy pagas de renta se convierte en patrimonio: un inmueble especializado en una zona de crecimiento.</p></article>
      <article class="tarjeta"><h3>También como inversión</h3><p>Los médicos son inquilinos estables y de largo plazo. Puedes usarlo tú o rentarlo a otro especialista.</p></article>
    </div>
  </div>
</section>""",
    {**LD_TORRE, "@context": "https://schema.org"},
)

PAGINAS["/hospital/"] = (
    "Consultorio junto a hospital en San Luis Potosí · Quirófanos y urgencias 24 h · 50 Doctors",
    "Consultorios en una torre con hospital 50 Doctors en San Luis Potosí: 3 quirófanos, 30 habitaciones, terapia intensiva, urgencias 24 h, hemodinamia, laboratorio e imagenología.",
    titular("El hospital", "Tu consulta, junto a un hospital completo",
            "Tus pacientes se operan, se estudian y se atienden de urgencia sin salir del edificio. Tú pasas de la consulta al quirófano en un elevador.",
            "quirofano.webp", "Quirófano de un hospital 50 Doctors", 1600, 1158)
    + """
<section class="seccion">
  <div class="contenedor dos-col">
    <div>
      <h2>Lo que tiene el hospital</h2>
      <p>La torre incluye un hospital 50 Doctors en sus primeros niveles, pensado para dar servicio a los médicos del edificio y a sus pacientes.</p>
      <ul class="lista">
        <li>3 quirófanos</li>
        <li>30 habitaciones</li>
        <li>Terapia intensiva (UCI)</li>
        <li>Urgencias 24 horas y sala de choque</li>
        <li>Sala de hemodinamia</li>
        <li>Laboratorio e imagenología</li>
      </ul>
    </div>
    <div class="galeria-2">
      <img src="/assets/img/hospital-pasillo.webp" alt="Pasillo de hospital 50 Doctors" width="1600" height="1067" loading="lazy">
      <img src="/assets/img/quirofano.webp" alt="Quirófano 50 Doctors" width="1600" height="1158" loading="lazy">
    </div>
  </div>
</section>
<section class="seccion seccion--gris">
  <div class="contenedor">
    <h2 class="centrado">Qué significa para tu práctica</h2>
    <div class="tarjetas">
      <article class="tarjeta"><h3>Cirugía sin trasladarte</h3><p>Operas en el mismo edificio donde pasas consulta: menos tiempo perdido y más control sobre tus pacientes.</p></article>
      <article class="tarjeta"><h3>Estudios al momento</h3><p>Laboratorio e imagenología a un piso de distancia: tus pacientes resuelven todo en una visita.</p></article>
      <article class="tarjeta"><h3>Respaldo 24 horas</h3><p>Urgencias y terapia intensiva disponibles día y noche, para ti y para tus pacientes.</p></article>
    </div>
  </div>
</section>""",
    None,
)

PAGINAS["/consultorios/"] = (
    "Consultorios de 22 a 32 m² en venta en San Luis Potosí · 50 Doctors SLP",
    "Consultorios médicos de 22 a 32 m² en San Luis Potosí, entregados sin divisiones para adaptarlos a tu especialidad. Acabados de calidad, seguridad 24/7, elevadores y estacionamiento.",
    titular("Los consultorios", "Un consultorio propio, a la medida de tu especialidad",
            "De 22 a 32 m² en los niveles 4 a 11, entregados sin divisiones para que los distribuyas como necesites.",
            "consultorio-real.webp", "Consultorio médico 50 Doctors", 1200, 1600)
    + """
<section class="seccion">
  <div class="contenedor dos-col">
    <div>
      <h2>Acabados de calidad</h2>
      <ul class="lista lista--2col">
        <li>Piso de porcelanato</li>
        <li>Puerta principal de cristal templado</li>
        <li>Iluminación LED en plafones</li>
        <li>Tablaroca con aislante acústico y térmico</li>
        <li>Instalación eléctrica, hidráulica y sanitaria</li>
        <li>Acometida de telefonía</li>
        <li>Ventanas y cancelería de aluminio</li>
        <li>Pintura vinílica en muros y plafones</li>
      </ul>
      <p class="nota">Los consultorios se entregan sin divisiones ni mobiliario. Te proponemos varias distribuciones según tu especialidad.</p>
    </div>
    <div class="galeria-mosaico">
      <img src="/assets/img/sala-espera.webp" alt="Sala de espera en una torre 50 Doctors" width="1600" height="1040" loading="lazy">
      <img src="/assets/img/consultorio.webp" alt="Consultorio amueblado, ejemplo de distribución" width="914" height="1600" loading="lazy">
      <img src="/assets/img/pasillo-consultorios.webp" alt="Pasillo de consultorios" width="1082" height="1600" loading="lazy">
    </div>
  </div>
</section>
<section class="seccion seccion--gris">
  <div class="contenedor">
    <h2 class="centrado">Servicios de la torre</h2>
    <ul class="lista lista--3col">
      <li>Seguridad privada 24/7</li>
      <li>Sistema de videovigilancia</li>
      <li>Elevadores</li>
      <li>Estacionamiento para pacientes</li>
      <li>Mantenimiento de áreas comunes</li>
      <li>Limpieza de áreas comunes</li>
      <li>Seguro de la torre</li>
      <li>Administrador del edificio</li>
      <li>Sistema contra incendios</li>
      <li>Área comercial</li>
    </ul>
  </div>
</section>""",
    None,
)

PAGINAS["/ubicacion/"] = (
    "Ubicación del hospital y oficina de ventas · Consultorios 50 Doctors San Luis Potosí",
    "El hospital 50 Doctors se construye en Av. Paseo de los Horizontes 500 (Lomas del Lago), San Luis Potosí. La oficina de ventas está en Paseo de los Horizontes 418.",
    titular("Ubicación", "Dónde está el hospital y dónde te atendemos",
            "Son dos puntos de la misma avenida: el terreno donde se construye el hospital y, un poco antes, nuestra oficina de ventas.",
            "torre-slp.webp", "Torre 50 Doctors en Av. Paseo de los Horizontes", 1600, 1313)
    + f"""
<section class="seccion">
  <div class="contenedor">
    <p class="centrado estrecho">El hospital y la oficina están en la <strong>misma avenida</strong>: la oficina queda antes y el terreno del hospital, más adelante.</p>
    <p class="centrado"><a class="boton boton--borde-oscuro" href="{_ruta()}" target="_blank" rel="noopener">Ver el camino de la oficina al hospital</a></p>
    <div class="lugares">
      <article class="lugar lugar--hospital">
        <div class="mapa"><iframe title="Mapa del hospital 50 Doctors" src="{_embed(HOSPITAL)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
        <p class="etiqueta">🏥 Aquí se construye el hospital</p>
        <h2>{HOSPITAL["nombre"]}</h2>
        <p>{HOSPITAL["direccion"]}.</p>
        <p class="nota">Es el terreno de la torre: todavía no hay oficina en la obra.</p>
        <a class="boton boton--borde-oscuro" href="{_maps(HOSPITAL)}" target="_blank" rel="noopener">Cómo llegar al terreno</a>
      </article>
      <article class="lugar lugar--oficina">
        <div class="mapa"><iframe title="Mapa de la oficina de ventas" src="{_embed(OFICINA)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
        <p class="etiqueta">📍 Aquí te atendemos</p>
        <h2>{OFICINA["nombre"]}</h2>
        <p>{OFICINA["direccion"]}.</p>
        <p class="nota">Te enseñamos planos, disponibilidad y condiciones. Pide información y te contactamos.</p>
        <div class="botones">
          <a class="boton" data-formulario href="/#contacto">Pedir información</a>
          <a class="boton boton--borde-oscuro" href="{_maps(OFICINA)}" target="_blank" rel="noopener">Cómo llegar a la oficina</a>
        </div>
      </article>
    </div>
  </div>
</section>""",
    LD_TORRE,
)

PAGINAS["/preventa/"] = (
    "Preventa de consultorios médicos en San Luis Potosí · 50 Doctors SLP",
    "Preventa de consultorios en la torre médica 50 Doctors de San Luis Potosí. La construcción está por comenzar: elige la mejor ubicación y aparta con facilidades de pago.",
    titular("Preventa", "La construcción está por comenzar",
            "Entrar ahora te permite elegir la mejor ubicación dentro de la torre y apartar tu consultorio en etapa de preventa.",
            "torre-slp.webp", "Torre 50 Doctors SLP en preventa", 1600, 1313)
    + """
<section class="seccion">
  <div class="contenedor">
    <h2 class="centrado">Por qué entrar en preventa</h2>
    <div class="tarjetas">
      <article class="tarjeta"><h3>Eliges ubicación</h3><p>Al principio hay más consultorios donde elegir: piso, orientación, vistas y cercanía a elevadores.</p></article>
      <article class="tarjeta"><h3>Apartas y congelas</h3><p>Al apartar se respetan la ubicación y las condiciones que pactas con tu asesor.</p></article>
      <article class="tarjeta"><h3>Facilidades de pago</h3><p>Planes de pago durante la obra. Tu asesor te explica las opciones disponibles.</p></article>
    </div>
  </div>
</section>
<section class="seccion seccion--gris">
  <div class="contenedor estrecho">
    <h2 class="centrado">Cómo apartar tu consultorio</h2>
    <ol class="pasos">
      <li><strong>Pide información.</strong> Te enviamos disponibilidad, planos y condiciones.</li>
      <li><strong>Elige tu consultorio.</strong> Te ayudamos a escoger el que mejor encaja con tu especialidad.</li>
      <li><strong>Aparta.</strong> Firmas con tu asesor y tu consultorio queda reservado.</li>
    </ol>
  </div>
</section>""",
    None,
)

PAGINAS["/red-50-doctors/"] = (
    "50 Doctors: red de hospitales y torres médicas en México · Consultorios en San Luis Potosí",
    "50 Doctors tiene más de 2,000 consultorios construidos y hospitales en operación en Puebla, La Paz, Villahermosa, Tampico, León, Boca del Río, Metepec, Torreón, Oaxaca y la CDMX.",
    titular("La red 50 Doctors", "Miles de médicos ya confían en 50 Doctors",
            "Más de 2,000 consultorios construidos y hospitales en operación en todo México. San Luis Potosí es el siguiente.",
            "red-puebla.webp", "Torres Médicas 50 Doctors en operación", 929, 1238)
    + """
<section class="seccion">
  <div class="contenedor">
    <h2 class="centrado">Hospitales y torres médicas en operación</h2>
    <p class="centrado estrecho">Puebla, La Paz, Villahermosa, Tampico, León, Boca del Río, Metepec, Torreón, Oaxaca y la Ciudad de México, con nuevos hospitales en desarrollo en todo el país.</p>
    <div class="red">
      <img src="/assets/img/red-puebla.webp" alt="Torres Médicas 50 Doctors" loading="lazy">
      <img src="/assets/img/red-torre-2.webp" alt="Torre médica 50 Doctors" loading="lazy">
      <img src="/assets/img/red-torre-3.webp" alt="Hospital 50 Doctors" loading="lazy">
      <img src="/assets/img/red-torre-4.webp" alt="Torre médica 50 Doctors" loading="lazy">
    </div>
    <p class="centrado nota">Más información de la red en el sitio oficial: <a href="https://www.50doctors.mx" target="_blank" rel="noopener">50doctors.mx</a>.</p>
  </div>
</section>""",
    None,
)


def _noticias() -> str:
    """Tarjetas de lo publicado en Instagram (noticias.json).

    Las saca del CRM (`meta_publicaciones`) un script aparte: texto sin
    hashtags ni teléfonos y la miniatura guardada aquí, porque la de Instagram
    caduca. Sin precios: se revisó al sacarlas."""
    import html
    from datetime import date
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    items = json.loads((RAIZ / "noticias.json").read_text(encoding="utf-8"))
    tarjetas = []
    for n in items:
        d = date.fromisoformat(n["fecha"])
        titulo, texto = n["titulo"], n["texto"]
        # «¡Atención, doctores…!» encabeza casi todas: como titular no dice
        # nada, así que se usa la primera frase del texto.
        if titulo.lower().startswith("¡atención") and texto:
            import re
            partes = re.split(r"(?<=[.!?…])\s+", texto, maxsplit=1)
            titulo, texto = partes[0], (partes[1] if len(partes) > 1 else "")
        tarjetas.append(f"""<article class="noticia">
      <a href="{n['enlace']}" target="_blank" rel="noopener" class="noticia__foto">
        <img src="{n['imagen']}" alt="" loading="lazy">
      </a>
      <div class="noticia__texto">
        <p class="noticia__fecha">{d.day} de {meses[d.month - 1]} de {d.year}</p>
        <h3>{html.escape(titulo)}</h3>
        <p>{html.escape(texto)}</p>
        <a class="enlace" href="{n['enlace']}" target="_blank" rel="noopener">Ver en Instagram →</a>
      </div>
    </article>""")
    return "\n    ".join(tarjetas)


PAGINAS["/noticias/"] = (
    "Noticias del hospital 50 Doctors San Luis Potosí · Avances y novedades",
    "Novedades del nuevo hospital 50 Doctors en San Luis Potosí: avances del proyecto, los consultorios en venta y la preventa.",
    titular("Noticias", "Lo último del hospital 50 Doctors San Luis Potosí",
            "Avances del proyecto, los consultorios y la preventa, tal como los contamos en nuestras redes.",
            "torre-slp.webp", "Torre 50 Doctors SLP", 1600, 1313)
    + f"""
<section class="seccion">
  <div class="contenedor">
    <div class="noticias">
    {_noticias()}
    </div>
    <p class="centrado siguenos">Todas las novedades, en nuestras redes: {redes("redes redes--grande")}</p>
  </div>
</section>""",
    None,
)


def construir() -> None:
    for ruta, (titulo, desc, cuerpo, ld) in PAGINAS.items():
        destino = RAIZ / ruta.strip("/") / "index.html" if ruta != "/" else RAIZ / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina(ruta, titulo, desc, cuerpo, ld), encoding="utf-8")
        print("ok", ruta)
    urls = "\n".join(
        f"  <url><loc>{DOMINIO}{r}</loc><lastmod>{HOY}</lastmod>"
        f"<priority>{'1.0' if r == '/' else '0.8'}</priority></url>"
        for r in PAGINAS
    )
    (RAIZ / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n",
        encoding="utf-8",
    )
    print("ok sitemap.xml")


if __name__ == "__main__":
    construir()
