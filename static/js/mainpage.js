const subMenuProfile = document.querySelector("#submenu")
const imageProfile = document.querySelector("#photo-profile")

imageProfile.addEventListener("click", () => {
    subMenuProfile.classList.toggle("hidden")
})