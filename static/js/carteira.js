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

//Event profile SUBMENU

document.addEventListener("DOMContentLoaded", function() {
   var photoProfile = document.querySelector(".photo-profile");
   var submenu = document.getElementById("submenu");
   var timeoutId;
 
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

 //SELECT FILE

 
 