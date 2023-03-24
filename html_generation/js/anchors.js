var headingsArr = Array.from(document.querySelectorAll('h1, h2, h3, h4'));
headingsArr.forEach(h => {
    var id = h.getAttribute('id');
    var link = document.createElement('a');
    link.setAttribute('href', '#' + id);
    link.className = 'anchor-link'
    h.classList.add('anchor-heading')
    link.innerHTML = h.innerHTML;
    h.innerHTML = link.outerHTML;
});