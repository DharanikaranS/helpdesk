document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById('complaint-form');
  
  form.addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent the default form submission
      
      // Get form data
      const formData = {
          help_topic: document.getElementById('help_topic').value,
          description: document.getElementById('description').value,
          location: document.getElementById('location').value,
          room_no: document.getElementById('room_no').value,
          mob_no: document.getElementById('mob_no').value,
          preferred_time: document.getElementById('preferred_time').value
      };

      fetch('/submit_clog', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              alert('Complaint submitted successfully!');
          } else {
              alert('Error submitting complaint.');
          }
      })
      .catch(error => {
          console.error('Error:', error);
          alert('An error occurred.');
      });
  });
});
