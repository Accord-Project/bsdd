var elArray = document.getElementsByClassName("mockup");

var arrayLength = elArray.length;

for (var i = 0; i < arrayLength; i++) {
    var innerText = elArray[i].innerHTML;

    var address = document.getElementsByClassName('mockup')[i].dataset.address;
    console.log(address);
    // inserts beginning of mockup

    elArray[i].innerHTML = "<body>\n" +
        "<div class=\"menuBar\">\n" +
        "    <div class=\"menuRow\">\n" +
        "        <div class=\"browserField left\">\n" +
        "            <span class=\"menuBarDots\" style=\"background:#ED594A;\"></span>\n" +
        "            <span class=\"menuBarDots\" style=\"background:#FDD800;\"></span>\n" +
        "            <span class=\"menuBarDots\" style=\"background:#5AC05A;\"></span>\n" +
        "        </div>\n" +
        "        <div class=\"browserField middle\">\n" +
        "            <input type=\"text\" value=" + '"' + address + '"' + ">" +
        "        </div>\n" +
        "<div class=\"browserField right\">" +
        "<div style=\"float:right\">" +
        "   <span class=\"menuDots\"></span>" +
        "   <span class=\"menuDots\"></span>" +
        "<span class=\"menuDots\"></span>" +
        " </div> " +
        "   </div> " +
        "    </div>\n" +
        "    <div class=\"content\"> "
        + innerText
        + "</div></div><br></body>"
}
