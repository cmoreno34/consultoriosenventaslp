// Los dos destinos de todos los botones de la web, en UN sitio.
//
//  · FORMULARIO: enlace de seguimiento del CRM (medio «Web»). Cada lead entra
//    en el CRM con su comercial, su tarea y sus correos.
//  · WHATSAPP: el número de 50 Doctors SLP con el mensaje ya escrito. El CRM
//    reconoce la frase «vengo de la web» y marca el lead como venido de aquí.
var FORMULARIO = "https://ventaconsultorios-slp.web.app/kbwYiT3V";
var WHATSAPP = "https://wa.me/524444283473?text=" + encodeURIComponent(
  "Hola, vengo de la web consultoriosenventaslp.mx y quiero información de los consultorios.");

document.querySelectorAll("[data-formulario]").forEach(function (a) {
  a.href = FORMULARIO; a.target = "_blank"; a.rel = "noopener";
});
document.querySelectorAll("[data-whatsapp]").forEach(function (a) {
  a.href = WHATSAPP; a.target = "_blank"; a.rel = "noopener";
});

// «Concertar una visita» (CEO 2026-10-11): el mismo formulario en modo CITA,
// en el que el médico elige día y franja y entra en el CRM como solicitud de
// cita para su comercial.
document.querySelectorAll("[data-cita]").forEach(function (a) {
  a.href = FORMULARIO + (FORMULARIO.indexOf("?") === -1 ? "?" : "&") + "kind=cita";
  a.target = "_blank"; a.rel = "noopener";
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
  try { utm = new URLSearchParams(location.search).get("utm_source") || ""; } catch (e) {}
  var datos = JSON.stringify({
    p: location.pathname, r: document.referrer || "", u: utm, e: primera ? 1 : 0
  });
  try {
    navigator.sendBeacon(CRM, new Blob([datos], { type: "text/plain;charset=UTF-8" }));
  } catch (e) {}
})();
