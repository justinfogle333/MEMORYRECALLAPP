/**
 * Google Apps Script — Survey Completion Webhook
 * ===============================================
 * 
 * This script runs inside Google Forms and sends a POST request
 * to your Review Agent server every time someone submits the survey.
 * 
 * SETUP INSTRUCTIONS:
 * 1. Open your Google Form
 * 2. Click the three dots menu -> Script Editor
 * 3. Paste this entire script
 * 4. Replace YOUR_SERVER_URL with your actual server URL
 * 5. Click Run -> onFormSubmit (to authorize permissions)
 * 6. Go to Triggers (clock icon) -> Add Trigger:
 *    - Function: onFormSubmit
 *    - Event type: On form submit
 * 7. Save
 * 
 * IMPORTANT: Your Google Form must include a hidden field or 
 * pre-filled parameter that passes the customer_id. The easiest
 * way is to use the pre-filled URL from the SMS:
 * https://docs.google.com/forms/d/YOUR_FORM_ID/viewform?entry.FIELD_ID=CUSTOMER_ID
 */

const WEBHOOK_URL = "https://YOUR_SERVER_URL/webhook/survey-complete";

function onFormSubmit(e) {
  try {
    // Get form responses
    const responses = e.response.getItemResponses();
    
    // Extract customer_id from the first response or a hidden field
    // Adjust the index based on your form structure
    let customerId = "";
    let customerEmail = "";
    
    for (let i = 0; i < responses.length; i++) {
      const title = responses[i].getItem().getTitle().toLowerCase();
      const answer = responses[i].getResponse();
      
      if (title.includes("customer") || title.includes("id")) {
        customerId = answer;
      }
      if (title.includes("email")) {
        customerEmail = answer;
      }
    }
    
    // If customer_id wasn't in the form, try to get it from the URL parameter
    if (!customerId) {
      // You can also parse it from the pre-filled URL if needed
      Logger.log("Warning: No customer_id found in form responses");
      return;
    }
    
    // Send webhook to Review Agent server
    const payload = {
      "customer_id": parseInt(customerId),
      "email": customerEmail
    };
    
    const options = {
      "method": "post",
      "contentType": "application/json",
      "payload": JSON.stringify(payload),
      "muteHttpExceptions": true
    };
    
    const response = UrlFetchApp.fetch(WEBHOOK_URL, options);
    Logger.log("Webhook response: " + response.getContentText());
    
  } catch (error) {
    Logger.log("Error in onFormSubmit: " + error.toString());
  }
}
