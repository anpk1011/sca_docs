/* Tocbot dynamic TOC, works with tocbot 3.0.2 */
var oldtoc = document.getElementById('toctitle').nextElementSibling;
var newtoc = document.createElement('div');
newtoc.setAttribute('id', 'tocbot');
newtoc.setAttribute('class', 'js-toc');
oldtoc.parentNode.replaceChild(newtoc, oldtoc);
tocbot.init({ 
	contentSelector: '#content',
    headingSelector: 'h1, h2, h3, h4',
    scrollSmooth: false,
    orderedList: false,
    includeHtml: true
});
document.getElementById('toctitle').innerHTML = "Black Duck REST API Usage Guide"

/* Swapping favicon for dark/light mode */
function toggleFavicon(goDark) {
    const favicon = document.querySelector('link[rel="shortcut icon"]');
    const href = goDark ? 
        favicon.href.replace('-white', '-black') : 
        favicon.href.replace('-black', '-white');

    favicon.setAttribute('href', href);
}

// Checks to make sure we're using the right icon
const isLightScheme = window.matchMedia('(prefers-color-scheme:light)');
toggleFavicon(isLightScheme.matches);
        
// Listens for changes to the theme
isLightScheme.onchange = (evt) => {
    toggleFavicon(evt.matches);
};
