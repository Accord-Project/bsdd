let elementToBeSearched = document.querySelector("body");

// Begin traversing the child elements as an array
Array.prototype.slice.call(elementToBeSearched.children).forEach(function(node){
    // Replace keywords with span elements that are tied to the correct CSS class.
    node.innerHTML = node.innerHTML.replace(/TODO( M\d+)*/g, "<span class='text-danger'>TODO $1</span>");
});