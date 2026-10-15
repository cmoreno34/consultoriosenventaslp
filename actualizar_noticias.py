"""Añade a Noticias lo nuevo publicado en Instagram y Facebook.

Uso:  python actualizar_noticias.py

CEO 2026-10-15: «hazlo automáticamente cuando publiquemos en Instagram o
Facebook». Lo corre la tarea programada `.github/workflows/noticias.yml`.

El CRM es quien lee de Meta y limpia los textos (sin precios, hashtags ni
teléfonos), y quien decide cada cuántos días se consulta: Admin → Envíos
automáticos → «Noticias de la web». Aquí solo se recoge su lista:

  · solo entra lo publicado desde la última noticia de la web; lo que ya
    está en noticias.json (por su enlace) no se toca, así que una
    noticia retocada a mano se queda como está;
  · de lo nuevo se guarda la foto aquí, porque la de Instagram caduca;
  · y se vuelven a generar las páginas con construir.py.

Sin novedades no cambia ningún fichero, y la tarea no publica nada.
"""
from __future__ import annotations

import io
import json
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).parent
CRM = "https://fifty-doctors-crm-805505290896.us-central1.run.app/api/v1/web-publica/noticias"
FOTOS = RAIZ / "assets" / "img" / "noticias"
# Como las de antes: 720 px de alto como mucho (las de los reels son 406×720).
LADO_MAX = 720


def _bajar(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "consultoriosenventaslp-noticias"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def _clave(enlace: str) -> str:
    return (enlace or "").split("?", 1)[0].rstrip("/").lower()


def _guardar_foto(url: str, red: str, fecha: str) -> str:
    from PIL import Image

    img = Image.open(io.BytesIO(_bajar(url))).convert("RGB")
    img.thumbnail((LADO_MAX, LADO_MAX))
    base = f"{'fb' if red == 'facebook' else 'ig'}-{fecha}"
    nombre, n = f"{base}.webp", 2
    while (FOTOS / nombre).exists():
        nombre, n = f"{base}-{n}.webp", n + 1
    FOTOS.mkdir(parents=True, exist_ok=True)
    img.save(FOTOS / nombre, "WEBP", quality=80)
    return f"/assets/img/noticias/{nombre}"


def main() -> int:
    # Los títulos llevan emojis: que imprimirlos no rompa en una consola Windows.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    datos = json.loads(_bajar(CRM))
    if datos.get("error"):
        print("Aviso del CRM:", datos["error"])
    if not datos.get("activo"):
        print("Apagado en el CRM (Admin → Envíos automáticos): no se toca nada.")
        return 0
    ruta = RAIZ / "noticias.json"
    actuales = json.loads(ruta.read_text(encoding="utf-8"))
    vistas = {_clave(n["enlace"]) for n in actuales}
    # Solo lo publicado desde la última noticia de la web: lo anterior ya se
    # eligió a mano el 11-oct, y lo que se dejó fuera se dejó a propósito.
    desde = max((n["fecha"] for n in actuales), default="")
    nuevas = []
    for n in datos.get("noticias") or []:
        if (_clave(n.get("enlace")) in vistas or not n.get("imagen_url")
                or (n.get("fecha") or "") < desde):
            continue
        try:
            imagen = _guardar_foto(n["imagen_url"], n["red"], n["fecha"])
        except Exception as exc:  # noqa: BLE001 — sin foto no se publica esa
            print("Sin foto, se deja para la próxima:", n.get("enlace"), exc)
            continue
        nuevas.append({
            "fecha": n["fecha"], "red": n["red"], "enlace": n["enlace"],
            "titulo": n["titulo"], "texto": n.get("texto") or "", "imagen": imagen,
        })
        vistas.add(_clave(n["enlace"]))
    if not nuevas:
        print("Sin novedades.")
        return 0
    todas = sorted(actuales + nuevas, key=lambda x: x["fecha"], reverse=True)
    ruta.write_text(json.dumps(todas, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for n in nuevas:
        print("Nueva:", n["fecha"], n["red"], n["titulo"])

    import construir

    construir.construir()
    return 0


if __name__ == "__main__":
    sys.exit(main())
