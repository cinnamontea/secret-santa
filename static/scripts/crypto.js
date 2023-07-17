/*
    In this script, we provide all the cryptographic materials to implement the parts of the
    security protocol that run on the client-side.
    We decided to use the Web Crypto API, to rely on browser implementation rather than JS libraries.
*/


/* ========================================
            DEFINITIONS & UTILS
   ======================================== */


/*
    A dictionary to specify the arguments for key import/export.
*/
const keyFormats = {
    "public": {
        format: "spki",
        alg: {
            name: "RSA-OAEP",
            hash: "SHA-256"
        },
        extractable: "true",
        uses: ["encrypt"]
    },
    "private": {
        format: "pkcs8",
        alg: {
            name: "RSA-OAEP",
            hash: "SHA-256"
        },
        extractable: "true",
        uses: ["decrypt"]
    },
    "symmetric": {
        format: "raw",
        alg: "AES-CTR",
        extractable: "true",
        uses: ["encrypt", "decrypt"]
    },
};


// ArrayBuffer to Base64 string.
// https://stackoverflow.com/a/11562550/9014097
function ab2b64(arrayBuffer) {
    return btoa(String.fromCharCode.apply(null, new Uint8Array(arrayBuffer)));
}


// Base64 string to ArrayBuffer.
// https://stackoverflow.com/a/41106346 
function b642ab(base64string) {
    return Uint8Array.from(atob(base64string), c => c.charCodeAt(0));
}


// UTF-8 text encoder.
function encodeMessage(msg) {
    let encoder = new TextEncoder();
    return encoder.encode(msg);
}


// Given an <a> Element, sets attributes to turn it into a download link for a file.
function genFileDownload(linkElem, filename, content) {
    linkElem.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    linkElem.setAttribute('download', filename);
}



/* ========================================
            KEY IMPORT & EXPORT
   ======================================== */


// Export a 'public', 'private' or 'symmetric' key in PEM format.
async function exportKey(key, type) {
    if (!Object.keys(keyFormats).includes(type)) {
        const validChoices = "\'" + Object.keys(keyFormats).join("\', \'") + "\'";
        throw new Error(`ExportKeyError: Invalid key type \'${type}\'. Expected one of these: ${validChoices}`);
    }
  
    const pemHeader = `-----BEGIN ${type.toUpperCase()} KEY-----\n`;
    const pemFooter = `\n-----END ${type.toUpperCase()} KEY-----`;
  
    const exported = await window.crypto.subtle.exportKey(keyFormats[type].format, key);
    const exportedAsBase64 = ab2b64(exported);
    const pemExported = pemHeader + exportedAsBase64 + pemFooter;
    console.log(pemExported);
  
    return pemExported;
}


async function exportKeyPair(keyPair) {
    const pemExportedPriv = await exportKey(keyPair.privateKey, "private");
    const pemExportedPub = await exportKey(keyPair.publicKey, "public");
  
    return {
      "exportedPub": pemExportedPub,
      "exportedPriv": pemExportedPriv
    };
}


// Import a key in PEM format.
async function importKey(rawKey, type) {
    if (!Object.keys(keyFormats).includes(type)) {
      const validChoices = "\'" + Object.keys(keyFormats).join("\', \'") + "\'";
      throw new Error(`ImportKeyError: Invalid key type \'${type}\'. Expected one of these: ${validChoices}`);
    }
  
    const pemHeader = `-----BEGIN ${type.toUpperCase()} KEY-----\n`;
    const pemFooter = `\n-----END ${type.toUpperCase()} KEY-----`;
    const keyContents = rawKey.substring(pemHeader.length, rawKey.length - pemFooter.length);
  
    const binArrContent = b642ab(keyContents);
  
    const keyFmt = keyFormats[type];
  
    return window.crypto.subtle.importKey(
      keyFmt.format,
      binArrContent,
      keyFmt.alg, keyFmt.extractable, keyFmt.uses);
}



/* ================================================================================
        RSA-OAEP
        Keypair generation, encryption and decryption.
        We use a modulus of 4096 bits and 65537 as the public exponent.
        OAEP uses SHA256 as the hash/digest function.
   ================================================================================ */


// Keypair generation
// () -> Promise(CryptoKeyPair)
async function genRSAKeyPair() {
    let keyPair = await window.crypto.subtle.generateKey({
            name: "RSA-OAEP",
            modulusLength: 4096,
            publicExponent: new Uint8Array([1, 0, 1]), // (0000 00001 0000 0000 0000 0001) = 65537
            hash: "SHA-256",
        },
        true,
        ["encrypt", "decrypt"],
    );
    return keyPair;
}


// Encryption
// (plaintxt : String, pubkey : CryptoKey) -> Promise(String (Base64))
async function encryptRSA_OAEP(plaintxt, pubkey) {
    let encoder = new TextEncoder();
    let encodedSecret = encoder.encode(plaintxt);
    console.log(`Encoded ptxt:\n${encodedSecret}`);
  
    let encrypted = await window.crypto.subtle.encrypt({
            name: "RSA-OAEP"
        },
        pubkey,
        encodedSecret
    );
  
    let ct = ab2b64(encrypted);
    console.log(ct /* .replace(/(.{48})/g,'$1\n') */ );
    return ct;
}


// Decryption
// (ciphertxt : String (Base64), privKey : CryptoKey) -> Promise(String)
async function decryptRSA_OAEP(ciphertxt, privKey) {
    const encoded_ctxt = b642ab(ciphertxt);
    console.log(encoded_ctxt.length);
    console.log(`${encoded_ctxt}`);
  
    var plaintxt = await window.crypto.subtle.decrypt({
            name: "RSA-OAEP"
        },
        privKey,
        encoded_ctxt
    );
    console.log(plaintxt.byteLength);
    console.log(`${plaintxt}`);
    let decoder = new TextDecoder();
    var ptxt = decoder.decode(plaintxt);
    console.log(ptxt);
    return ptxt
}



/* ================================================================================
        AES-CTR
        Key generation, encryption and decryption.
        We use a key of 256 bits for the block cipher (AES).
        The counter used for encryption is generated randomly and has a size
        of 16 bytes (eq. 128 bits).
   ================================================================================ */


// Key generation.
// () -> Promise(CryptoKey)
async function genAESCTRKey() {
    let key = await window.crypto.subtle.generateKey({
            name: "AES-CTR",
            length: 256,
        },
        true,
        ["encrypt", "decrypt"],
    );
    return key;
}


// Encryption
// (plaintxt : String, key : CryptoKey) -> Promise(String (Base64))
// The resulting encoded ciphertext includes the counter used during encryption,
// it can be found in the first 16 bytes of the decoded array.
async function encryptAESCTR(plaintxt, key) {
    let encoded = encodeMessage(plaintxt);
    const counter = window.crypto.getRandomValues(new Uint8Array(16));
  
    var ciphertxt = await window.crypto.subtle.encrypt({
        name: "AES-CTR",
        counter: counter,
        length: 128, // The counter has 16 bytes, so it is 16*8=128 bits long.
      },
      key,
      encoded
    );
  
    var ciphertxtArr = new Uint8Array(ciphertxt);
  
    // Append the ctr and the ciphertext. The counter will be needed to decrypt.
    var ctrNCtxt = new Uint8Array(counter.length + ciphertxtArr.length);
    ctrNCtxt.set(counter);
    ctrNCtxt.set(ciphertxtArr, counter.length);
  
    // Return a string with the Base64 encoding of the final ciphertext.
    encodedCtxt = btoa(String.fromCharCode.apply(null, ctrNCtxt));
    return encodedCtxt;
}


// Decryption
// (ciphertxt : String (Base64), key : CryptoKey) -> Promise(String)
async function decryptAESCTR(ciphertxt, key) {
    // Recover the [counter] from the first 16 bytes of the decoded [ciphertext].
    const decoded_ctr_ctxt = b642ab(ciphertxt);
    const counter = decoded_ctr_ctxt.slice(0, 16);
    const ctxt = decoded_ctr_ctxt.slice(16);
  
    var ptxt = await window.crypto.subtle.decrypt({
            name: "AES-CTR",
            counter,
            length: 128
      },
      key,
      ctxt
    );
  
    let decoder = new TextDecoder();
    return decoder.decode(ptxt);
}
