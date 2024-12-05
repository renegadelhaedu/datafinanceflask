const subMenuProfile = document.querySelector("#submenu")
const imageProfile = document.querySelector("#photo-profile")

imageProfile.addEventListener("click", () => {
    subMenuProfile.classList.toggle("hidden")
})

function enviariframe(endpoint) {
            event.preventDefault();
            var iframe = document.getElementById('iframe-card');
            iframe.src = endpoint;
}