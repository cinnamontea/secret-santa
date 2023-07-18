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
    var chatsElem = document.getElementById("event_chats");

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
    var geeName = document.getElementById("giftee_name");
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
        eKey.value = decEKey;
        return decryptEventResults(decEKey, encGeeId, encGeeCID, encGeeCK, encGerCID, encGerCK)
    })
    .then((decInfo) => {
        let {"geeId": decGeeId, "geeCID": decGeeCID, "geeCK": decGeeCK, "gerCID": decGerCID, "gerCK": decGerCK} = decInfo;
        geeId.value = decGeeId;
        geeName.value = decGeeId;
        gifteeId = decGeeId;
        geeCID.value = decGeeCID;
        gifteeCID = decGeeCID;
        geeCK.value = decGeeCK;
        gerCID.value = decGerCID;
        gifterCID = decGerCID;
        gerCK.value = decGerCK;
        return importChatKeys(decGeeCK, decGerCK);
    })
    .then((chatKeys) => {
        gifteeCK = chatKeys.geeCK;
        gifterCK = chatKeys.gerCK;
        refreshChats();
    })
    .catch((err) => {
        decErrsElem.innerHTML = `Ocurrió un error al intentar desencriptar la información.\nVerifica que seleccionaste la clave privada correcta.\n${err}`;
    })

    resElem.style.display = "block";
    chatsElem.style.display = "block";
}


async function importChatKeys(rawGeeCK, rawGerCK) {
    let pemHeader = "-----BEGIN SYMMETRIC KEY-----\n";
    let pemFooter = "\n-----END SYMMETRIC KEY-----";
    let geeCK = await importKey(pemHeader + rawGeeCK + pemFooter, "symmetric");
    let gerCK = await importKey(pemHeader + rawGerCK + pemFooter, "symmetric");
    return {geeCK: geeCK, gerCK: gerCK};
}


async function decryptEventResults(ekey, encGeeId, encGeeCID, encGeeCK, encGerCID, encGerCK) {
    let pemKey = "-----BEGIN SYMMETRIC KEY-----\n" + ekey + "\n-----END SYMMETRIC KEY-----;"
    let key = await importKey(pemKey, "symmetric");
    eventKey = key;
    let geeId = await decryptAESCTR(encGeeId, key);
    let geeCID = await decryptAESCTR(encGeeCID, key);
    let geeCK = await decryptAESCTR(encGeeCK, key);
    let gerCID = await decryptAESCTR(encGerCID, key);
    let gerCK = await decryptAESCTR(encGerCK, key);

    return {"geeId": geeId, "geeCID": geeCID, "geeCK": geeCK, "gerCID": gerCID, "gerCK": gerCK};
}


async function encryptMessage(msg, cid, key) {
    let encMsg = await encryptAESCTR(msg, key);
    let encCID = await encryptAESCTR(cid, key);
    return {encMsg: encMsg, encCID: encCID};
}


async function decryptMessage(msgObj, acceptedCID, key) {
    /*
        We need to decrypt the [chat_id] and the message itself, this could
        raise an exception if those fields were not encrypted with [key].
        We will only return a message that decrypts correctly and whose chat_id
        matches the acceptedCID.
    */
   
    try {
        let chat_id = await decryptAESCTR(msgObj.chat_id, key);
        console.log(`CID matched: ${chat_id}`);
        if (acceptedCID == chat_id) {
            let msg = await decryptAESCTR(msgObj.msg, key);
            console.log(msg);
            return msg;
        }
    } catch (error) {
        console.log(`The CID or the message couldn't be decrypted: ${error}`);
    }
}

async function decryptMessages(msgs) {
    var gifteeMsgs = [];
    var gifterMsgs = [];

    for (i=0; i<msgs.length; i++) {
        console.log(`Attempting to decrypt msg with GeeCID=${gifteeCID} and GeeCK:\nCID:${msgs[i].chat_id}\nMsg:${msgs[i].msg}`);
        let decGeeMsg = await decryptMessage(msgs[i], gifteeCID, gifteeCK);
        console.log(`Attempting to decrypt msg with GerCID=${gifterCID} and GeeCK:\nCID:${msgs[i].chat_id}\nMsg:${msgs[i].msg}`);
        let decGerMsg = await decryptMessage(msgs[i], gifterCID, gifterCK);
        
        // Only count messages that were correctly decrypted and which belong
        // to the correct chats.
        if (decGeeMsg) {
            gifteeMsgs.push(decGeeMsg);
        }
        
        if (decGerMsg) {
            gifterMsgs.push(decGerMsg);
        }
    }

    return {geeMsgs: gifteeMsgs, gerMsgs: gifterMsgs};
}


function sendMessage(chat) {
    let msgElemId = (chat == "giftee") ? "msg_giftee" : "msg_gifter";
    let chatElemId = (chat == "giftee") ? "chat_giftee" : "chat_gifter";
    let msgElem = document.getElementById(msgElemId);
    let chatElem = document.getElementById(chatElemId);
    
    let msg = msgElem.value;
    if ( msg == "") {
        return;
    }

    let cid = (chat == "giftee") ? gifteeCID : gifterCID;
    let key = (chat == "giftee") ? gifteeCK : gifterCK;

    encryptMessage(msg, cid, key)
    .then((msgObj) =>
        fetch(sendMessageURL, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({event_pk: eventPK, chat_id: msgObj.encCID, msg: msgObj.encMsg}),
    }))
    .then((response) => response.json())
    .then((thedata) => {
        console.log(thedata);
        chatElem.value = chatElem.value + msgElem.value + "\n";
        msgElem.value = "";
    })
    .catch((err) => {
        console.log(`An error occurred while sending a message: ${err}`);
    })
}


function refreshChats() {
    let geeChatElem = document.getElementById("chat_giftee");
    let gerChatElem = document.getElementById("chat_gifter");

    fetch(getMessageURL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        redirect: "follow",
    })
    .then((response) => response.json())
    .then((body) => {
        console.log(body);
        console.log(body.msgs);
        return decryptMessages(body.msgs);
    })
    .then((msgs) => {
        console.log(msgs);

        geeChatElem.value = msgs.geeMsgs.join("\n") + "\n";
        gerChatElem.value = msgs.gerMsgs.join("\n") + "\n";
    })
    .catch((err) => {
        console.log(`An error occurred in fetch get request: ${err}`);
    })
}


function testFetchGet() {

    fetch(getMessageURL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        redirect: "follow",
    })
    .then((response) => response.json())
    .then((thedata) => {
        console.log(thedata);
    })
    .catch((err) => {
        console.log(`An error occurred in fetch get request: ${err}`);
    })

}

function testFetchPost() {
    fetch(sendMessageURL, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({event_pk: eventPK, chat_id: 0, msg: "Hi"}),
    })
    .then((response) => response.json())
    .then((thedata) => {
        console.log(thedata);
    })
    .catch((err) => {
        console.log(`An error occurred in fetch get request: ${err}`);
    })
}

function printGlobals() {

    console.log(secretKey);
    console.log(eventKey);
    console.log(gifteeId);
    console.log(gifteeCID);
    console.log(gifteeCK);
    console.log(gifterCID);
    console.log(gifterCK);
}