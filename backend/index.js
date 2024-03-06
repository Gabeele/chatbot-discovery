// Training 

const natural = require('natural');
const classifier = new natural.LogisticRegressionClassifier();

// Train the classifier with some example sentences
// Reporting different types of problems
classifier.addDocument(['leak under the sink', 'water leaking from ceiling'], 'report_problem');
classifier.addDocument(['broken window handle', 'cracked window glass'], 'report_problem');
classifier.addDocument(['door lock is jammed', 'front door won’t close properly'], 'report_problem');
classifier.addDocument(['dishwasher not turning on', 'washing machine is leaking'], 'report_problem');
classifier.addDocument(['fridge is too warm', 'freezer not working'], 'report_problem');
classifier.addDocument(['oven not heating', 'stove burner won’t light'], 'report_problem');
classifier.addDocument(['clogged bathtub', 'shower drain blocked'], 'report_problem');
classifier.addDocument(['toilet won’t flush', 'running toilet'], 'report_problem');
classifier.addDocument(['wall has damp spots', 'mold in the bathroom'], 'report_problem');
classifier.addDocument(['noisy radiator', 'heating system makes banging noise'], 'report_problem');
classifier.addDocument(['air conditioning unit leaking', 'AC making strange noises'], 'report_problem');
classifier.addDocument(['electrical outlet not working', 'light switch is broken'], 'report_problem');
classifier.addDocument(['smoke detector beeping', 'carbon monoxide alarm going off'], 'report_problem');


// Inquiring about request status
classifier.addDocument(['has my issue been looked at', 'any progress on my maintenance request'], 'status_request');
classifier.addDocument(['estimated time for repair', 'how long until it’s fixed'], 'status_request');
classifier.addDocument(['when will the technician arrive', 'appointment time for repairs'], 'status_request');
classifier.addDocument(['is my request scheduled', 'has a date been set for the repair'], 'status_request');

// Canceling requests
classifier.addDocument(['decided not to proceed with the request', 'cancel the scheduled repair'], 'cancel_request');
classifier.addDocument(['issue resolved without help', 'found a workaround for my problem'], 'cancel_request');
classifier.addDocument(['please stop the maintenance work', 'halt the ongoing repair'], 'cancel_request');
classifier.addDocument(['retract my previous maintenance request', 'decided against the repair service'], 'cancel_request');


// Train the classifier after adding all documents
classifier.train();


classifier.save('classifier.json', function (err, classifier) {
  // the classifier is saved to the classifier.json file!
});

function processMessage(message) {
  const intent = classifier.classify(message);

  switch (intent) {
    case 'report_problem':
      return { message: "It sounds like you're reporting a problem. Can you provide more details?" };
    case 'status_request':
      return { message: "You're asking for the status of a request. Let me check on that." };
    case 'cancel_request':
      return { message: "You want to cancel a request. Please provide the request ID." };
    default:
      return { message: "Sorry, I didn't understand that." };
  }
}

// Server code
const express = require('express');
const bodyParser = require('body-parser'); // To parse JSON body in requests

const app = express();
const PORT = 3001;

app.use(bodyParser.json()); // Middleware to parse JSON bodies


// Serve the chatbot's page at the root URL
app.get('/', (req, res) => {
  res.sendFile('index.html', { root: __dirname });
});

app.get('/api/chat', (req, res) => {

  // Create a random token, send it as the response and log it
  console.log('Received request for a new chat token');
  res.json({ token: Math.random().toString(36).substring(7), message: 'Hello! How can I help you?', options: ['Maintenance Request', 'Question about my Contract', 'Complaint', 'Other'] });

}
);

// Chatbot API endpoint
app.post('/api/chat/message', (req, res) => {

  console.log('Request received')

  const message = req.body.message;

  console.log(`Received message: ${message}`);

  const data = processMessage(message);
  console.log(data)


  console.log(`Responding with: ${data.message}`);
  res.json(data);

});


app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});

