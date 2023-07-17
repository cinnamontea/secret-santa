function enableSubmitBtn(downloadedKey) {
	var pubdl = document.getElementById("pubdl");
    var pridl = document.getElementById("pridl");
    var dbtn = document.getElementById("dbtn");
  
    switch (downloadedKey) {
    case "pub":
        pubdl.setAttribute("value", "1");
        if (pridl.getAttribute("value") == 1) {
            dbtn.removeAttribute("disabled");
        }
        break;
    case "pri":
        pridl.setAttribute("value", "1");
        if (pubdl.getAttribute("value") == 1) {
            dbtn.removeAttribute("disabled");
        }
        break;
    }
}


function genKeys() {
    var msgsElem = document.getElementById("key_msgs");
    msgsElem.innerHTML = "Por favor, descarga los siguientes archivos y guárdalos en un lugar seguro. Estos contienen las claves que necesitarás para participar en los eventos. El botón de registro se activará cuando descargues las claves.";

    genRSAKeyPair()
    .then((keyPair) => exportKeyPair(keyPair))
    .then((exportedKP) => {
        let {"exportedPub": pemPK, "exportedPriv": pemSK} = exportedKP;

        document.getElementById("pubkey").value = pemPK;
        var pubLink = document.getElementById("publink");
        var privLink = document.getElementById("privlink");

        genFileDownload(pubLink, "pubkey", pemPK);
        pubLink.style.display = "inline";
        pubLink.addEventListener("click", (event) => {enableSubmitBtn("pub")});

        genFileDownload(privLink, "privkey", pemSK);
        privLink.style.display = "inline";
        privLink.addEventListener("click", (event) => {enableSubmitBtn("pri")});
    })
    .catch((err) => {
        msg.style.color = "red";
        msg.innerHTML = `Ocurrió un error al generar las claves. Por favor intenta más tarde:\n${err}`;
    });
}