window.addEventListener('storage', function(event) {
  if(event.key === 'login') {
    window.location.reload();
  }
});

function showForm(form) {
    console.log("Show function executed");
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('register-form').classList.add('hidden');
    document.getElementById(form + '-form').classList.remove('hidden');
}

async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
        credentials: "include"
    });
    if (response.ok) {
        const data = await response.json();
        document.cookie = `access_token=${data.access_token}; path=/; SameSite=Lax`;
        localStorage.setItem('login', Date.now());
        window.location.href = "/";
    } else {
        alert("Invalid username or password");
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;
    const response = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
        credentials: "include"
    });
    if (response.ok) {
        const data = await response.json();
        document.cookie = `access_token=${data.access_token}; path=/; SameSite=Lax`;
        localStorage.setItem('login', Date.now());
        window.location.href = "/";
    } else {
        alert("Registration failed");
    }
}

showForm('login');