// Importing the bot and user svg files
import bot from './assets/bot.svg'
import user from './assets/user.svg'

// Selecting the HTML elements
const form = document.querySelector('form')
const chatContainer = document.querySelector('#chat_container')

// Declaring the loadInterval variable
let loadInterval

// Loader function to create typing animation with the loading indicator
function loader(element) {
    element.textContent = ''

    // Start the interval to update the text content of the loading indicator
    loadInterval = setInterval(() => {
        element.textContent += '.'

        // Reset the loading indicator if it has reached three dots
        if (element.textContent === '....') {
            element.textContent = ''
        }
    }, 300)
}

// Function to type text with a typing effect
function typeText(element, text) {
    let index = 0

    // Start the interval to type the text with a typing effect
    let interval = setInterval(() => {
        if (index < text.length) {
            element.innerHTML += text.charAt(index)
            index++
        } else {
            clearInterval(interval)
        }
    }, 20)
}

// Function to generate a unique ID for each message div of the bot
// Necessary for typing text effect for that specific reply
// Without unique ID, typing text will work on every element
function generateUniqueId() {
    const timestamp = Date.now()
    const randomNumber = Math.random()
    const hexadecimalString = randomNumber.toString(16)

    return `id-${timestamp}-${hexadecimalString}`
}

// Function to create chat stripe
function chatStripe(isAi, value, uniqueId) {
    return (
        `
        <div class="wrapper ${isAi && 'ai'}">
            <div class="chat">
                <div class="profile">
                    <img 
                      src=${isAi ? bot : user} 
                      alt="${isAi ? 'bot' : 'user'}" 
                    />
                </div>
                <div class="message" id=${uniqueId}>${value}</div>
            </div>
        </div>
    `
    )
}

// Function to handle form submit
const handleSubmit = async (e) => {
    e.preventDefault()

    const data = new FormData(form)

    // User's chat stripe
    chatContainer.innerHTML += chatStripe(false, data.get('prompt'))

    // Clear the textarea input 
    form.reset()

    // Bot's chat stripe
    const uniqueId = generateUniqueId()
    chatContainer.innerHTML += chatStripe(true, " ", uniqueId)

    // Focus scroll to the bottom 
    chatContainer.scrollTop = chatContainer.scrollHeight

    // Specific message div 
    const messageDiv = document.getElementById(uniqueId)

    // Show the loading indicator
    loader(messageDiv)

    const response = await fetch('http://localhost:5000/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prompt: data.get('prompt')
        })
    })

    clearInterval(loadInterval)
    messageDiv.innerHTML = " "

    if (response.ok) {
        const data = await response.json()
        const parsedData = data.bot.trim() // Trim any trailing spaces/'\n' 

        // Type the bot's response with typing effect
        typeText(messageDiv, parsedData)
    } else {
        const err = await response.text()

        messageDiv.innerHTML = "Something went wrong"
        console.log(err)

    }
}

// Add event listeners to the form for submitting and keyup (if enter is pressed)
form.addEventListener('submit', handleSubmit)
form.addEventListener('keyup', (e) => {
    if (e.keyCode === 13) {
        handleSubmit(e)

    }
})