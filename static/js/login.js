document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById('login-form');
    
    loginForm.addEventListener('submit', function(event) {
      event.preventDefault();
      const usernameInput = document.getElementById('username');
      const username = usernameInput.value.trim();
      if (username) {
        // Salvar o nome do usuário no armazenamento local (localStorage)
        localStorage.setItem('username', username);
        window.location.href = "./templates/logado.html";
      }
    });
  
    // Verificar se o usuário já fez login anteriormente
    const username = localStorage.getItem('username');
    if (username) {
      const loginContainer = document.getElementById('login-container');
      loginContainer.innerHTML = `<p>Bem-vindo, ${username}!</p>`;
    }
  });
  