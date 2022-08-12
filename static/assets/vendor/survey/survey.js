const btn = document.querySelector('#btn');
const sb = document.querySelector('#algorithm')
btn.onclick = (event) => {
    event.preventDefault();
    // show the selected index
    alert(sb.selectedIndex);
};