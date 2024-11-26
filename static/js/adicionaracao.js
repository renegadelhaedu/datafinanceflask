const numberInput = document.querySelector("#number-input")
const amountInput = document.querySelector("#amount-input")
const priceInput = document.querySelector("#price-input")

const arrayInputs = [amountInput, priceInput]

const validDigits = (text) => {
    return text.replace(/[^0-9,]/g, "")
}

arrayInputs.forEach((input) => {
    input.addEventListener("input", (e) => {
        const updateValue = validDigits(e.target.value)

        e.target.value = updateValue
    })
})