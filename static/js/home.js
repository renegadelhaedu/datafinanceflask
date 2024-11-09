function op1() {
    document.getElementById('iframeTarget').src = "{{url_for('atualizarcorrelacaoallindicadores')}}";
    var data = document.getElementById('nameData');
    data.textContent = "CALCULATE RISK RETURN"
}
function op2() {
    document.getElementById('iframeTarget').src = "{{url_for('gerarminhacarteira')}}";
    var data = document.getElementById('nameData');
    data.textContent = "Wallet"
}
function op3() {
    var iframe = document.getElementById('iframeTarget');
    iframe.src = "{{url_for('/minhacarteira')}}";
    var data = document.getElementById('nameData');
    data.textContent = "Ranking Dividends"
}
function op4() {
    var iframe = document.getElementById('iframeTarget');
    iframe.src = "{{url_for('calcularRiscoRetorno', opcao=GET)}}";
    var data = document.getElementById('nameData');
    data.textContent = "Correlacao Indicators"
}
function op5() {
    var iframe = document.getElementById('iframeTarget');
    iframe.src = "{{url_for('calcularRiscoRetorno', opcao=GET)}}";
    var data = document.getElementById('nameData');
    data.textContent = "data"
}

/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
      navToggle = document.getElementById('nav-toggle'),
      navClose = document.getElementById('nav-close')

/* Menu show */
navToggle.addEventListener('click', () =>{
   navMenu.classList.add('show-menu')
})

/* Menu hidden */
navClose.addEventListener('click', () =>{
   navMenu.classList.remove('show-menu')
})

/*=============== SEARCH ===============*/
const search = document.getElementById('search'),
      searchBtn = document.getElementById('search-btn'),
      searchClose = document.getElementById('search-close')

/* Search show */
searchBtn.addEventListener('click', () =>{
   search.classList.add('show-search')
})

/* Search hidden */
searchClose.addEventListener('click', () =>{
   search.classList.remove('show-search')
})

/*=============== LOGIN ===============*/
const login = document.getElementById('login'),
      loginBtn = document.getElementById('login-btn'),
      loginClose = document.getElementById('login-close')

/* Login show */
loginBtn.addEventListener('click', () =>{
   login.classList.add('show-login')
})

/* Login hidden */
loginClose.addEventListener('click', () =>{
   login.classList.remove('show-login')
})

/*=============== CAROUSEL ===============*/



 



