function displayEventResults() {
    var skFileElem = document.getElementById("skey");
    var decErrsElem = document.getElementById("dec_errors");
    
    if (skFileElem.files.length == 0) {
        decErrsElem.innerHTML = "Por favor, selecciona el archivo con tu clave privada para desencriptar la información.";
        return;
    } 

    decErrsElem.innerHTML = "";
    var resElem = document.getElementById("eventres");

    // Encrypted event info.
    var encEKey = document.getElementById("enc_event_key").value;
    var encGeeId = document.getElementById("enc_giftee_id").value;
    var encGeePK = document.getElementById("enc_giftee_pk").value;
    var encGerPK = document.getElementById("enc_gifter_pk").value;

    // Elements where the decrypted info will be shown.
    var eKey = document.getElementById("ekey");
    var geeId = document.getElementById("giftee_id");
    var geePK = document.getElementById("giftee_pk");
    var gerPK = document.getElementById("gifter_pk");
    
    // Decrypt and display the info.
    skFileElem.files[0].text()
    .then((rawKey) => importKey(rawKey, "private"))
    .then((key) => decryptRSA_OAEP(encEKey, key))
    .then((decEKey) => {
        eKey.value = decEKey;
        return decryptEventResults(decEKey, encGeeId, encGeePK, encGerPK)
    })
    .then((decInfo) => {
        let {"geeId": decGeeId, "geePK": decGeePK, "gerPK": decGerPK} = decInfo;
        geeId.value = decGeeId;
        geePK.value = decGeePK;
        gerPK.value = decGerPK;
    })
    .catch((err) => {
        decErrsElem.innerHTML = `Ocurrió un error al intentar desencriptar la información.\nVerifica que seleccionaste la clave privada correcta.\n${err}`;
    })

    resElem.style.display = "block";
}


async function decryptEventResults(ekey, encGeeId, encGeePK, encGerPK) {
    let pemKey = "-----BEGIN SYMMETRIC KEY-----\n" + ekey + "\n-----END SYMMETRIC KEY-----;"
    let key = await importKey(pemKey, "symmetric");
    let geeId = await decryptAESCTR(encGeeId, key);
    let geePK = await decryptAESCTR(encGeePK, key);
    let gerPK = await decryptAESCTR(encGerPK, key);

    return {"geeId": geeId, "geePK": geePK, "gerPK": gerPK};
}

