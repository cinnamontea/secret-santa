var secretKey;
var eventKey;
var gifteeId;
var gifteeCID;
var gifteeCK;
var gifterCID;
var gifterCK;


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
    var encGeeCID = document.getElementById("enc_giftee_chat_id").value;
    var encGeeCK = document.getElementById("enc_giftee_chat_key").value;
    var encGerCID = document.getElementById("enc_gifter_chat_id").value;
    var encGerCK = document.getElementById("enc_gifter_chat_key").value;

    // Elements where the decrypted info will be shown.
    var eKey = document.getElementById("ekey");
    var geeId = document.getElementById("giftee_id");
    var geeCID = document.getElementById("giftee_chat_id");
    var geeCK = document.getElementById("giftee_chat_key");
    var gerCID = document.getElementById("gifter_chat_id");
    var gerCK = document.getElementById("gifter_chat_key");
    
    // Decrypt and display the info.
    skFileElem.files[0].text()
    .then((rawKey) => importKey(rawKey, "private"))
    .then((key) => {
        secretKey = key;
        return decryptRSA_OAEP(encEKey, key)
    })
    .then((decEKey) => {
        eventKey = decEKey;
        eKey.value = decEKey;
        return decryptEventResults(decEKey, encGeeId, encGeeCID, encGeeCK, encGerCID, encGerCK)
    })
    .then((decInfo) => {
        let {"geeId": decGeeId, "geeCID": decGeeCID, "geeCK": decGeeCK, "gerCID": decGerCID, "gerCK": decGerCK} = decInfo;
        geeId.value = decGeeId;
        gifteeId = decGeeId;
        geeCID.value = decGeeCID;
        gifteeCID = decGeeCID;
        geeCK.value = decGeeCK;
        gifteeCK = decGeeCK;
        gerCID.value = decGerCID;
        gifterCID = decGerCID;
        gerCK.value = decGerCK;
        gifterCK = decGerCK;
    })
    .catch((err) => {
        decErrsElem.innerHTML = `Ocurrió un error al intentar desencriptar la información.\nVerifica que seleccionaste la clave privada correcta.\n${err}`;
    })

    resElem.style.display = "block";
}


async function decryptEventResults(ekey, encGeeId, encGeeCID, encGeeCK, encGerCID, encGerCK) {
    let pemKey = "-----BEGIN SYMMETRIC KEY-----\n" + ekey + "\n-----END SYMMETRIC KEY-----;"
    let key = await importKey(pemKey, "symmetric");
    let geeId = await decryptAESCTR(encGeeId, key);
    let geeCID = await decryptAESCTR(encGeeCID, key);
    let geeCK = await decryptAESCTR(encGeeCK, key);
    let gerCID = await decryptAESCTR(encGerCID, key);
    let gerCK = await decryptAESCTR(encGerCK, key);

    return {"geeId": geeId, "geeCID": geeCID, "geeCK": geeCK, "gerCID": gerCID, "gerCK": gerCK};
}

