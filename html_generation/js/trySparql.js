function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

if (gdbUrl) {
    var headingsArr = Array.from(document.querySelectorAll('.sparql'));
    headingsArr.forEach((h) => {
        var query = h.innerText;
        var a = document.createElement("a");
        var linkText = document.createTextNode("Try it");
        a.setAttribute('target', '_blank');
        a.setAttribute('class', 'externalLink');
        a.appendChild(linkText);
        a.title = "Try it";

        if(typeof prefixes !== 'undefined'){
            a.href = gdbUrl + "sparql?query=" + encodeURIComponent(prefixes)+ encodeURIComponent(query);
        } else {
            a.href = gdbUrl + "sparql?query=" + encodeURIComponent(query);
        }

        document.body.appendChild(a);
        insertAfter(h, a);
    })
}

