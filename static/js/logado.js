document.addEventListener("DOMContentLoaded", function() {
    const username = localStorage.getItem('username');
    if (username) {
        const newMessage = document.getElementById('newMessage');
        newMessage.textContent = `Bem-vindo, ${username}!`;
    }

    var photoProfile = document.querySelector(".photo-profile");
    var submenu = document.getElementById("submenu");
    var timeoutId;

    photoProfile.addEventListener("click", function() {
        document.getElementById("fileInput").click();
    });

    photoProfile.addEventListener("mouseenter", function() {
        clearTimeout(timeoutId);
        submenu.style.display = "block"; 
    });
  
    photoProfile.addEventListener("mouseleave", function() {
        timeoutId = setTimeout(function() {
            submenu.style.display = "none";
        }, 100);
    });
  
    submenu.addEventListener("mouseenter", function() {
        clearTimeout(timeoutId);
        submenu.style.display = "block";
    });
  
    submenu.addEventListener("mouseleave", function() {
        timeoutId = setTimeout(function() {
            submenu.style.display = "none";
        }, 100);
    });
});

function op1() {
    var data = document.getElementById('nameData');
    data.textContent = "CALCULATE RISK RETURN"
    document.getElementById('wallet').src = "{{url_for('gerarminhacarteira')}}";
}

function op2() {
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
