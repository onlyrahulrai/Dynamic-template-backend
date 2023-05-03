window.addEventListener("load", () => {
  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then(function(stream) {
      // Create a new instance of the SpeechSynthesisUtterance object
      const utterance = new SpeechSynthesisUtterance();

      // Set the text to be spoken
      utterance.text = `welcome ${user} in the Fixed layout template.`;

      utterance.lang = "en-US";

      // Set the voice for speech synthesis (optional)
      utterance.voice = speechSynthesis.getVoices()[0];

      // Add event listeners for the speech synthesis events
      utterance.onstart = () => {
        console.log("Speech synthesis started");
      };

      utterance.onend = () => {
        console.log("Speech synthesis ended");
      };

      utterance.onerror = (event) => {
        console.error(`Speech synthesis error: ${event.error}`);
      };

      // Start the speech synthesis
      speechSynthesis.speak(utterance);
    })
    .catch(function(error) {
      // Microphone and sound permission denied or error occurred
    });
});
