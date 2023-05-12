import express from 'express'
import * as dotenv from 'dotenv'
import cors from 'cors'
import { Configuration, OpenAIApi } from 'openai'

dotenv.config()

// Configure the OpenAI API with the provided API key
const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});

// Initialize the OpenAIApi client with the configuration
const openai = new OpenAIApi(configuration);

// Create a new Express app instance
const app = express()

// Enable CORS middleware to allow cross-origin requests
app.use(cors())

// Parse request bodies as JSON
app.use(express.json())

// Respond with a simple greeting on a GET request to the root endpoint
app.get('/', async (req, res) => {
  res.status(200).send({
    message: 'Hello from CodeX!'
  })
})

// Handle POST requests to the root endpoint by querying the OpenAI API
app.post('/', async (req, res) => {
  try {
    // Extract the prompt from the request body
    const prompt = req.body.prompt;

    // Send a request to the OpenAI API to generate a completion based on the prompt
    const response = await openai.createCompletion({
      model: "text-davinci-003",
      prompt: `${prompt}`,
      temperature: 0, // Higher values means the model will take more risks.
      max_tokens: 3000, // The maximum number of tokens to generate in the completion. Most models have a context length of 2048 tokens (except for the newest models, which support 4096).
      top_p: 1, // alternative to sampling with temperature, called nucleus sampling
      frequency_penalty: 0.5, // Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
      presence_penalty: 0, // Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
    });

    // Send the generated completion text back to the client
    res.status(200).send({
      bot: response.data.choices[0].text
    });
  } catch (error) {
    // Log any errors and respond with a 500 error status
    console.error(error)
    res.status(500).send(error || 'Something went wrong');
  }
})

// Start the Express app on port 5000 and log a message to the console
app.listen(5000, () => console.log('AI server started on http://localhost:5000'))
