
/*
Generates a hyperlink element to download a file named [filename] with the given [content].
*/
function genFileDownload(linktext, filename, content) {
    var downloadLink = document.createElement('a');
    downloadLink.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    downloadLink.setAttribute('download', filename);
    downloadLink.innerHTML = linktext;
  
    return downloadLink;
}

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

function genKeyDownload(exportedPub, exportedPriv) {
	var keydiv = document.getElementById("keys");
    var msg = document.createElement('p');
    msg.innerHTML = "Por favor, descarga los siguientes archivos y guárdalos en un lugar seguro. Estos contienen las claves que necesitarás para participar en los eventos. El botón de registro se activará cuando descargues las claves.";
    keydiv.appendChild(msg);
    
    var pubLink = genFileDownload("Descargar Clave Pública", "pubkey", exportedPub);
    pubLink.addEventListener("click", (event) => {enableSubmitBtn("pub")});
    keydiv.appendChild(pubLink);
    keydiv.appendChild(document.createElement('br'));
    var priLink = genFileDownload("Descargar Clave Privada", "privkey", exportedPriv);
    priLink.addEventListener("click", (event) => {enableSubmitBtn("pri")});
    keydiv.appendChild(priLink);
    keydiv.appendChild(document.createElement('br'));
}

/*
	Key Exportation
*/

function ab2str(buf) {
  return String.fromCharCode.apply(null, new Uint8Array(buf));
}

/*
Export the given key and write it into the "exported-key" space.
*/
async function exportKeypair(keypair) {
  const exportedPub = await window.crypto.subtle.exportKey("spki", keypair.publicKey);
  const exportedPubAsString = ab2str(exportedPub);
  const exportedPubAsBase64 = window.btoa(exportedPubAsString);
  const pemExportedPub = `-----BEGIN PUBLIC KEY-----\n${exportedPubAsBase64}\n-----END PUBLIC KEY-----`;
	
  const exportedPriv = await window.crypto.subtle.exportKey("pkcs8", keypair.privateKey);
  const exportedPrivAsString = ab2str(exportedPriv);
  const exportedPrivAsBase64 = window.btoa(exportedPrivAsString);
  const pemExportedPriv = `-----BEGIN PRIVATE KEY-----\n${exportedPrivAsBase64}\n-----END PRIVATE KEY-----`;
  
  return {"pub": pemExportedPub, "priv": pemExportedPriv};
}

function genKeys() {

    window.crypto.subtle.generateKey(
    {
    	name: "ECDH",
        namedCurve: "P-521"
    },
    true,
    ["deriveKey"]
    ).then((keypair) => exportKeypair(keypair))
    .then((dict) => {
      var {"pub": exportedPub, "priv": exportedPriv} = dict;
      genKeyDownload(exportedPub, exportedPriv);
    }).catch((errMsg) => {
      console.error(`An error occurred while generating keypair. Try again later: ${errMsg}`);
    })
}