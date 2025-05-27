// Utility function to send POST request with JSON
async function postData(url = '', data = {}) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Something went wrong');
        }

        return result;

    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
    }
}

// Handle signup
async function handleSignup(event) {
    event.preventDefault();

    const signupData = {
        username: document.getElementById('signup-username').value,
        password: document.getElementById('signup-password').value
    };
    const response = await postData('http://localhost:5000/signup', signupData);

    if (response) {
        alert('Signup successful! Please log in.');
        // Optionally reset the form
        document.getElementById('signup-form').reset();
    }
}

// Handle login
async function handleLogin(event) {
    event.preventDefault();

    const loginData = {
        username: document.getElementById('login-username').value,
        password: document.getElementById('login-password').value
    };

    const response = await postData('http://localhost:5000/login', loginData);

    if (response && response.token) {
        alert('Login successful!');
        localStorage.setItem('username', loginData.username);
        localStorage.setItem('authToken', response.token);

        // Redirect to dashboard or any protected page
        window.location.href = '/index.html';
    }
}

// Add event listeners after DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }
});
