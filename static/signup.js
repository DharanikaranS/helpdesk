document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    
    // Retrieve form values
    var fullName = document.getElementById('fullname').value.trim();
    var email = document.getElementById('email').value.trim();
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;
    
    // Client-side validation
    if (!fullName || !email || !password || !confirmPassword) {
        alert('Please fill in all fields.');
        return;
    }
    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return;
    }

    // If validation passed, proceed with form submission using Fetch API
    var formData = {
        fullname: fullName,
        email: email,
        password: password
    };

    fetch('/submit_signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.redirected ? window.location.href = response.url : response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/signin';
        } else {
            alert('Signup failed. Please try again.');
        }
    })
    .catch(error => console.error('Error:', error));
});