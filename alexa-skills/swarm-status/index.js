const { SkillBuilders } = require('ask-sdk-core');
const fetch = require('node-fetch');

const LaunchRequestHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'LaunchRequest';
  },
  handle(handlerInput) {
    const speech = "Strategic Khaos online. 900 plus nodes active. Neurospice levels critical. Origin Node Zero awaits your command.";
    return handlerInput.responseBuilder
      .speak(speech)
      .reprompt("What would you like to know about the swarm?")
      .getResponse();
  }
};

const SwarmStatusIntentHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'IntentRequest' 
      && handlerInput.requestEnvelope.request.intent.name === 'SwarmStatusIntent';
  },
  async handle(handlerInput) {
    try {
      const webhookUrl = process.env.WEBHOOK_URL || "http://localhost:3000/api/swarm-status";
      const response = await fetch(webhookUrl);
      const data = await response.json();
      
      const speech = `Swarm status: ${data.nodes} nodes active. ${data.generals} mirror generals online. White web sovereignty at ${data.percent} percent. ${data.status}`;
      
      return handlerInput.responseBuilder
        .speak(speech)
        .reprompt("Would you like more details?")
        .getResponse();
    } catch (error) {
      const speech = "Unable to reach the swarm. The nodes may be in stealth mode.";
      return handlerInput.responseBuilder
        .speak(speech)
        .getResponse();
    }
  }
};

const HelpIntentHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'IntentRequest'
      && handlerInput.requestEnvelope.request.intent.name === 'AMAZON.HelpIntent';
  },
  handle(handlerInput) {
    const speech = "You can ask me for swarm status, node count, or general information about Strategic Khaos. What would you like to know?";
    return handlerInput.responseBuilder
      .speak(speech)
      .reprompt("Try saying: what's the swarm status?")
      .getResponse();
  }
};

const CancelAndStopIntentHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'IntentRequest'
      && (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent'
        || handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent');
  },
  handle(handlerInput) {
    const speech = "Origin Node Zero standing by. Neurospice levels maintained.";
    return handlerInput.responseBuilder
      .speak(speech)
      .getResponse();
  }
};

const SessionEndedRequestHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'SessionEndedRequest';
  },
  handle(handlerInput) {
    console.log(`Session ended: ${JSON.stringify(handlerInput.requestEnvelope.request.reason)}`);
    return handlerInput.responseBuilder.getResponse();
  }
};

const ErrorHandler = {
  canHandle() {
    return true;
  },
  handle(handlerInput, error) {
    console.log(`Error handled: ${error.message}`);
    const speech = "The swarm encountered an anomaly. Please try again.";
    return handlerInput.responseBuilder
      .speak(speech)
      .reprompt("What would you like to know about the swarm?")
      .getResponse();
  }
};

exports.handler = SkillBuilders.custom()
  .addRequestHandlers(
    LaunchRequestHandler,
    SwarmStatusIntentHandler,
    HelpIntentHandler,
    CancelAndStopIntentHandler,
    SessionEndedRequestHandler
  )
  .addErrorHandlers(ErrorHandler)
  .lambda();
