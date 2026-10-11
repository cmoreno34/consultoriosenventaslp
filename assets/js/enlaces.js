// Los dos destinos de todos los botones de la web, en UN sitio.
//
//  · FORMULARIO: enlace de seguimiento del CRM (medio «Web»). Cada lead entra
//    en el CRM con su comercial, su tarea y sus correos.
//  · WHATSAPP: el número de 50 Doctors SLP con el mensaje ya escrito. El CRM
//    reconoce la frase «vengo de la web» y marca el lead como venido de aquí.
var FORMULARIO = "https://ventaconsultorios-slp.web.app/";
var WHATSAPP = "https://wa.me/524444283473?text=" + encodeURIComponent(
  "Hola, vengo de la web consultoriosenventaslp.mx y quiero información de los consultorios.");

document.querySelectorAll("[data-formulario]").forEach(function (a) {
  a.href = FORMULARIO; a.target = "_blank"; a.rel = "noopener";
});
document.querySelectorAll("[data-whatsapp]").forEach(function (a) {
  a.href = WHATSAPP; a.target = "_blank"; a.rel = "noopener";
});
