const loginButton = document.querySelector("#login-button")
const loginContainer = document.querySelector("#login-container")
const loginClose = document.querySelector("#login-close")

const rankingButton = document.querySelector("#action-button")
const mainIframe = document.querySelector("#iframe-main")
const carrouselIframe = document.querySelector("#iframe-carousel")
const cardIframe = document.querySelector("#iframe-card")


loginButton.addEventListener("click", () => {
   loginContainer.classList.toggle("hidden")
   console.log(loginContainer);
})

loginClose.addEventListener("click", () => {
   loginContainer.classList.toggle("hidden")
})

rankingButton.addEventListener("click", () => {
   mainIframe.src = "/rankingacoes/all"
   mainIframe.classList.toggle("hidden")
   carrouselIframe.classList.toggle("hidden")
   cardIframe.classList.toggle("hidden")
})