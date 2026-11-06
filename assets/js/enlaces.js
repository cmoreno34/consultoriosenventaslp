// Los dos destinos de todos los botones de la web, en UN sitio.
//
//  · FORMULARIO: enlace de seguimiento del CRM (medio «Web»). Cada lead entra
//    en el CRM con su comercial, su tarea y sus correos.
//  · WHATSAPP: el número de 50 Doctors SLP con el mensaje ya escrito. El CRM
//    reconoce la frase «vengo de la web» y marca el lead como venido de aquí.
var FORMULARIO = "https://ventaconsultorios-slp.web.app/kbwYiT3V";
var WHATSAPP = "https://wa.me/524444283473?text=" + encodeURIComponent(
  "Hola, vengo de la web consultoriosenventaslp.mx y quiero información de los consultorios.");

// Google Ads (CEO 2026-11-02, cuenta 209-593-1827). Quien llega de un anuncio
// trae `gclid` en la URL; se guarda para la pestaña (sessionStorage) y se pasa al
// formulario del CRM, así el lead queda unido al clic aunque cambie de página.
var GOOGLE_ADS = "AW-18551963654";
// Etiquetas de las acciones de conversión de Google Ads (Objetivos →
// Conversiones). Vacía = esa conversión aún no existe y no se manda nada.
var CONVERSIONES = {
  formulario: "yISCCP2u0bAdEIaAoo5F",  // Pedir información (web)
  cita: "",  // «Concertar visita» quitada (CEO 2026-11-02): la web no tiene ese botón
  whatsapp: "OmuxCPuv0bAdEIaAoo5F"     // WhatsApp (web)
};

var GCLID = "";
try {
  var _q = new URLSearchParams(location.search);
  GCLID = _q.get("gclid") || _q.get("gbraid") || _q.get("wbraid") || "";
  if (GCLID) sessionStorage.setItem("cv_gclid", GCLID);
  else GCLID = sessionStorage.getItem("cv_gclid") || "";
} catch (e) {}
if (GCLID) FORMULARIO += (FORMULARIO.indexOf("?") === -1 ? "?" : "&") + "gclid=" + encodeURIComponent(GCLID);

function conversion(tipo) {
  var etiqueta = CONVERSIONES[tipo];
  if (!etiqueta || typeof gtag !== "function") return;
  try { gtag("event", "conversion", { send_to: GOOGLE_ADS + "/" + etiqueta }); } catch (e) {}
}

document.querySelectorAll("[data-formulario]").forEach(function (a) {
  a.href = FORMULARIO; a.target = "_blank"; a.rel = "noopener";
  a.addEventListener("click", function () { conversion("formulario"); });
});
document.querySelectorAll("[data-whatsapp]").forEach(function (a) {
  a.href = WHATSAPP; a.target = "_blank"; a.rel = "noopener";
  a.addEventListener("click", function () { conversion("whatsapp"); });
});

// «Concertar una visita» (CEO 2026-10-11): el mismo formulario en modo CITA,
// en el que el médico elige día y franja y entra en el CRM como solicitud de
// cita para su comercial.
document.querySelectorAll("[data-cita]").forEach(function (a) {
  a.href = FORMULARIO + (FORMULARIO.indexOf("?") === -1 ? "?" : "&") + "kind=cita";
  a.target = "_blank"; a.rel = "noopener";
  a.addEventListener("click", function () { conversion("cita"); });
});

// Contador de visitas (CEO 2026-10-15: «monta el contador de visitas de la web
// dentro del CRM, por día, por página y de dónde vienen»). Cada página avisa al
// CRM al abrirse; las cifras salen en el CRM, Campañas → Análisis → Web.
//
//  · Sin cookies ni datos de la persona: solo la página, de dónde viene y si
//    es la primera página de la visita (`sessionStorage`, que se borra al
//    cerrar la pestaña).
//  · `sendBeacon` con texto plano: no frena la página y no necesita CORS.
(function () {
  var CRM = "https://fifty-doctors-crm-805505290896.us-central1.run.app/api/v1/web-publica/visita";
  if (!navigator.sendBeacon) return;
  var primera = true;
  try {
    primera = !sessionStorage.getItem("cv_visita");
    sessionStorage.setItem("cv_visita", "1");
  } catch (e) { /* modo privado: cuenta como primera */ }
  var utm = "";
  try {
    var q = new URLSearchParams(location.search);
    utm = q.get("utm_source") || "";
    // Clic en un anuncio de Google Ads: Google añade gclid (o gbraid/wbraid en
    // iPhone). Así el CRM separa anuncio de búsqueda normal (CEO 2026-10-22).
    if (q.get("gclid") || q.get("gbraid") || q.get("wbraid")) utm = "google_ads";
  } catch (e) {}
  var datos = JSON.stringify({
    p: location.pathname, r: document.referrer || "", u: utm, e: primera ? 1 : 0
  });
  try {
    navigator.sendBeacon(CRM, new Blob([datos], { type: "text/plain;charset=UTF-8" }));
  } catch (e) {}
})();

// Promoción vigente (CEO 2026-11-06). El anuncio flotante sale en todas las
// páginas salvo la de la promo; se puede cerrar (hasta cerrar la pestaña) y
// desaparece solo, con la sección destacada, al acabar la vigencia aunque nadie
// vuelva a construir la web.
(function () {
  var ahora = Date.now();
  document.querySelectorAll("[data-promo-hasta]").forEach(function (el) {
    var fin = Date.parse(el.getAttribute("data-promo-hasta"));
    if (fin && ahora >= fin) { el.remove(); return; }
    if (!el.classList.contains("promo-flotante")) return;
    var cerrada = false;
    try { cerrada = sessionStorage.getItem("cv_promo_cerrada") === el.getAttribute("data-promo-hasta"); } catch (e) {}
    if (cerrada) { el.remove(); return; }
    el.hidden = false;
    var x = el.querySelector(".promo-flotante__cerrar");
    if (x) x.addEventListener("click", function () {
      try { sessionStorage.setItem("cv_promo_cerrada", el.getAttribute("data-promo-hasta")); } catch (e) {}
      el.remove();
    });
  });
})();
