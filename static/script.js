
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("translationForm");

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        translateText();
    });
});

// Fonction appelée lorsqu'on clique sur le bouton "Traduire"
async function translateText() {
    // Récupérer les valeurs des champs du formulaire
    const texte = document.getElementById("texte").value;
    const source = document.getElementById("source").value;
    const target = document.getElementById("target").value;

    // Envoyer une requête POST à Flask
    fetch("/translate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: texte,
            source: source,
            target: target
        })
    })
        .then(response => response.json())
        .then(data => {
            const translated = data.translated_text;  // On récupère directement la valeur
            const resultDiv = document.getElementById("outputText");
            resultDiv.textContent = translated;
        })
        .catch(error => {
            console.error("Erreur lors de la traduction :", error);
        });
}

function speakText(type) {
    let text, lang;

    if (type === 'input') {
        text = document.getElementById("texte").value;
        lang = document.getElementById("source").value;
    } else {
        text = document.getElementById("outputText").textContent;
        lang = document.getElementById("target").value;
    }

    fetch("/synthetize", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text,
            lang: lang
        })
    })
        .then(response => {
            if (!response.ok) throw new Error("Erreur réseau");
            return response.blob(); // On attend un fichier audio
        })
        .then(audioBlob => {
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play();
        })
        .catch(error => {
            console.error("Erreur de synthèse vocale :", error);
        });
}

function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).innerText;
    navigator.clipboard.writeText(text)
        .then(() => alert("Texte copié !"))
        .catch(err => alert("Erreur de copie : " + err));
}
